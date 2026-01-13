from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Awaitable, Callable, Dict, List, Optional

from .agent_settings import DeepAnalyzeAgentSettings
from .agent_secret_store import get_api_key
from .agent_openai_compat_client import (
    chat_completions as openai_compat_chat_completions,
    chat_completions_stream as openai_compat_chat_completions_stream,
)
from .agent_vllm_client import (
    VllmChatResponse,
    chat_completions as vllm_chat_completions,
    chat_completions_stream as vllm_chat_completions_stream,
)


@dataclass(frozen=True)
class ChatResponse:
    """
    统一的 LLM 响应结构（中间层输出）。

    说明：
    - 当前仍直接透传 vLLM（OpenAI-Compatible）的响应。
    - 后续接入外部大模型 API 时，可在此做字段归一化。
    """

    content: str
    raw: Dict[str, Any]
    backend: str


def _normalize_backend(raw: str) -> str:
    b = str(raw or "").strip().lower()
    return b or "vllm"


def _preprocess_messages(
    *, messages: List[Dict[str, str]], settings: DeepAnalyzeAgentSettings
) -> List[Dict[str, str]]:
    """
    前端 -> 后端 -> LLM 的消息预处理占位。

    当前不做任何修改，以保证行为不变；后续可在这里实现：
    - system prompt 注入/切换
    - 模式选择（工具调用 / 外部 API / 多 agent 等）
    - 额外上下文拼接与安全过滤
    """

    backend = _normalize_backend(getattr(settings, "llm_backend", "vllm"))
    # 仅透传 role/content，避免把内部字段（如 _turn_id 等）传给 OpenAI-compatible 兼容层。
    cleaned: List[Dict[str, str]] = []
    for msg in messages:
        role = str((msg or {}).get("role") or "").strip()
        content = str((msg or {}).get("content") or "")
        if not role:
            continue

        # 外部 OpenAI-compatible API 往往严格校验 role（只允许 system/user/assistant/tool 等）。
        # 本项目内部会注入 role=execute 用于携带 Notebook 执行输出；这里做一次兼容映射。
        normalized_role = role.strip().lower()
        if backend != "vllm":
            if normalized_role == "execute":
                cleaned.append({"role": "user", "content": f"# Execution Result\n{content}".strip()})
                continue
            if normalized_role not in {"system", "user", "assistant", "tool"}:
                cleaned.append({"role": "user", "content": f"# Context\n[{role}]\n{content}".strip()})
                continue

        cleaned.append({"role": role, "content": content})
    return cleaned


def _postprocess_response(
    *, response: Any, settings: DeepAnalyzeAgentSettings, backend: str
) -> ChatResponse:
    """
    LLM -> 后端 -> 前端 的响应后处理占位。

    当前仅透传 content/raw；后续可实现：
    - 内容清洗/截断
    - 结构化提取（如工具调用、引用、token 使用量等）
    """

    _ = settings
    return ChatResponse(content=str(getattr(response, "content", "") or ""), raw=getattr(response, "raw", {}) or {}, backend=backend)


async def chat_completions(
    *,
    settings: DeepAnalyzeAgentSettings,
    messages: List[Dict[str, str]],
    timeout_s: Optional[float] = None,
    temperature: float = 0.4,
    max_tokens: Optional[int] = None,
    add_generation_prompt: bool = False,
    stop_token_ids: Optional[List[int]] = None,
    max_new_tokens: Optional[int] = None,
) -> ChatResponse:
    """
    LLM 中间层：统一对外提供 chat.completions 能力。

    当前默认直连 vLLM（OpenAI-Compatible）以保持功能不变；
    其他后端仅做占位（后续再实现）。
    """

    backend = _normalize_backend(getattr(settings, "llm_backend", "vllm"))
    effective_timeout = float(timeout_s) if timeout_s is not None else float(settings.vllm_timeout_s)

    prepared = _preprocess_messages(messages=messages, settings=settings)

    if backend == "vllm":
        vllm_response = await vllm_chat_completions(
            base_url=settings.vllm_base_url,
            model=settings.vllm_model,
            messages=prepared,
            timeout_s=effective_timeout,
            temperature=temperature,
            max_tokens=max_tokens,
            add_generation_prompt=add_generation_prompt,
            stop_token_ids=stop_token_ids,
            max_new_tokens=max_new_tokens,
        )
        return _postprocess_response(response=vllm_response, settings=settings, backend=backend)

    if backend == "openai_compat":
        api_key = get_api_key(getattr(settings, "active_model_id", "") or "")
        if not str(api_key or "").strip():
            raise RuntimeError("缺少 API Key（请在前端为该模型设置/校验）")
        effective_max_tokens = max_tokens
        if effective_max_tokens is None and max_new_tokens is not None:
            effective_max_tokens = int(max_new_tokens)
        response = await openai_compat_chat_completions(
            base_url=settings.vllm_base_url,
            model=settings.vllm_model,
            messages=prepared,
            api_key=api_key,
            timeout_s=effective_timeout,
            temperature=temperature,
            max_tokens=effective_max_tokens,
        )
        return _postprocess_response(response=response, settings=settings, backend=backend)

    raise NotImplementedError(f"暂不支持的 LLM 后端：{backend}")


async def chat_completions_stream(
    *,
    settings: DeepAnalyzeAgentSettings,
    messages: List[Dict[str, str]],
    on_delta: Callable[[str], Awaitable[None]],
    timeout_s: Optional[float] = None,
    temperature: float = 0.4,
    max_tokens: Optional[int] = None,
    add_generation_prompt: bool = False,
    stop_token_ids: Optional[List[int]] = None,
    max_new_tokens: Optional[int] = None,
) -> ChatResponse:
    """
    LLM 中间层：流式 chat.completions（支持增量 token）。

    说明：
    - 当前仅实现 vLLM(OpenAI-Compatible) 的流式；
    - 通过 `on_delta` 把增量回调给上层（通常用于 SSE）。
    """

    backend = _normalize_backend(getattr(settings, "llm_backend", "vllm"))
    effective_timeout = float(timeout_s) if timeout_s is not None else float(settings.vllm_timeout_s)

    prepared = _preprocess_messages(messages=messages, settings=settings)

    if backend == "vllm":
        vllm_response = await vllm_chat_completions_stream(
            base_url=settings.vllm_base_url,
            model=settings.vllm_model,
            messages=prepared,
            on_delta=on_delta,
            timeout_s=effective_timeout,
            temperature=temperature,
            max_tokens=max_tokens,
            add_generation_prompt=add_generation_prompt,
            stop_token_ids=stop_token_ids,
            max_new_tokens=max_new_tokens,
        )
        return _postprocess_response(response=vllm_response, settings=settings, backend=backend)

    if backend == "openai_compat":
        api_key = get_api_key(getattr(settings, "active_model_id", "") or "")
        if not str(api_key or "").strip():
            raise RuntimeError("缺少 API Key（请在前端为该模型设置/校验）")
        effective_max_tokens = max_tokens
        if effective_max_tokens is None and max_new_tokens is not None:
            effective_max_tokens = int(max_new_tokens)
        response = await openai_compat_chat_completions_stream(
            base_url=settings.vllm_base_url,
            model=settings.vllm_model,
            messages=prepared,
            api_key=api_key,
            on_delta=on_delta,
            timeout_s=effective_timeout,
            temperature=temperature,
            max_tokens=effective_max_tokens,
        )
        return _postprocess_response(response=response, settings=settings, backend=backend)

    raise NotImplementedError(f"暂不支持的 LLM 后端：{backend}")
