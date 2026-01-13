from __future__ import annotations

import json
from dataclasses import replace
from functools import lru_cache
from pathlib import Path
from typing import Any, Dict, List

import tornado.web
from jupyter_server.base.handlers import APIHandler

from .agent_frontend_ops import NotebookPaths
from .agent_logging import get_deepanalyze_logger
from .agent_llm_gateway import chat_completions
from .agent_llm_gateway import chat_completions_stream
from .agent_orchestrator import handle_feedback, handle_user_message
from .agent_model_store import generate_custom_model_id, upsert_model
from .agent_secret_store import get_api_key, get_api_key_status, set_and_validate_api_key
from .agent_session_store import get_session_store
from .agent_settings import get_agent_settings
from .agent_tag_parser import extract_answer_text
from .model_registry import get_default_model_id, load_model_specs, resolve_model_spec
from .notebook_tools import DeepAnalyzeNotebookTool

logger = get_deepanalyze_logger("deepanalyze.backend")

"""
后端 HTTP API（Jupyter Server Extension）。

接口设计目标：
- chat / feedback 返回统一结构：`reply`（给 Chat 面板）+ `data`（给前端编排器 open.ts 执行 frontend_ops）。
- 流式接口使用 SSE（start/delta/final），便于前端实现“scratch 流式占位”。
"""


def _extract_model_id(payload: Dict[str, Any]) -> str:
    return str(payload.get("model_id") or payload.get("modelId") or "").strip()


def _extract_prompt_lang(payload: Dict[str, Any]) -> str:
    return str(payload.get("prompt_lang") or payload.get("promptLang") or "").strip()


def _normalize_prompt_lang(raw: str) -> str:
    v = str(raw or "").strip().lower()
    if v in {"zh", "zh-cn", "zh_cn", "cn"}:
        return "zh"
    if v in {"en", "en-us", "en_us"}:
        return "en"
    return ""


@lru_cache(maxsize=2)
def _available_prompt_names() -> set[str]:
    """
    返回 deepanalyze/prompts/index.json 中声明的 prompts name 集合，用于在选择 _ZH 版本时做兜底。
    """

    index_path = Path(__file__).resolve().parent / "prompts" / "index.json"
    if not index_path.exists():
        return set()
    try:
        data = json.loads(index_path.read_text(encoding="utf-8"))
    except Exception:  # noqa: BLE001
        return set()
    items = data.get("prompts") if isinstance(data, dict) else None
    if not isinstance(items, list):
        return set()
    names: set[str] = set()
    for it in items:
        if not isinstance(it, dict):
            continue
        name = str(it.get("name") or "").strip()
        if name:
            names.add(name)
    return names

def _session_key(session_id: str, model_id: str, prompt_lang: str) -> str:
    sid = str(session_id or "").strip() or "anonymous"
    mid = str(model_id or "").strip() or "default"
    lang = _normalize_prompt_lang(prompt_lang) or "en"
    return f"{sid}::model={mid}::lang={lang}"


def _apply_model_to_settings(settings, *, model_id: str, prompt_lang: str = ""):
    """
    根据前端选择的 model_id，动态覆写本次请求使用的后端、base_url、模型名与 system prompt。

    注意：
    - `SessionState` 里的 system prompt 只会注入一次；因此我们用 session_key 把“同一个 session_id
      在不同模型下的会话”隔离开，避免中途切换模型导致 system prompt/上下文混用。
    """

    spec = resolve_model_spec(settings=settings, model_id=model_id)
    configured_prompt_name = str(spec.prompt_name or getattr(settings, "system_prompt_name", "general"))
    # 约定：中文版本 prompt 使用 `<name>_ZH`（文件名也同理）
    base = configured_prompt_name[:-3] if configured_prompt_name.endswith("_ZH") else configured_prompt_name
    lang = _normalize_prompt_lang(prompt_lang) or "en"
    candidate = f"{base}_ZH" if lang == "zh" else base
    # 若目标语言版本不存在，则回退到配置值（避免 load_system_prompt 进一步兜底到默认 deepanalyze_8b）
    prompt_name = candidate if candidate in _available_prompt_names() else configured_prompt_name
    effective = replace(
        settings,
        llm_backend=str(spec.backend or "vllm"),
        vllm_base_url=str(spec.base_url or settings.vllm_base_url),
        vllm_model=str(spec.model or settings.vllm_model),
        system_prompt_name=prompt_name,
        system_prompt_path="",
        active_model_id=str(spec.id or getattr(settings, "active_model_id", "")),
        llm_temperature=float(getattr(spec, "temperature", 0.4) or 0.4),
    )
    # 外部 OpenAI-compatible：避免透传 vLLM 特有字段引发服务端 400
    if str(spec.backend or "").strip().lower() != "vllm":
        effective = replace(
            effective,
            vllm_add_generation_prompt=False,
            vllm_stop_token_ids=[],
            # 外部 API 的 max_tokens 通常更严格，默认做一个保守上限以减少 400 风险
            vllm_max_new_tokens=min(int(getattr(settings, "vllm_max_new_tokens", 0) or 0), 4096)
            if int(getattr(settings, "vllm_max_new_tokens", 0) or 0) > 0
            else 2048,
        )
    return effective, spec


def _clean_cell_rewrite_answer(text: str) -> str:
    """
    清理大模型在回答中可能附带的语言标记/代码围栏（如 [python]、```python ... ```）。

    说明：
    - 目标是把“单元格最终内容”提取出来，避免把围栏符号写回 cell。
    - 对于完整包裹的 fenced code block，会直接提取其中内容；
      对于仅在开头出现的标记，会移除开头标记；结尾 ``` 会在存在时移除。
    """

    s = str(text or "").replace("\r\n", "\n").strip()
    if not s:
        return ""

    lower = s.lstrip().lower()
    if lower.startswith("[python]") or lower.startswith("[py]"):
        # 去掉首行 [python]/[py]
        lines = s.split("\n")
        if lines:
            first = lines[0].strip().lower()
            if first in ("[python]", "[py]"):
                s = "\n".join(lines[1:]).strip()

    stripped = s.lstrip()
    if stripped.startswith("```"):
        # 完整 fenced code block：```python\n...\n```
        lines = s.split("\n")
        if len(lines) >= 2 and lines[0].lstrip().startswith("```"):
            first = lines[0].strip()
            last = lines[-1].strip()
            if last == "```":
                s = "\n".join(lines[1:-1]).strip("\n")
                # 去掉第一行的语言标记（```python / ```py / ```）
                if first.lower().startswith("```python") or first.lower().startswith("```py") or first == "```":
                    return s.strip()

        # 非完整包裹：尽量只移除开头围栏行与末尾单独一行的 ```
        if "\n" in s and lines[0].lstrip().startswith("```"):
            s = "\n".join(lines[1:])
        s = s.rstrip()
        if s.endswith("\n```"):
            s = s[: -len("\n```")]

    return s.strip()


class ChatHandler(APIHandler):
    @tornado.web.authenticated
    async def post(self) -> None:
        payload: Dict[str, Any] = self.get_json_body() or {}
        message = str(payload.get("message", "") or "").strip()
        session_id = str(payload.get("session_id") or payload.get("sessionId") or "").strip()
        model_id = _extract_model_id(payload)
        prompt_lang = _extract_prompt_lang(payload)

        tool = DeepAnalyzeNotebookTool(
            contents_manager=self.contents_manager,
            kernel_manager=self.kernel_manager,
            state={},
        )

        context = payload.get("context") or {}
        if isinstance(context, dict):
            tool.set_active_context(
                workspace_dir=context.get("workspaceDir") or context.get("workspace_dir"),
                output_path=context.get("outputPath") or context.get("output_path"),
                scratch_path=context.get("scratchPath") or context.get("scratch_path"),
            )

        # 约定：若用户消息本身是 JSON（形如 {"op":"list_workspaces"}），则走“工具模式”，不走大模型生成。
        if message.startswith("{") and message.endswith("}"):
            try:
                op_payload = json.loads(message)
                result = await tool.handle_op(op_payload)
                reply = str(result.get("reply") or "")
                logger.info(
                    "tool_op ok session_id=%s op=%s",
                    session_id or "-",
                    str(op_payload.get("op") or ""),
                )
                self.set_header("Content-Type", "application/json")
                self.finish(
                    json.dumps(
                        {"reply": reply, "data": {**result, "session_id": session_id}},
                        ensure_ascii=False,
                    )
                )
                return
            except Exception as e:  # noqa: BLE001
                logger.exception("tool_op failed session_id=%s", session_id or "-")
                reply = f"命令解析/执行失败：{e}\n\n{tool.to_help_text()}"
                self.set_header("Content-Type", "application/json")
                self.finish(json.dumps({"reply": reply}, ensure_ascii=False))
                return

        # /help 与 /reset 属于“控制命令”，用于帮助/重置，不走 LLM。
        if message in ("/help", "help", "/da", "/da help"):
            reply = tool.to_help_text()
        else:
            if message in ("/reset", "reset"):
                settings = get_agent_settings()
                effective_settings, _spec = _apply_model_to_settings(
                    settings,
                    model_id=(model_id or getattr(settings, "active_model_id", "")),
                    prompt_lang=prompt_lang,
                )
                if session_id:
                    get_session_store().reset(
                        _session_key(session_id, effective_settings.active_model_id, prompt_lang)
                    )
                logger.info(
                    "reset session_id=%s model_id=%s",
                    session_id or "-",
                    effective_settings.active_model_id,
                )
                reply = "已重置当前会话。"
            else:
                settings = get_agent_settings()
                effective_settings, _spec = _apply_model_to_settings(
                    settings,
                    model_id=(model_id or getattr(settings, "active_model_id", "")),
                    prompt_lang=prompt_lang,
                )
                ctx = tool.active_context()
                workspace_dir = str(ctx.get("workspace_dir") or "").strip()
                output_path = str(ctx.get("output_path") or "").strip()
                scratch_path = str(ctx.get("scratch_path") or "").strip()

                if workspace_dir and output_path and scratch_path and message and session_id:
                    try:
                        store_key = _session_key(
                            session_id, effective_settings.active_model_id, prompt_lang
                        )
                        session = get_session_store().get_or_create(store_key)
                        logger.info(
                            "chat start session_id=%s model_id=%s backend=%s workspace=%s message_len=%s",
                            store_key,
                            effective_settings.active_model_id,
                            getattr(effective_settings, "llm_backend", "-"),
                            workspace_dir,
                            len(message),
                        )
                        data = await handle_user_message(
                            session=session,
                            session_id=store_key,
                            settings=effective_settings,
                            contents_manager=self.contents_manager,
                            workspace_dir=workspace_dir,
                            notebook_paths=NotebookPaths(
                                output_path=output_path, scratch_path=scratch_path
                            ),
                            user_message=message,
                        )
                        reply = str(data.get("reply") or "")
                        logger.info(
                            "chat ok session_id=%s model_id=%s await_feedback=%s ops=%s",
                            store_key,
                            effective_settings.active_model_id,
                            bool(data.get("await_feedback")),
                            len(data.get("frontend_ops") or []),
                        )
                        self.set_header("Content-Type", "application/json")
                        self.finish(json.dumps({"reply": reply, "data": data}, ensure_ascii=False))
                        return
                    except Exception as e:  # noqa: BLE001
                        logger.exception("chat failed session_id=%s", session_id)
                        reply = f"调用模型失败：{e}"
                else:
                    reply = "缺少工作区上下文或 session_id（请先进入 DeepAnalyze 工作区再对话）。"

        self.set_header("Content-Type", "application/json")
        self.finish(json.dumps({"reply": reply}, ensure_ascii=False))


class ChatStreamHandler(APIHandler):
    """
    流式聊天接口：以 SSE 的形式把 vLLM 增量 token 推送给前端。

    约定：
    - 响应为 `text/event-stream`；
    - 每个事件使用 `data: <json>\n\n`，json 形如：
      - {"type":"delta","delta":"..."}
      - {"type":"final","response":{...与 /deepanalyze/chat 相同的结构...}}
    """

    @tornado.web.authenticated
    async def post(self) -> None:
        settings = get_agent_settings()
        if not bool(getattr(settings, "enable_stream", False)):
            logger.info(
                "chat_stream disabled session_id=%s uri=%s",
                str((self.get_json_body() or {}).get("session_id") or "-"),
                getattr(self.request, "uri", "-"),
            )
            self.set_status(409)
            self.set_header("Content-Type", "application/json")
            self.finish(json.dumps({"reply": "未启用流式（DEEPANALYZE_ENABLE_STREAM=false）"}, ensure_ascii=False))
            return

        payload: Dict[str, Any] = self.get_json_body() or {}
        message = str(payload.get("message", "") or "").strip()
        session_id = str(payload.get("session_id") or payload.get("sessionId") or "").strip()
        model_id = _extract_model_id(payload)
        prompt_lang = _extract_prompt_lang(payload)

        tool = DeepAnalyzeNotebookTool(
            contents_manager=self.contents_manager,
            kernel_manager=self.kernel_manager,
            state={},
        )

        context = payload.get("context") or {}
        if isinstance(context, dict):
            tool.set_active_context(
                workspace_dir=context.get("workspaceDir") or context.get("workspace_dir"),
                output_path=context.get("outputPath") or context.get("output_path"),
                scratch_path=context.get("scratchPath") or context.get("scratch_path"),
            )

        logger.info(
            "chat_stream start session_id=%s model_id=%s uri=%s msg_len=%s",
            session_id or "-",
            model_id or "-",
            getattr(self.request, "uri", "-"),
            len(message),
        )

        self.set_header("Content-Type", "text/event-stream; charset=utf-8")
        self.set_header("Cache-Control", "no-cache")
        self.set_header("Connection", "keep-alive")
        self.set_header("X-Accel-Buffering", "no")

        async def send_event(obj: Dict[str, Any]) -> None:
            try:
                self.write(f"data: {json.dumps(obj, ensure_ascii=False)}\n\n")
                await self.flush()
            except Exception:  # noqa: BLE001
                # 客户端中断/网络异常等
                logger.exception("chat_stream write failed session_id=%s", session_id or "-")
                raise

        await send_event({"type": "start"})

        # 工具模式：不做流式，直接返回一次性结果（保持行为一致）。
        if message.startswith("{") and message.endswith("}"):
            try:
                op_payload = json.loads(message)
                result = await tool.handle_op(op_payload)
                reply = str(result.get("reply") or "")
                await send_event(
                    {
                        "type": "final",
                        "response": {
                            "reply": reply,
                            "data": {**result, "session_id": session_id},
                        },
                    }
                )
                self.finish()
                return
            except Exception as e:  # noqa: BLE001
                await send_event(
                    {
                        "type": "final",
                        "response": {"reply": f"命令解析/执行失败：{e}\n\n{tool.to_help_text()}"},
                    }
                )
                self.finish()
                return

        if message in ("/help", "help", "/da", "/da help"):
            await send_event({"type": "final", "response": {"reply": tool.to_help_text()}})
            self.finish()
            return

        if message in ("/reset", "reset"):
            effective_settings, _spec = _apply_model_to_settings(
                settings,
                model_id=(model_id or getattr(settings, "active_model_id", "")),
                prompt_lang=prompt_lang,
            )
            if session_id:
                get_session_store().reset(
                    _session_key(session_id, effective_settings.active_model_id, prompt_lang)
                )
            await send_event({"type": "final", "response": {"reply": "已重置当前会话。"}})
            self.finish()
            return

        ctx = tool.active_context()
        workspace_dir = str(ctx.get("workspace_dir") or "").strip()
        output_path = str(ctx.get("output_path") or "").strip()
        scratch_path = str(ctx.get("scratch_path") or "").strip()

        if not (workspace_dir and output_path and scratch_path and message and session_id):
            await send_event(
                {
                    "type": "final",
                    "response": {
                        "reply": "缺少工作区上下文或 session_id（请先进入 DeepAnalyze 工作区再对话）。"
                    },
                }
            )
            self.finish()
            return

        effective_settings, _spec = _apply_model_to_settings(
            settings,
            model_id=(model_id or getattr(settings, "active_model_id", "")),
            prompt_lang=prompt_lang,
        )
        store_key = _session_key(session_id, effective_settings.active_model_id, prompt_lang)
        session = get_session_store().get_or_create(store_key)
        delta_count = 0
        delta_chars = 0

        async def on_delta(delta: str) -> None:
            nonlocal delta_count, delta_chars
            d = str(delta or "")
            if not d:
                return
            delta_count += 1
            delta_chars += len(d)
            if delta_count <= 3:
                logger.info(
                    "chat_stream delta session_id=%s n=%s delta_len=%s",
                    store_key,
                    delta_count,
                    len(d),
                )
            await send_event({"type": "delta", "delta": d})

        try:
            data = await handle_user_message(
                session=session,
                session_id=store_key,
                settings=effective_settings,
                contents_manager=self.contents_manager,
                workspace_dir=workspace_dir,
                notebook_paths=NotebookPaths(output_path=output_path, scratch_path=scratch_path),
                user_message=message,
                on_stream_delta=on_delta,
            )
            reply = str(data.get("reply") or "")
            await send_event({"type": "final", "response": {"reply": reply, "data": data}})
        except Exception as e:  # noqa: BLE001
            logger.exception("chat_stream failed session_id=%s", session_id)
            await send_event({"type": "final", "response": {"reply": f"调用模型失败：{e}"}})
        finally:
            logger.info(
                "chat_stream end session_id=%s model_id=%s delta_count=%s delta_chars=%s",
                store_key,
                effective_settings.active_model_id,
                delta_count,
                delta_chars,
            )
            self.finish()


class FeedbackHandler(APIHandler):
    @tornado.web.authenticated
    async def post(self) -> None:
        payload: Dict[str, Any] = self.get_json_body() or {}
        session_id = str(payload.get("session_id") or payload.get("sessionId") or "").strip()
        model_id = _extract_model_id(payload)
        prompt_lang = _extract_prompt_lang(payload)
        if not session_id:
            self.set_status(400)
            self.finish(json.dumps({"reply": "缺少 session_id"}, ensure_ascii=False))
            return

        tool_results = payload.get("tool_results") or payload.get("toolResults") or []
        if not isinstance(tool_results, list):
            tool_results = []
        execute_text = str(payload.get("execute_text") or payload.get("executeText") or "").strip()

        # context 用于定位工作区路径
        context = payload.get("context") or {}
        workspace_dir = str(
            (context.get("workspaceDir") or context.get("workspace_dir") or "")
        ).strip()
        output_path = str((context.get("outputPath") or context.get("output_path") or "")).strip()
        scratch_path = str(
            (context.get("scratchPath") or context.get("scratch_path") or "")
        ).strip()

        if not (workspace_dir and output_path and scratch_path):
            self.set_status(400)
            self.finish(json.dumps({"reply": "缺少 context（workspace/output/scratch）"}, ensure_ascii=False))
            return

        settings = get_agent_settings()
        effective_settings, _spec = _apply_model_to_settings(
            settings,
            model_id=(model_id or getattr(settings, "active_model_id", "")),
            prompt_lang=prompt_lang,
        )
        store_key = _session_key(session_id, effective_settings.active_model_id, prompt_lang)
        session = get_session_store().get_or_create(store_key)
        logger.info(
            "feedback start session_id=%s model_id=%s tool_results=%s execute_len=%s",
            store_key,
            effective_settings.active_model_id,
            len(tool_results),
            len(execute_text),
        )
        data = await handle_feedback(
            session=session,
            session_id=store_key,
            settings=effective_settings,
            contents_manager=self.contents_manager,
            workspace_dir=workspace_dir,
            notebook_paths=NotebookPaths(output_path=output_path, scratch_path=scratch_path),
            tool_results=[it for it in tool_results if isinstance(it, dict)],
            execute_text=execute_text,
        )

        reply = str(data.get("reply") or "")
        logger.info(
            "feedback ok session_id=%s await_feedback=%s ops=%s",
            store_key,
            bool(data.get("await_feedback")),
            len(data.get("frontend_ops") or []),
        )
        self.set_header("Content-Type", "application/json")
        self.finish(json.dumps({"reply": reply, "data": data}, ensure_ascii=False))


class FeedbackStreamHandler(APIHandler):
    """
    流式 feedback：与 `ChatStreamHandler` 相同协议，用于执行回环后的续写。
    """

    @tornado.web.authenticated
    async def post(self) -> None:
        settings = get_agent_settings()
        if not bool(getattr(settings, "enable_stream", False)):
            logger.info(
                "feedback_stream disabled uri=%s",
                getattr(self.request, "uri", "-"),
            )
            self.set_status(409)
            self.set_header("Content-Type", "application/json")
            self.finish(json.dumps({"reply": "未启用流式（DEEPANALYZE_ENABLE_STREAM=false）"}, ensure_ascii=False))
            return

        payload: Dict[str, Any] = self.get_json_body() or {}
        session_id = str(payload.get("session_id") or payload.get("sessionId") or "").strip()
        model_id = _extract_model_id(payload)
        prompt_lang = _extract_prompt_lang(payload)
        if not session_id:
            self.set_status(400)
            self.set_header("Content-Type", "application/json")
            self.finish(json.dumps({"reply": "缺少 session_id"}, ensure_ascii=False))
            return

        tool_results = payload.get("tool_results") or payload.get("toolResults") or []
        if not isinstance(tool_results, list):
            tool_results = []
        execute_text = str(payload.get("execute_text") or payload.get("executeText") or "").strip()

        context = payload.get("context") or {}
        workspace_dir = str(
            (context.get("workspaceDir") or context.get("workspace_dir") or "")
        ).strip()
        output_path = str((context.get("outputPath") or context.get("output_path") or "")).strip()
        scratch_path = str(
            (context.get("scratchPath") or context.get("scratch_path") or "")
        ).strip()

        if not (workspace_dir and output_path and scratch_path):
            self.set_status(400)
            self.set_header("Content-Type", "application/json")
            self.finish(json.dumps({"reply": "缺少 context（workspace/output/scratch）"}, ensure_ascii=False))
            return

        logger.info(
            "feedback_stream start session_id=%s model_id=%s uri=%s tool_results=%s execute_len=%s",
            session_id,
            model_id or "-",
            getattr(self.request, "uri", "-"),
            len(tool_results),
            len(execute_text),
        )

        self.set_header("Content-Type", "text/event-stream; charset=utf-8")
        self.set_header("Cache-Control", "no-cache")
        self.set_header("Connection", "keep-alive")
        self.set_header("X-Accel-Buffering", "no")

        async def send_event(obj: Dict[str, Any]) -> None:
            try:
                self.write(f"data: {json.dumps(obj, ensure_ascii=False)}\n\n")
                await self.flush()
            except Exception:  # noqa: BLE001
                logger.exception("feedback_stream write failed session_id=%s", session_id)
                raise

        await send_event({"type": "start"})

        effective_settings, _spec = _apply_model_to_settings(
            settings,
            model_id=(model_id or getattr(settings, "active_model_id", "")),
            prompt_lang=prompt_lang,
        )
        store_key = _session_key(session_id, effective_settings.active_model_id, prompt_lang)
        session = get_session_store().get_or_create(store_key)
        delta_count = 0
        delta_chars = 0

        async def on_delta(delta: str) -> None:
            nonlocal delta_count, delta_chars
            d = str(delta or "")
            if not d:
                return
            delta_count += 1
            delta_chars += len(d)
            if delta_count <= 3:
                logger.info(
                    "feedback_stream delta session_id=%s n=%s delta_len=%s",
                    store_key,
                    delta_count,
                    len(d),
                )
            await send_event({"type": "delta", "delta": d})

        try:
            data = await handle_feedback(
                session=session,
                session_id=store_key,
                settings=effective_settings,
                contents_manager=self.contents_manager,
                workspace_dir=workspace_dir,
                notebook_paths=NotebookPaths(output_path=output_path, scratch_path=scratch_path),
                tool_results=[it for it in tool_results if isinstance(it, dict)],
                execute_text=execute_text,
                on_stream_delta=on_delta,
            )
            reply = str(data.get("reply") or "")
            await send_event({"type": "final", "response": {"reply": reply, "data": data}})
        except Exception as e:  # noqa: BLE001
            logger.exception("feedback_stream failed session_id=%s", store_key)
            await send_event({"type": "final", "response": {"reply": f"feedback 失败：{e}"}})
        finally:
            logger.info(
                "feedback_stream end session_id=%s model_id=%s delta_count=%s delta_chars=%s",
                store_key,
                effective_settings.active_model_id,
                delta_count,
                delta_chars,
            )
            self.finish()


class ModelsHandler(APIHandler):
    """
    前端模型选择器的数据源：
    - 返回模型列表
    - 返回每个模型的 api_key 状态（ok/missing/invalid）
    """

    @tornado.web.authenticated
    async def get(self) -> None:
        settings = get_agent_settings()
        specs = load_model_specs(settings=settings)
        default_id = get_default_model_id(settings=settings)

        models: List[Dict[str, Any]] = []
        for spec in specs:
            key_status = get_api_key_status(spec.id, requires_api_key=bool(spec.requires_api_key))
            models.append({**spec.to_public_dict(), "api_key_status": key_status.to_public_dict()})

        self.set_header("Content-Type", "application/json")
        self.finish(json.dumps({"default_model_id": default_id, "models": models}, ensure_ascii=False))


class ModelApiKeyHandler(APIHandler):
    """
    设置/校验某个模型的 api_key。
    """

    @tornado.web.authenticated
    async def post(self) -> None:
        payload: Dict[str, Any] = self.get_json_body() or {}
        model_id = _extract_model_id(payload)
        api_key = str(payload.get("api_key") or payload.get("apiKey") or "").strip()

        settings = get_agent_settings()
        spec = resolve_model_spec(settings=settings, model_id=model_id)
        if not bool(spec.requires_api_key):
            self.set_status(400)
            self.set_header("Content-Type", "application/json")
            self.finish(json.dumps({"reply": "该模型不需要 api_key"}, ensure_ascii=False))
            return

        status = await set_and_validate_api_key(spec=spec, api_key=api_key, timeout_s=10.0)
        self.set_header("Content-Type", "application/json")
        self.finish(json.dumps({"api_key_status": status.to_public_dict()}, ensure_ascii=False))


class ModelUpsertHandler(APIHandler):
    """
    创建/更新模型配置（用于前端“齿轮设置”与“添加自定义模型”）。

    说明：
    - 不会在 GET 列表时返回 api_key；
    - 若提交了 api_key，则会写入并进行一次校验。
    """

    @tornado.web.authenticated
    async def post(self) -> None:
        payload: Dict[str, Any] = self.get_json_body() or {}
        raw_id = _extract_model_id(payload)
        label = str(payload.get("label") or payload.get("name") or "").strip()
        base_url = str(payload.get("base_url") or payload.get("baseUrl") or "").strip()
        model_name = str(payload.get("model") or payload.get("model_name") or payload.get("modelName") or "").strip()
        api_key = str(payload.get("api_key") or payload.get("apiKey") or "").strip()
        temperature_raw = payload.get("temperature")

        settings = get_agent_settings()

        # 判断是“更新已有模型”还是“新增自定义模型”
        if raw_id:
            spec = resolve_model_spec(settings=settings, model_id=raw_id)
            model_id = spec.id
            is_custom = bool(getattr(spec, "is_custom", False))
        else:
            if not label:
                self.set_status(400)
                self.set_header("Content-Type", "application/json")
                self.finish(json.dumps({"reply": "新增自定义模型需要 label"}, ensure_ascii=False))
                return
            model_id = generate_custom_model_id(label)
            # 新增默认为 OpenAI-Compatible
            spec = resolve_model_spec(settings=settings, model_id="openai")
            is_custom = True

        backend = str(getattr(spec, "backend", "") or "openai_compat").strip().lower()
        prompt_name = str(getattr(spec, "prompt_name", "") or "universal_llm").strip().lower()
        requires_api_key = bool(getattr(spec, "requires_api_key", True))

        # 校验/清洗参数
        if backend != "vllm":
            if not base_url:
                self.set_status(400)
                self.set_header("Content-Type", "application/json")
                self.finish(json.dumps({"reply": "base_url 不能为空"}, ensure_ascii=False))
                return
            if not model_name:
                self.set_status(400)
                self.set_header("Content-Type", "application/json")
                self.finish(json.dumps({"reply": "model 不能为空"}, ensure_ascii=False))
                return

        try:
            temperature = float(temperature_raw) if temperature_raw is not None else float(getattr(spec, "temperature", 0.4) or 0.4)
        except Exception:  # noqa: BLE001
            temperature = float(getattr(spec, "temperature", 0.4) or 0.4)
        # 简单约束范围
        if temperature < 0.0:
            temperature = 0.0
        if temperature > 2.0:
            temperature = 2.0

        record = upsert_model(
            model_id=model_id,
            label=label or getattr(spec, "label", model_id),
            backend=backend,
            base_url=base_url or getattr(spec, "base_url", ""),
            model=model_name or getattr(spec, "model", ""),
            temperature=temperature,
            prompt_name=prompt_name,
            requires_api_key=requires_api_key,
            is_custom=is_custom,
        )

        # 重新解析一次 spec（包含最新 override）
        updated_spec = resolve_model_spec(settings=settings, model_id=model_id)

        # 若提交了 api_key，则立即写入并校验；否则保持现状（但 base_url 变化可能会使旧 key 失效，交给用户重新校验）
        key_status = get_api_key_status(updated_spec.id, requires_api_key=bool(updated_spec.requires_api_key))
        if api_key and bool(updated_spec.requires_api_key):
            key_status = await set_and_validate_api_key(spec=updated_spec, api_key=api_key, timeout_s=10.0)
        else:
            # 若存在已保存 key 且用户更新了 base_url，可尝试快速重验一次，避免“绿点但实际不可用”
            existing_key = get_api_key(updated_spec.id)
            if existing_key and bool(updated_spec.requires_api_key):
                key_status = await set_and_validate_api_key(
                    spec=updated_spec, api_key=existing_key, timeout_s=8.0
                )

        self.set_header("Content-Type", "application/json")
        self.finish(
            json.dumps(
                {"model": {**updated_spec.to_public_dict(), "api_key_status": key_status.to_public_dict()}},
                ensure_ascii=False,
            )
        )


class CellRewriteHandler(APIHandler):
    @tornado.web.authenticated
    async def post(self) -> None:
        payload: Dict[str, Any] = self.get_json_body() or {}
        source = str(payload.get("source") or "").rstrip()
        instruction = str(payload.get("instruction") or "").strip()
        cell_type = str(payload.get("cell_type") or "").strip()
        execution_result = str(payload.get("execution_result") or "").rstrip()
        model_id = _extract_model_id(payload)

        if not instruction:
            self.set_status(400)
            self.set_header("Content-Type", "application/json")
            self.finish(json.dumps({"answer": "", "raw": "", "error": "缺少 instruction"}, ensure_ascii=False))
            return

        prompt = "**按要求修改这部分内容：**\n"
        prompt += f"{source}\n"
        if execution_result and (cell_type == "code" or not cell_type):
            prompt += "\n**该单元格最近一次运行的输出/错误信息（供参考）：**\n"
            prompt += f"```text\n{execution_result}\n```\n"
        prompt += f"**要求：** {instruction}\n\n"
        prompt += "**你修改完成后，将修改后的全部内容返回给我，除此之外不要额外说任何东西。**\n"

        settings = get_agent_settings()
        effective_settings, _spec = _apply_model_to_settings(
            settings, model_id=(model_id or getattr(settings, "active_model_id", ""))
        )
        resp = await chat_completions(
            settings=effective_settings,
            messages=[{"role": "user", "content": prompt}],
            temperature=float(getattr(effective_settings, "llm_temperature", 0.4)),
        )

        raw = str(resp.content or "").strip()
        answer = extract_answer_text(raw) or raw
        answer = _clean_cell_rewrite_answer(answer)

        self.set_header("Content-Type", "application/json")
        self.finish(json.dumps({"answer": answer, "raw": raw}, ensure_ascii=False))


class CellRewriteStreamHandler(APIHandler):
    @tornado.web.authenticated
    async def post(self) -> None:
        settings = get_agent_settings()
        if not bool(getattr(settings, "enable_stream", False)):
            self.set_status(409)
            self.set_header("Content-Type", "application/json")
            self.finish(
                json.dumps({"answer": "", "raw": "", "error": "未启用流式（DEEPANALYZE_ENABLE_STREAM=false）"}, ensure_ascii=False)
            )
            return

        payload: Dict[str, Any] = self.get_json_body() or {}
        source = str(payload.get("source") or "").rstrip()
        instruction = str(payload.get("instruction") or "").strip()
        cell_type = str(payload.get("cell_type") or "").strip()
        execution_result = str(payload.get("execution_result") or "").rstrip()
        model_id = _extract_model_id(payload)

        if not instruction:
            self.set_status(400)
            self.set_header("Content-Type", "application/json")
            self.finish(json.dumps({"answer": "", "raw": "", "error": "缺少 instruction"}, ensure_ascii=False))
            return

        prompt = "**按要求修改这部分内容：**\n"
        prompt += f"{source}\n"
        if execution_result and (cell_type == "code" or not cell_type):
            prompt += "\n**该单元格最近一次运行的输出/错误信息（供参考）：**\n"
            prompt += f"```text\n{execution_result}\n```\n"
        prompt += f"**要求：** {instruction}\n\n"
        prompt += "**你修改完成后，将修改后的全部内容返回给我，除此之外不要额外说任何东西。**\n"

        self.set_header("Content-Type", "text/event-stream; charset=utf-8")
        self.set_header("Cache-Control", "no-cache")
        self.set_header("Connection", "keep-alive")
        self.set_header("X-Accel-Buffering", "no")

        async def send_event(obj: Dict[str, Any]) -> None:
            self.write(f"data: {json.dumps(obj, ensure_ascii=False)}\n\n")
            await self.flush()

        await send_event({"type": "start"})

        delta_count = 0
        delta_chars = 0

        async def on_delta(delta: str) -> None:
            nonlocal delta_count, delta_chars
            d = str(delta or "")
            if not d:
                return
            delta_count += 1
            delta_chars += len(d)
            await send_event({"type": "delta", "delta": d})

        try:
            effective_settings, _spec = _apply_model_to_settings(
                settings, model_id=(model_id or getattr(settings, "active_model_id", ""))
            )
            resp = await chat_completions_stream(
                settings=effective_settings,
                messages=[{"role": "user", "content": prompt}],
                on_delta=on_delta,
                temperature=float(getattr(effective_settings, "llm_temperature", 0.4)),
            )
            raw = str(resp.content or "").strip()
            answer = extract_answer_text(raw) or raw
            answer = _clean_cell_rewrite_answer(answer)
            await send_event({"type": "final", "response": {"answer": answer, "raw": raw}})
        except Exception as e:  # noqa: BLE001
            logger.exception("cell_rewrite_stream failed")
            await send_event({"type": "final", "response": {"answer": "", "raw": "", "error": str(e)}})
        finally:
            logger.info(
                "cell_rewrite_stream end delta_count=%s delta_chars=%s",
                delta_count,
                delta_chars,
            )
            self.finish()


class FrontendLogHandler(APIHandler):
    @tornado.web.authenticated
    async def post(self) -> None:
        payload: Dict[str, Any] = self.get_json_body() or {}
        session_id = str(payload.get("session_id") or payload.get("sessionId") or "").strip()
        depth = payload.get("depth")
        await_feedback = payload.get("await_feedback")

        context = payload.get("context") or {}
        workspace_dir = ""
        if isinstance(context, dict):
            workspace_dir = str(
                (context.get("workspaceDir") or context.get("workspace_dir") or "")
            ).strip()

        message = str(payload.get("message") or "").strip()
        logs = str(payload.get("logs") or "").strip()
        tool_results = payload.get("tool_results") or payload.get("toolResults") or []
        if not isinstance(tool_results, list):
            tool_results = []

        def truncate_text(value: str, limit: int = 8000) -> str:
            s = str(value or "")
            if len(s) <= limit:
                return s
            return s[: max(0, limit - 1)] + "…"

        logger.info(
            "frontend_log session_id=%s workspace=%s depth=%s await_feedback=%s msg_len=%s log_len=%s tool_results=%s",
            session_id or "-",
            workspace_dir or "-",
            depth if depth is not None else "-",
            bool(await_feedback) if await_feedback is not None else "-",
            len(message),
            len(logs),
            len(tool_results),
        )

        if message:
            logger.info(
                "frontend_log_message session_id=%s message=%s",
                session_id or "-",
                truncate_text(message, 2000),
            )

        # 注意：避免把模型输出/执行输出等大段内容直接写入日志（泄露风险 + 容易刷屏）。
        # 需要定位问题时可通过 msg_len/log_len/tool_results 数量等统计信息排查。

        self.set_header("Content-Type", "application/json")
        self.finish(json.dumps({"reply": "ok", "ok": True}, ensure_ascii=False))
