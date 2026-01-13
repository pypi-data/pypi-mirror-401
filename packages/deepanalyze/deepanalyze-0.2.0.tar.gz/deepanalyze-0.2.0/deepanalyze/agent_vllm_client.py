from __future__ import annotations

import asyncio
import json
import re
from dataclasses import dataclass
from typing import Any, Awaitable, Callable, Dict, List, Optional

from tornado.httpclient import AsyncHTTPClient, HTTPClientError, HTTPRequest

from .agent_logging import get_deepanalyze_logger

logger = get_deepanalyze_logger("deepanalyze.vllm")


@dataclass(frozen=True)
class VllmChatResponse:
    content: str
    raw: Dict[str, Any]


def _join_url(base_url: str, path: str) -> str:
    base = str(base_url or "").rstrip("/")
    p = str(path or "").lstrip("/")
    return f"{base}/{p}" if base and p else base or p


_CTX_LEN_PATTERN = re.compile(
    r"maximum context length is (\d+) tokens.*requested (\d+) tokens.*\((\d+) in the messages, (\d+) in the completion\)",
    re.IGNORECASE | re.DOTALL,
)


def _extract_error_body(e: HTTPClientError) -> str:
    try:
        if getattr(e, "response", None) is not None and e.response.body:
            return e.response.body.decode("utf-8", errors="ignore")[:4000]
    except Exception:  # noqa: BLE001
        return ""
    return ""


def _parse_context_len_error(body: str) -> Optional[Dict[str, int]]:
    s = str(body or "")
    match = _CTX_LEN_PATTERN.search(s)
    if not match:
        return None
    try:
        return {
            "max_ctx": int(match.group(1)),
            "requested": int(match.group(2)),
            "prompt_tokens": int(match.group(3)),
            "completion_tokens": int(match.group(4)),
        }
    except Exception:  # noqa: BLE001
        return None


async def chat_completions(
    *,
    base_url: str,
    model: str,
    messages: List[Dict[str, str]],
    timeout_s: float = 120.0,
    temperature: float = 0.4,
    max_tokens: Optional[int] = None,
    add_generation_prompt: bool = False,
    stop_token_ids: Optional[List[int]] = None,
    max_new_tokens: Optional[int] = None,
) -> VllmChatResponse:
    """
    调用 vLLM OpenAI-compatible 的 /v1/chat/completions（非流式，MVP）。
    """

    url = _join_url(base_url, "chat/completions")
    payload: Dict[str, Any] = {
        "model": model,
        "messages": messages,
        "stream": False,
        "temperature": temperature,
        # DeepAnalyze-8B 在参考实现中会显式传这些字段（vLLM/兼容层一般允许 extra params）
        "add_generation_prompt": bool(add_generation_prompt),
    }
    if max_tokens is not None:
        payload["max_tokens"] = int(max_tokens)
    if stop_token_ids:
        payload["stop_token_ids"] = [int(x) for x in stop_token_ids]
    if max_new_tokens is not None:
        payload["max_new_tokens"] = int(max_new_tokens)
        # 兼容：部分 OpenAI-compatible 实现只识别 max_tokens
        payload.setdefault("max_tokens", int(max_new_tokens))

    client = AsyncHTTPClient()

    async def _fetch(payload_obj: Dict[str, Any]) -> Any:
        request = HTTPRequest(
            url=url,
            method="POST",
            headers={"Content-Type": "application/json"},
            body=json.dumps(payload_obj, ensure_ascii=False),
            request_timeout=timeout_s,
        )
        return await client.fetch(request, raise_error=True)

    try:
        response = await _fetch(payload)
    except HTTPClientError as e:
        body = _extract_error_body(e)

        # vLLM 报“maximum context length”时，自动降 max_tokens/max_new_tokens 并重试一次
        ctx = _parse_context_len_error(body)
        current = int(payload.get("max_tokens") or 0)
        if ctx and current > 0:
            safety = 128
            allowed = max(1, int(ctx["max_ctx"]) - int(ctx["prompt_tokens"]) - safety)
            if allowed < current:
                payload_retry = dict(payload)
                payload_retry["max_tokens"] = allowed
                payload_retry["max_new_tokens"] = allowed
                try:
                    response = await _fetch(payload_retry)
                except HTTPClientError as e2:
                    body2 = _extract_error_body(e2)
                    msg = f"vLLM 请求失败：{e2}"
                    if body2:
                        msg = f"{msg} body={body2}"
                    raise RuntimeError(msg) from e2
            else:
                msg = f"vLLM 请求失败：{e}"
                if body:
                    msg = f"{msg} body={body}"
                raise RuntimeError(msg) from e
        else:
            msg = f"vLLM 请求失败：{e}"
            if body:
                msg = f"{msg} body={body}"
            raise RuntimeError(msg) from e

    try:
        data = json.loads(response.body.decode("utf-8"))
    except Exception as e:  # noqa: BLE001
        raise RuntimeError("vLLM 返回非 JSON 响应") from e

    try:
        content = str(data["choices"][0]["message"]["content"])
    except Exception as e:  # noqa: BLE001
        raise RuntimeError(f"vLLM 响应结构异常：{data}") from e

    return VllmChatResponse(content=content, raw=data)


def _extract_delta_text(data: Any) -> str:
    if not isinstance(data, dict):
        return ""
    choices = data.get("choices")
    if not isinstance(choices, list) or not choices:
        return ""
    first = choices[0] if isinstance(choices[0], dict) else {}
    delta = first.get("delta")
    if isinstance(delta, dict):
        content = delta.get("content")
        if isinstance(content, str) and content:
            return content
        text = delta.get("text")
        if isinstance(text, str) and text:
            return text
        # 兼容：部分实现会把内容放到 reasoning_content 等字段
        for key in ("reasoning_content", "reasoning", "content_text"):
            v = delta.get(key)
            if isinstance(v, str) and v:
                return v
    # 兼容：极少数实现可能直接给 text
    text = first.get("text")
    if isinstance(text, str) and text:
        return text
    # 兼容：部分 OpenAI-compatible 会在流式 chunk 中直接给 message.content（而不是 delta.content）
    message = first.get("message")
    if isinstance(message, dict):
        content = message.get("content")
        if isinstance(content, str) and content:
            return content
    return ""


async def chat_completions_stream(
    *,
    base_url: str,
    model: str,
    messages: List[Dict[str, str]],
    on_delta: Callable[[str], Awaitable[None]],
    timeout_s: float = 120.0,
    temperature: float = 0.4,
    max_tokens: Optional[int] = None,
    add_generation_prompt: bool = False,
    stop_token_ids: Optional[List[int]] = None,
    max_new_tokens: Optional[int] = None,
) -> VllmChatResponse:
    """
    调用 vLLM OpenAI-compatible 的 /v1/chat/completions（流式）。

    说明：
    - 通过 SSE（data: ...）逐段返回增量 token。
    - `on_delta` 用于把增量推送给上层（例如后端 SSE 给前端）。
    """

    url = _join_url(base_url, "chat/completions")
    payload: Dict[str, Any] = {
        "model": model,
        "messages": messages,
        "stream": True,
        "temperature": temperature,
        "add_generation_prompt": bool(add_generation_prompt),
    }
    if max_tokens is not None:
        payload["max_tokens"] = int(max_tokens)
    if stop_token_ids:
        payload["stop_token_ids"] = [int(x) for x in stop_token_ids]
    if max_new_tokens is not None:
        payload["max_new_tokens"] = int(max_new_tokens)
        payload.setdefault("max_tokens", int(max_new_tokens))

    client = AsyncHTTPClient()

    async def _run_stream(payload_obj: Dict[str, Any]) -> VllmChatResponse:
        buf = ""
        parts: List[str] = []
        last_json: Dict[str, Any] | None = None
        bytes_in = 0
        event_count = 0
        json_error_count = 0
        delta_count = 0

        queue: asyncio.Queue[Optional[str]] = asyncio.Queue()

        async def _consume() -> None:
            while True:
                item = await queue.get()
                if item is None:
                    return
                try:
                    await on_delta(item)
                except Exception:  # noqa: BLE001
                    # on_delta 失败不影响主流程（避免前端刷新失败导致推理中断）
                    continue

        consumer_task = asyncio.create_task(_consume())

        def _feed(chunk: bytes) -> None:
            nonlocal buf, last_json, bytes_in, event_count, json_error_count, delta_count
            try:
                text = chunk.decode("utf-8", errors="ignore")
            except Exception:  # noqa: BLE001
                return
            if not text:
                return
            bytes_in += len(chunk)
            buf += text.replace("\r\n", "\n").replace("\r", "\n")
            while "\n\n" in buf:
                event, buf = buf.split("\n\n", 1)
                if not event.strip():
                    continue
                event_count += 1
                data_lines: List[str] = []
                for line in event.split("\n"):
                    if not line.startswith("data:"):
                        continue
                    data_lines.append(line[len("data:") :].strip())
                if not data_lines:
                    continue
                data_str = "\n".join([x for x in data_lines if x])
                if not data_str:
                    continue
                if data_str.strip() == "[DONE]":
                    continue
                try:
                    obj = json.loads(data_str)
                except Exception:  # noqa: BLE001
                    json_error_count += 1
                    continue
                if isinstance(obj, dict):
                    last_json = obj
                delta_text = _extract_delta_text(obj)
                if not delta_text:
                    continue
                delta_count += 1
                parts.append(delta_text)
                try:
                    queue.put_nowait(delta_text)
                except Exception:  # noqa: BLE001
                    # queue 满/异常时，直接跳过该 delta
                    continue

        request = HTTPRequest(
            url=url,
            method="POST",
            headers={"Content-Type": "application/json"},
            body=json.dumps(payload_obj, ensure_ascii=False),
            request_timeout=timeout_s,
            streaming_callback=_feed,
        )

        response = None
        try:
            response = await client.fetch(request, raise_error=True)
        finally:
            try:
                queue.put_nowait(None)
            except Exception:  # noqa: BLE001
                pass
            try:
                await consumer_task
            except Exception:  # noqa: BLE001
                pass

        content = "".join(parts)

        logger.info(
            "vllm stream done url=%s bytes_in=%s events=%s json_errors=%s deltas=%s content_len=%s",
            url,
            bytes_in,
            event_count,
            json_error_count,
            delta_count,
            len(content),
        )

        # 如果服务端返回了 error（但我们未能提取到 delta），优先按错误处理。
        if not content.strip() and isinstance(last_json, dict) and last_json.get("error") is not None:
            raise RuntimeError(f"vLLM 流式返回错误：{last_json.get('error')}")

        # 兼容：若服务端未按 SSE 返回（或代理聚合了响应），尝试回退按非流式解析。
        if not content.strip() and response is not None:
            try:
                data = json.loads(response.body.decode("utf-8"))
                content = str(data["choices"][0]["message"]["content"])
                logger.warning(
                    "vllm stream fallback_to_json url=%s body_len=%s content_len=%s",
                    url,
                    len(response.body or b""),
                    len(content),
                )
                return VllmChatResponse(content=content, raw=data)
            except Exception:  # noqa: BLE001
                pass

        # 兜底：极端情况下 stream chunk 不含 content（只含 role/finish_reason），此时改用非流式再请求一次。
        if not content.strip():
            logger.warning(
                "vllm stream empty_content retry_non_stream url=%s bytes_in=%s events=%s last=%s",
                url,
                bytes_in,
                event_count,
                str(last_json)[:500],
            )
            retry = await chat_completions(
                base_url=base_url,
                model=model,
                messages=messages,
                timeout_s=timeout_s,
                temperature=temperature,
                max_tokens=max_tokens,
                add_generation_prompt=add_generation_prompt,
                stop_token_ids=stop_token_ids,
                max_new_tokens=max_new_tokens,
            )
            if retry.content.strip():
                try:
                    await on_delta(retry.content)
                except Exception:  # noqa: BLE001
                    pass
                return retry
            raise RuntimeError("vLLM 流式与非流式均返回空内容")

        raw: Dict[str, Any] = {"stream": True, "last": last_json or {}}
        return VllmChatResponse(content=content, raw=raw)

    try:
        return await _run_stream(payload)
    except HTTPClientError as e:
        body = _extract_error_body(e)

        ctx = _parse_context_len_error(body)
        current = int(payload.get("max_tokens") or 0)
        if ctx and current > 0:
            safety = 128
            allowed = max(1, int(ctx["max_ctx"]) - int(ctx["prompt_tokens"]) - safety)
            if allowed < current:
                payload_retry = dict(payload)
                payload_retry["max_tokens"] = allowed
                payload_retry["max_new_tokens"] = allowed
                try:
                    return await _run_stream(payload_retry)
                except HTTPClientError as e2:
                    body2 = _extract_error_body(e2)
                    msg = f"vLLM 请求失败：{e2}"
                    if body2:
                        msg = f"{msg} body={body2}"
                    raise RuntimeError(msg) from e2

        msg = f"vLLM 请求失败：{e}"
        if body:
            msg = f"{msg} body={body}"
        raise RuntimeError(msg) from e
