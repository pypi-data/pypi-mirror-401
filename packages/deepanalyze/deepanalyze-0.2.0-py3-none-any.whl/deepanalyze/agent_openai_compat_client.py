from __future__ import annotations

import asyncio
import json
from dataclasses import dataclass
from typing import Any, Awaitable, Callable, Dict, List, Optional, Tuple

from tornado.httpclient import AsyncHTTPClient, HTTPClientError, HTTPRequest

from .agent_logging import get_deepanalyze_logger

logger = get_deepanalyze_logger("deepanalyze.openai_compat")


@dataclass(frozen=True)
class OpenAICompatChatResponse:
    content: str
    raw: Dict[str, Any]


def _join_url(base_url: str, path: str) -> str:
    base = str(base_url or "").rstrip("/")
    p = str(path or "").lstrip("/")
    return f"{base}/{p}" if base and p else base or p


def _extract_error_body(e: HTTPClientError) -> str:
    try:
        if getattr(e, "response", None) is not None and e.response.body:
            return e.response.body.decode("utf-8", errors="ignore")[:4000]
    except Exception:  # noqa: BLE001
        return ""
    return ""


async def validate_api_key(*, base_url: str, api_key: str, timeout_s: float = 10.0) -> Tuple[bool, str]:
    """
    通过 GET /models 粗略验证 api_key 是否可用。

    说明：
    - 该校验仅用于 UI“绿点/红点”的状态提示，不能保证对任意模型都有权限。
    - 失败时返回 (False, error_message)。
    """

    key = str(api_key or "").strip()
    if not key:
        return False, "api_key 为空"

    url = _join_url(base_url, "models")
    client = AsyncHTTPClient()
    req = HTTPRequest(
        url=url,
        method="GET",
        headers={"Authorization": f"Bearer {key}"},
        request_timeout=float(timeout_s),
    )
    try:
        resp = await client.fetch(req, raise_error=True)
        _ = resp  # noqa: F841
        return True, ""
    except HTTPClientError as e:
        body = _extract_error_body(e)
        msg = f"HTTP {getattr(getattr(e, 'response', None), 'code', '-')}: {e}"
        if body:
            msg = f"{msg} body={body}"
        return False, msg
    except Exception as e:  # noqa: BLE001
        return False, str(e)


async def chat_completions(
    *,
    base_url: str,
    model: str,
    messages: List[Dict[str, str]],
    api_key: str,
    timeout_s: float = 120.0,
    temperature: float = 0.4,
    max_tokens: Optional[int] = None,
) -> OpenAICompatChatResponse:
    """
    调用 OpenAI-compatible 的 /v1/chat/completions（非流式）。
    """

    url = _join_url(base_url, "chat/completions")
    payload: Dict[str, Any] = {
        "model": model,
        "messages": messages,
        "stream": False,
        "temperature": float(temperature),
    }
    if max_tokens is not None:
        payload["max_tokens"] = int(max_tokens)

    client = AsyncHTTPClient()
    request = HTTPRequest(
        url=url,
        method="POST",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {str(api_key or '').strip()}",
        },
        body=json.dumps(payload, ensure_ascii=False),
        request_timeout=float(timeout_s),
    )
    try:
        response = await client.fetch(request, raise_error=True)
    except HTTPClientError as e:
        body = _extract_error_body(e)
        msg = f"OpenAI-compatible 请求失败：{e}"
        if body:
            msg = f"{msg} body={body}"
        raise RuntimeError(msg) from e

    try:
        data = json.loads(response.body.decode("utf-8"))
    except Exception as e:  # noqa: BLE001
        raise RuntimeError("OpenAI-compatible 返回非 JSON 响应") from e

    try:
        content = str(data["choices"][0]["message"]["content"])
    except Exception as e:  # noqa: BLE001
        raise RuntimeError(f"OpenAI-compatible 响应结构异常：{data}") from e

    return OpenAICompatChatResponse(content=content, raw=data)


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
        for key in ("reasoning_content", "reasoning", "content_text", "text"):
            v = delta.get(key)
            if isinstance(v, str) and v:
                return v
    text = first.get("text")
    if isinstance(text, str) and text:
        return text
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
    api_key: str,
    on_delta: Callable[[str], Awaitable[None]],
    timeout_s: float = 120.0,
    temperature: float = 0.4,
    max_tokens: Optional[int] = None,
) -> OpenAICompatChatResponse:
    """
    调用 OpenAI-compatible 的 /v1/chat/completions（流式）。
    """

    url = _join_url(base_url, "chat/completions")
    payload: Dict[str, Any] = {
        "model": model,
        "messages": messages,
        "stream": True,
        "temperature": float(temperature),
    }
    if max_tokens is not None:
        payload["max_tokens"] = int(max_tokens)

    client = AsyncHTTPClient()
    buf = ""
    parts: List[str] = []
    last_json: Dict[str, Any] | None = None
    bytes_in = 0
    event_count = 0
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
                continue

    consumer_task = asyncio.create_task(_consume())

    def _feed(chunk: bytes) -> None:
        nonlocal buf, last_json, bytes_in, event_count, delta_count
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
            for line in event.split("\n"):
                ln = line.strip()
                if not ln.startswith("data:"):
                    continue
                data = ln[len("data:") :].strip()
                if not data or data == "[DONE]":
                    continue
                try:
                    obj = json.loads(data)
                    if isinstance(obj, dict):
                        last_json = obj
                        delta = _extract_delta_text(obj)
                        if delta:
                            parts.append(delta)
                            delta_count += 1
                            queue.put_nowait(delta)
                except Exception:  # noqa: BLE001
                    continue

    req = HTTPRequest(
        url=url,
        method="POST",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {str(api_key or '').strip()}",
        },
        body=json.dumps(payload, ensure_ascii=False),
        request_timeout=float(timeout_s),
        streaming_callback=_feed,
    )

    try:
        response = await client.fetch(req, raise_error=True)
        _ = response  # noqa: F841
    except HTTPClientError as e:
        body = _extract_error_body(e)
        msg = f"OpenAI-compatible 流式请求失败：{e}"
        if body:
            msg = f"{msg} body={body}"
        raise RuntimeError(msg) from e
    finally:
        queue.put_nowait(None)
        try:
            await consumer_task
        except Exception:  # noqa: BLE001
            pass

    logger.info(
        "openai_compat stream done bytes=%s events=%s deltas=%s",
        bytes_in,
        event_count,
        delta_count,
    )
    return OpenAICompatChatResponse(content="".join(parts), raw=last_json or {})


