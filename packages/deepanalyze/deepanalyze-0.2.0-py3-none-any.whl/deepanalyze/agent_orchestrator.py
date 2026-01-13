from __future__ import annotations

import posixpath
import re
from datetime import datetime
from dataclasses import dataclass
from typing import Any, Awaitable, Callable, Dict, List, Optional, Tuple

from .agent_logging import get_deepanalyze_logger
from .agent_frontend_ops import NotebookPaths, build_frontend_ops_from_segments
from .agent_prompt import load_system_prompt
from .agent_prompt_builder import build_user_prompt
from .agent_settings import DeepAnalyzeAgentSettings
from .agent_tag_parser import extract_answer_text, parse_tagged_segments
from .agent_llm_gateway import chat_completions, chat_completions_stream
from .agent_workspace_scanner import list_workspace_files
from .agent_session_store import SessionState

"""
后端编排器（DeepAnalyze 的“大脑”）。

职责概览：
- 维护 session.messages（user/assistant/execute），保证多轮对话与回环可持续。
- 构造 prompt：system prompt + user prompt（含 # Data 文件列表）。
- 调用 LLM（当前默认为 vLLM OpenAI-compatible）。
- 解析模型输出的标签段落（Analyze/Understand/Code/Answer）。
- 将标签段落映射为前端可执行的 `frontend_ops`，由前端写入/执行 notebook。

返回给前端的核心字段：
- raw: 模型原始输出（含标签）
- frontend_ops: notebook 操作指令列表
- await_feedback: 是否需要执行回环（通常：有 Code 但没有 Answer）
- reply: 用于 Chat 面板展示的最终文本（优先 Answer）
"""

logger = get_deepanalyze_logger("deepanalyze.orchestrator")

_TAG_PATTERN = re.compile(
    r"<(?P<tag>Analyze|Understand|Code|Answer)>(.*?)</(?P=tag)>", re.DOTALL
)


def _new_turn_id() -> str:
    return datetime.utcnow().strftime("%Y%m%d%H%M%S%f")


def _remember_turn(session: SessionState, *, turn_id: str, assistant_index: int) -> None:
    turns = session.meta.setdefault("turns", {})
    if isinstance(turns, dict):
        turns[str(turn_id)] = {"assistant_index": int(assistant_index)}


def _remember_ops(session: SessionState, ops: List[Dict[str, Any]]) -> None:
    op_meta = session.meta.setdefault("op_meta", {})
    if not isinstance(op_meta, dict):
        return
    for op in ops or []:
        op_id = str((op or {}).get("id") or "").strip()
        if not op_id:
            continue
        op_meta[op_id] = {
            "turn_id": (op or {}).get("turn_id"),
            "segment_tag": (op or {}).get("segment_tag"),
            "segment_ordinal": (op or {}).get("segment_ordinal"),
            "segment_kind": (op or {}).get("segment_kind"),
        }


def _resolve_tool_meta(session: SessionState, item: Dict[str, Any]) -> Dict[str, Any]:
    if not isinstance(item, dict):
        return {}
    meta: Dict[str, Any] = {}
    for key in ("turn_id", "segment_tag", "segment_ordinal", "segment_kind"):
        if key in item:
            meta[key] = item.get(key)
    if meta.get("turn_id") and meta.get("segment_tag") is not None and meta.get("segment_ordinal") is not None:
        return meta

    op_id = str(item.get("id") or "").strip()
    if not op_id:
        return meta
    op_meta = session.meta.get("op_meta") if isinstance(session.meta, dict) else None
    if not isinstance(op_meta, dict):
        return meta
    stored = op_meta.get(op_id)
    if isinstance(stored, dict):
        merged = dict(stored)
        merged.update(meta)
        return merged
    return meta


def _strip_markdown_heading(source: str, tag: str) -> str:
    s = str(source or "").strip()
    if not s:
        return ""
    lines = s.splitlines()
    if not lines:
        return ""
    first = lines[0].strip()
    if first.lower() == f"### {str(tag or '').strip().lower()}":
        rest = lines[1:]
        while rest and not rest[0].strip():
            rest = rest[1:]
        return "\n".join(rest).strip()
    return s


def _format_code_for_message(code: str) -> str:
    src = str(code or "").rstrip()
    if not src.strip():
        return ""
    # notebook 的 code cell source 本身就是“纯代码文本”，这里保持一致，不额外包 fenced。
    return src.strip()


def _iter_nonempty_tag_matches(text: str):
    s = str(text or "")
    for m in _TAG_PATTERN.finditer(s):
        inner = str(m.group(2) or "").strip()
        if not inner:
            continue
        yield m


def _overwrite_assistant_segment(
    session: SessionState, *, turn_id: str, segment_ordinal: int, new_inner: str
) -> bool:
    tid = str(turn_id or "").strip()
    if not tid:
        return False

    assistant_index: Optional[int] = None
    turns = session.meta.get("turns") if isinstance(session.meta, dict) else None
    if isinstance(turns, dict):
        info = turns.get(tid)
        if isinstance(info, dict) and isinstance(info.get("assistant_index"), int):
            assistant_index = int(info["assistant_index"])

    if assistant_index is None or assistant_index < 0 or assistant_index >= len(session.messages):
        # 兜底：从后往前找
        for i in range(len(session.messages) - 1, -1, -1):
            msg = session.messages[i]
            if msg.get("role") == "assistant" and str(msg.get("_turn_id") or "") == tid:
                assistant_index = i
                break

    if assistant_index is None:
        return False

    msg = session.messages[assistant_index]
    content = str(msg.get("content") or "")
    target = int(segment_ordinal)
    for i, m in enumerate(_iter_nonempty_tag_matches(content)):
        if i != target:
            continue
        inner = str(new_inner or "").strip()
        msg["content"] = content[: m.start(2)] + "\n" + inner + "\n" + content[m.end(2) :]
        return True
    return False


def _upsert_execute_message(
    session: SessionState, *, turn_id: str, segment_ordinal: int, exe_output: str
) -> bool:
    tid = str(turn_id or "").strip()
    out = str(exe_output or "").strip()
    if not tid or not out:
        return False

    ordinal = int(segment_ordinal)
    for i in range(len(session.messages) - 1, -1, -1):
        msg = session.messages[i]
        if msg.get("role") != "execute":
            continue
        if str(msg.get("_turn_id") or "") != tid:
            continue
        if int(msg.get("_segment_ordinal") or -1) != ordinal:
            continue
        msg["content"] = out
        return True

    session.messages.append(
        {
            "role": "execute",
            "content": out,
            "_turn_id": tid,
            "_segment_ordinal": ordinal,
        }
    )
    return True


def _limit_messages(messages: List[Dict[str, str]], *, keep_last: int = 24) -> List[Dict[str, str]]:
    if keep_last <= 0:
        return messages[:]
    if len(messages) <= keep_last:
        return messages[:]
    # 保留 system + 最近 keep_last-1 条
    head: List[Dict[str, str]] = []
    if messages and messages[0].get("role") == "system":
        head = [messages[0]]
        tail = messages[-(keep_last - 1) :]
        return head + tail
    return messages[-keep_last:]


def _has_tag(segments: List[Any], tag: str) -> bool:
    for seg in segments:
        if getattr(seg, "tag", None) == tag:
            return True
    return False


def _ensure_system_prompt(session: SessionState, settings: DeepAnalyzeAgentSettings) -> None:
    """
    确保会话 messages 以 system prompt 开头。

    说明：
    - 仅在当前会话还没有 system 消息时注入，避免中途切换 prompt 影响上下文一致性。
    """

    if session.messages and session.messages[0].get("role") == "system":
        return
    session.messages.insert(0, {"role": "system", "content": load_system_prompt(settings)})


def _build_execute_text(tool_results: List[Dict[str, Any]]) -> str:
    parts: List[str] = []
    for item in tool_results:
        if str(item.get("op") or "") not in {"run_cell", "run_last_cell"}:
            continue
        text = str(item.get("text") or "").strip()
        if text:
            parts.append(text)
    return "\n\n".join(parts).strip()


@dataclass(frozen=True)
class ScratchCodeSnapshot:
    source: str
    outputs_text: str


def _extract_scratch_code_snapshot(
    tool_results: List[Dict[str, Any]],
    *,
    scratch_path: str,
) -> Optional[ScratchCodeSnapshot]:
    scratch = str(scratch_path or "").strip()
    if not scratch:
        return None

    # 优先取最新一次“运行”得到的 source/outputs（最接近用户点击继续时的实际状态）。
    for item in reversed(tool_results or []):
        if str(item.get("path") or "").strip() != scratch:
            continue
        if str(item.get("op") or "").strip() not in {"run_cell", "run_last_cell"}:
            continue
        source = str(item.get("source") or "").rstrip()
        outputs_text = str(item.get("text") or "").rstrip()
        if source.strip():
            return ScratchCodeSnapshot(source=source, outputs_text=outputs_text)

    # 兜底：若没有 run_*，则尝试从最近一次 insert/update 获取 source。
    for item in reversed(tool_results or []):
        if str(item.get("path") or "").strip() != scratch:
            continue
        if str(item.get("op") or "").strip() not in {"insert_cell", "update_cell"}:
            continue
        source = str(item.get("source") or "").rstrip()
        if not source.strip():
            continue
        return ScratchCodeSnapshot(source=source, outputs_text="")

    return None


def _format_code_segment(snapshot: ScratchCodeSnapshot) -> str:
    parts: List[str] = []
    parts.append("```python")
    parts.append(snapshot.source.rstrip())
    parts.append("```")
    if snapshot.outputs_text.strip():
        parts.append("")
        parts.append("### outputs")
        parts.append(snapshot.outputs_text.rstrip())
    return "\n".join(parts).strip()


def _sync_last_assistant_code_from_scratch(
    session: SessionState, snapshot: ScratchCodeSnapshot
) -> bool:
    """
    以 scratch notebook 为准：若用户修改了 code cell，则把“最近一条带 <Code> 的 assistant 消息”
    中的 <Code> 内容更新为当前 code/outputs。

    说明：只更新 content，不新增/删除 messages，也不改 role。
    """

    for i in range(len(session.messages) - 1, -1, -1):
        msg = session.messages[i]
        if msg.get("role") != "assistant":
            continue
        content = str(msg.get("content") or "")
        if "<Code>" not in content:
            continue

        segments = parse_tagged_segments(content)
        if not segments:
            continue

        rebuilt: List[str] = []
        for seg in segments:
            if seg.tag == "Code":
                rebuilt.append(f"<Code>\n{_format_code_segment(snapshot)}\n</Code>")
                continue
            rebuilt.append(f"<{seg.tag}>\n{seg.content}\n</{seg.tag}>")

        msg["content"] = "\n\n".join(rebuilt).strip()
        return True

    return False


def _conversation_slice_for_latest_user(session: SessionState) -> List[Dict[str, str]]:
    last_user_index: Optional[int] = None
    for i in range(len(session.messages) - 1, -1, -1):
        if session.messages[i].get("role") == "user":
            last_user_index = i
            break
    if last_user_index is None:
        return [m for m in session.messages if m.get("role") != "system"]
    return session.messages[last_user_index:]


def _render_history_markdown(messages: List[Dict[str, str]], *, session_id: str) -> str:
    saved_at = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    lines: List[str] = []
    lines.append("# DeepAnalyze 历史")
    lines.append(f"- session_id: {session_id}")
    lines.append(f"- saved_at: {saved_at}")
    lines.append("")

    for msg in messages:
        role = str(msg.get("role") or "").strip() or "unknown"
        content = str(msg.get("content") or "").rstrip()
        if role == "system":
            continue
        title = "User" if role == "user" else "Assistant" if role == "assistant" else role
        lines.append(f"## {title}")
        lines.append("```text")
        lines.append(content)
        lines.append("```")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def _as_dict(value: Any) -> Dict[str, Any]:
    if value is None:
        return {}
    if isinstance(value, dict):
        return value
    if hasattr(value, "model_dump"):
        return value.model_dump()  # type: ignore[no-any-return]
    if hasattr(value, "to_dict"):
        return value.to_dict()  # type: ignore[no-any-return]
    if hasattr(value, "__dict__"):
        return dict(value.__dict__)
    try:
        return dict(value)  # type: ignore[arg-type]
    except Exception:  # noqa: BLE001
        return {"value": value}


async def _maybe_await(value: Any) -> Any:
    if hasattr(value, "__await__"):
        return await value
    return value


async def _cm_get(contents_manager: Any, path: str, *, content: bool) -> Dict[str, Any]:
    return _as_dict(await _maybe_await(contents_manager.get(path, content=content)))


async def _cm_save(contents_manager: Any, model: Dict[str, Any], path: str) -> Dict[str, Any]:
    return _as_dict(await _maybe_await(contents_manager.save(model, path)))


async def _cm_new_untitled(contents_manager: Any, *, path: str, type: str) -> Dict[str, Any]:
    return _as_dict(await _maybe_await(contents_manager.new_untitled(path=path, type=type)))


async def _cm_rename(contents_manager: Any, old_path: str, new_path: str) -> Dict[str, Any]:
    return _as_dict(await _maybe_await(contents_manager.rename(old_path, new_path)))


async def _ensure_directory(contents_manager: Any, path: str) -> None:
    p = str(path or "").lstrip("/").strip()
    if not p or p == ".":
        return
    try:
        model = await _cm_get(contents_manager, p, content=False)
        if model.get("type") == "directory":
            return
    except Exception:  # noqa: BLE001
        pass

    parent = posixpath.dirname(p)
    name = posixpath.basename(p)
    if parent and parent != ".":
        await _ensure_directory(contents_manager, parent)
    else:
        parent = ""

    tmp = await _cm_new_untitled(contents_manager, path=parent, type="directory")
    await _cm_rename(contents_manager, tmp.get("path") or "", posixpath.join(parent, name))


async def _persist_history_if_answer(
    *,
    contents_manager: Any,
    workspace_dir: str,
    session_id: str,
    messages: List[Dict[str, str]],
    has_answer: bool,
) -> None:
    if not has_answer:
        return
    ws = str(workspace_dir or "").strip().strip("/")
    if not ws:
        return

    history_dir = posixpath.join(ws, "history")
    try:
        await _ensure_directory(contents_manager, history_dir)
    except Exception:  # noqa: BLE001
        logger.exception("history ensure_directory failed session_id=%s dir=%s", session_id, history_dir)
        return

    ts = datetime.utcnow().strftime("%Y%m%d-%H%M%S")
    sid = (session_id or "anonymous").strip()
    sid_short = sid[:8] if sid else "anonymous"
    filename = f"{ts}-{sid_short}.md"
    target = posixpath.join(history_dir, filename)

    # 简单避免覆盖：若存在则加后缀递增。
    for i in range(0, 20):
        candidate = target if i == 0 else posixpath.join(history_dir, f"{ts}-{sid_short}-{i}.md")
        try:
            await _cm_get(contents_manager, candidate, content=False)
            continue
        except Exception:  # noqa: BLE001
            target = candidate
            break

    text = _render_history_markdown(messages, session_id=sid)
    try:
        await _cm_save(
            contents_manager,
            {"type": "file", "format": "text", "content": text},
            target,
        )
        logger.info("history saved session_id=%s path=%s", sid or "-", target)
    except Exception:  # noqa: BLE001
        logger.exception("history save failed session_id=%s path=%s", sid or "-", target)


async def handle_user_message(
    *,
    session: SessionState,
    session_id: str,
    settings: DeepAnalyzeAgentSettings,
    contents_manager: Any,
    workspace_dir: str,
    notebook_paths: NotebookPaths,
    user_message: str,
    on_stream_delta: Optional[Callable[[str], Awaitable[None]]] = None,
) -> Dict[str, Any]:
    """
    处理用户消息（第一跳）：构造上下文 -> 调用 LLM -> 解析标签 -> 生成 frontend_ops。

    说明：
    - 若开启流式（settings.enable_stream=true 且传入 on_stream_delta），会边生成边回调 delta；
      但最终仍会在结束时返回完整结构（raw/frontend_ops/await_feedback/reply）。
    - frontend_ops 只描述“前端应当如何写 notebook”，后端不直接改 ipynb 文件。
    """

    _ensure_system_prompt(session, settings)
    data_block, files = await list_workspace_files(
        contents_manager=contents_manager,
        workspace_dir=workspace_dir,
        settings=settings,
    )

    session.messages.append(
        {
            "role": "user",
            "content": build_user_prompt(user_message=user_message, data_block=data_block),
        }
    )

    vllm_messages = _limit_messages(session.messages)
    logger.info(
        "vllm request session_id=%s messages=%s data_files=%s",
        session_id,
        len(vllm_messages),
        len(files),
    )
    if settings.enable_stream and on_stream_delta is not None:
        response = await chat_completions_stream(
            settings=settings,
            messages=vllm_messages,
            on_delta=on_stream_delta,
            timeout_s=settings.vllm_timeout_s,
            temperature=float(getattr(settings, "llm_temperature", 0.4)),
            add_generation_prompt=settings.vllm_add_generation_prompt,
            stop_token_ids=settings.vllm_stop_token_ids,
            max_new_tokens=settings.vllm_max_new_tokens,
        )
    else:
        response = await chat_completions(
            settings=settings,
            messages=vllm_messages,
            timeout_s=settings.vllm_timeout_s,
            temperature=float(getattr(settings, "llm_temperature", 0.4)),
            add_generation_prompt=settings.vllm_add_generation_prompt,
            stop_token_ids=settings.vllm_stop_token_ids,
            max_new_tokens=settings.vllm_max_new_tokens,
        )

    turn_id = _new_turn_id()
    session.messages.append({"role": "assistant", "content": response.content, "_turn_id": turn_id})

    segments = parse_tagged_segments(response.content)
    ops = build_frontend_ops_from_segments(
        segments=segments,
        paths=notebook_paths,
        include_run_after_code=True,
        turn_id=turn_id,
    )
    _remember_turn(session, turn_id=turn_id, assistant_index=len(session.messages) - 1)
    _remember_ops(session, ops)

    answer_text = extract_answer_text(response.content)
    await_feedback = _has_tag(segments, "Code") and not _has_tag(segments, "Answer")
    has_answer = _has_tag(segments, "Answer")
    await _persist_history_if_answer(
        contents_manager=contents_manager,
        workspace_dir=workspace_dir,
        session_id=session_id,
        messages=_conversation_slice_for_latest_user(session),
        has_answer=has_answer,
    )
    logger.info(
        "vllm response session_id=%s segments=%s await_feedback=%s ops=%s",
        session_id,
        len(segments),
        await_feedback,
        len(ops),
    )

    return {
        "ok": True,
        "session_id": session_id,
        "vllm_model": settings.vllm_model,
        "data_block": data_block,
        "files": files,
        "raw": response.content,
        "frontend_ops": ops,
        "await_feedback": await_feedback,
        "reply": answer_text or response.content or "(empty)",
    }


async def handle_feedback(
    *,
    session: SessionState,
    session_id: str,
    settings: DeepAnalyzeAgentSettings,
    contents_manager: Any,
    workspace_dir: str,
    notebook_paths: NotebookPaths,
    tool_results: List[Dict[str, Any]],
    execute_text: str,
    on_stream_delta: Optional[Callable[[str], Awaitable[None]]] = None,
) -> Dict[str, Any]:
    """
    处理回环（第二跳及以后）：消费前端的执行结果 -> 追加/覆写上下文 -> 再次调用 LLM。

    输入：
    - tool_results: 前端执行 frontend_ops 的结果（含 cell source、输出摘要、meta 等）
    - execute_text: 前端汇总后的“快照文本”（用于保证本轮一定有可喂给模型的新增上下文）
    """

    _ensure_system_prompt(session, settings)
    data_block, files = await list_workspace_files(
        contents_manager=contents_manager,
        workspace_dir=workspace_dir,
        settings=settings,
    )

    payload_text = (execute_text or "").strip() or _build_execute_text(tool_results)
    if not payload_text:
        payload_text = "(empty execute output)"

    # 0) 确保本轮 feedback 一定会产生“可喂给模型”的 execute message。
    #    说明：前端传来的 execute_text 是“当前 notebook 快照”（含 cell source 与输出摘要），
    #    若仅靠 run_cell/run_last_cell 的输出摘要，遇到 display_data（图像等）可能为空，
    #    从而导致本轮没有新增上下文，部分 vLLM 兼容实现会返回空内容。
    feedback_turn_id = ""
    feedback_ordinal: Optional[int] = None
    for item in tool_results or []:
        if not isinstance(item, dict):
            continue
        meta = _resolve_tool_meta(session, item)
        if str(meta.get("segment_tag") or "").strip() != "Code":
            continue
        if str(meta.get("segment_kind") or "").strip() != "code":
            continue
        feedback_turn_id = str(meta.get("turn_id") or "").strip()
        try:
            feedback_ordinal = int(meta.get("segment_ordinal"))
        except Exception:  # noqa: BLE001
            feedback_ordinal = None
        if feedback_turn_id and feedback_ordinal is not None:
            break

    if feedback_turn_id and feedback_ordinal is not None:
        _upsert_execute_message(
            session,
            turn_id=feedback_turn_id,
            segment_ordinal=feedback_ordinal,
            exe_output=payload_text,
        )

    # 1) 以 notebook 当前可见内容为准：覆写本轮 assistant message 中对应的代码块/markdown 块。
    for item in tool_results or []:
        if not isinstance(item, dict):
            continue
        meta = _resolve_tool_meta(session, item)
        turn_id = str(meta.get("turn_id") or "").strip()
        seg_tag = str(meta.get("segment_tag") or "").strip()
        seg_kind = str(meta.get("segment_kind") or "").strip()
        try:
            seg_ordinal = int(meta.get("segment_ordinal"))
        except Exception:  # noqa: BLE001
            continue

        src = str(item.get("source") or "").rstrip()
        if not src.strip():
            continue

        if seg_kind == "markdown" and seg_tag in {"Analyze", "Understand", "Answer"}:
            _overwrite_assistant_segment(
                session,
                turn_id=turn_id,
                segment_ordinal=seg_ordinal,
                new_inner=_strip_markdown_heading(src, seg_tag),
            )
            continue

        if seg_kind == "code" and seg_tag == "Code":
            _overwrite_assistant_segment(
                session,
                turn_id=turn_id,
                segment_ordinal=seg_ordinal,
                new_inner=_format_code_for_message(src),
            )
            continue

    # 2) code cell 的执行输出：追加/覆写 role=execute 的 message（用于下一轮 vLLM 上下文）。
    for item in tool_results or []:
        if not isinstance(item, dict):
            continue
        if str(item.get("op") or "") not in {"run_cell", "run_last_cell"}:
            continue
        meta = _resolve_tool_meta(session, item)
        seg_tag = str(meta.get("segment_tag") or "").strip()
        seg_kind = str(meta.get("segment_kind") or "").strip()
        if seg_tag != "Code" or seg_kind != "code":
            continue
        turn_id = str(meta.get("turn_id") or "").strip()
        try:
            seg_ordinal = int(meta.get("segment_ordinal"))
        except Exception:  # noqa: BLE001
            continue

        out = str(item.get("text") or "").strip()
        if not out:
            stdout = str(item.get("stdout") or "").strip()
            result = str(item.get("result") or "").strip()
            out = "\n".join([x for x in (stdout, result) if x]).strip()
        _upsert_execute_message(session, turn_id=turn_id, segment_ordinal=seg_ordinal, exe_output=out)

    vllm_messages = _limit_messages(session.messages)
    logger.info(
        "vllm feedback session_id=%s messages=%s execute_len=%s",
        session_id,
        len(vllm_messages),
        len(payload_text),
    )
    if settings.enable_stream and on_stream_delta is not None:
        response = await chat_completions_stream(
            settings=settings,
            messages=vllm_messages,
            on_delta=on_stream_delta,
            timeout_s=settings.vllm_timeout_s,
            temperature=float(getattr(settings, "llm_temperature", 0.4)),
            add_generation_prompt=settings.vllm_add_generation_prompt,
            stop_token_ids=settings.vllm_stop_token_ids,
            max_new_tokens=settings.vllm_max_new_tokens,
        )
    else:
        response = await chat_completions(
            settings=settings,
            messages=vllm_messages,
            timeout_s=settings.vllm_timeout_s,
            temperature=float(getattr(settings, "llm_temperature", 0.4)),
            add_generation_prompt=settings.vllm_add_generation_prompt,
            stop_token_ids=settings.vllm_stop_token_ids,
            max_new_tokens=settings.vllm_max_new_tokens,
        )

    turn_id = _new_turn_id()
    session.messages.append({"role": "assistant", "content": response.content, "_turn_id": turn_id})

    segments = parse_tagged_segments(response.content)
    ops = build_frontend_ops_from_segments(
        segments=segments,
        paths=notebook_paths,
        include_run_after_code=True,
        turn_id=turn_id,
    )
    _remember_turn(session, turn_id=turn_id, assistant_index=len(session.messages) - 1)
    _remember_ops(session, ops)

    answer_text = extract_answer_text(response.content)
    await_feedback = _has_tag(segments, "Code") and not _has_tag(segments, "Answer")
    has_answer = _has_tag(segments, "Answer")
    await _persist_history_if_answer(
        contents_manager=contents_manager,
        workspace_dir=workspace_dir,
        session_id=session_id,
        messages=_conversation_slice_for_latest_user(session),
        has_answer=has_answer,
    )
    logger.info(
        "vllm feedback response session_id=%s segments=%s await_feedback=%s ops=%s",
        session_id,
        len(segments),
        await_feedback,
        len(ops),
    )

    return {
        "ok": True,
        "session_id": session_id,
        "vllm_model": settings.vllm_model,
        "data_block": data_block,
        "files": files,
        "raw": response.content,
        "frontend_ops": ops,
        "await_feedback": await_feedback,
        "reply": answer_text or response.content or "(empty)",
    }
