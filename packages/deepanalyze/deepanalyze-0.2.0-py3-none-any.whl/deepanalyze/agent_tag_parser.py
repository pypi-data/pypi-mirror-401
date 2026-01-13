from __future__ import annotations

import re
from dataclasses import dataclass
from typing import List, Literal, Optional


TagName = Literal["Analyze", "Understand", "Code", "Answer"]


@dataclass(frozen=True)
class TaggedSegment:
    tag: TagName
    raw: str
    content: str


_TAG_PATTERN = re.compile(r"<(Analyze|Understand|Code|Answer)>([\s\S]*?)</\1>", re.DOTALL)


def _fix_unclosed_code(text: str) -> str:
    """
    容错：有些情况下模型会 stop 在 </Code> 之前，这里做一次补全，避免解析不到代码段。
    """

    s = str(text or "")
    if "<Code>" in s and "</Code>" not in s:
        return s + "\n</Code>"
    return s


def extract_code(code_segment: str) -> str:
    """
    从 <Code> 段中提取可执行代码：
    - 若包含 ```python fenced```，取 fenced 内部
    - 否则取原文本
    """

    raw = str(code_segment or "").strip()
    fence = re.search(r"```(?:python)?\s*([\s\S]*?)```", raw, re.DOTALL | re.IGNORECASE)
    if fence:
        return str(fence.group(1) or "").strip()
    return raw


def parse_tagged_segments(text: str) -> List[TaggedSegment]:
    s = _fix_unclosed_code(text)
    segments: List[TaggedSegment] = []
    for match in _TAG_PATTERN.finditer(s):
        tag = match.group(1)  # type: ignore[assignment]
        content = (match.group(2) or "").strip()
        raw_block = match.group(0)
        if not content:
            continue
        segments.append(TaggedSegment(tag=tag, raw=raw_block, content=content))
    return segments


def extract_answer_text(text: str) -> Optional[str]:
    segments = parse_tagged_segments(text)
    for seg in segments:
        if seg.tag == "Answer":
            return seg.content
    return None

