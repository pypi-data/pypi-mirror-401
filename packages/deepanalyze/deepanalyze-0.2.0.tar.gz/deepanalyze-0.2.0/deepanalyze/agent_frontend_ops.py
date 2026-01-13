from __future__ import annotations

from datetime import datetime
from dataclasses import dataclass
from typing import Any, Dict, List

from .agent_tag_parser import TaggedSegment, extract_code


def _op_id() -> str:
    return datetime.utcnow().strftime("%Y%m%d%H%M%S%f")


@dataclass(frozen=True)
class NotebookPaths:
    output_path: str
    scratch_path: str


def build_frontend_ops_from_segments(
    *,
    segments: List[TaggedSegment],
    paths: NotebookPaths,
    include_run_after_code: bool = False,
    turn_id: str | None = None,
) -> List[Dict[str, Any]]:
    """
    把模型输出的 tag 段落映射为前端可执行的 frontend_ops（方案A）。

    约定：
    - 所有模块都会追加到 scratch（便于完整回放模型推理/产出）
    - Analyze/Understand/Answer：追加 markdown cell 到 scratch（带标题）
    - Code：先追加标题 markdown，再追加 code cell 到 scratch
    - Answer：同时追加 markdown cell 到 model-output（用于最终结果展示）
    """

    ops: List[Dict[str, Any]] = []
    for seg_i, seg in enumerate(segments):
        base_meta: Dict[str, Any] = {
            "turn_id": turn_id,
            "segment_tag": seg.tag,
            "segment_ordinal": seg_i,
        }
        if seg.tag in ("Analyze", "Understand"):
            ops.append(
                {
                    "id": _op_id(),
                    "op": "insert_cell",
                    "path": paths.scratch_path,
                    "cell_type": "markdown",
                    "source": f"### {seg.tag}\n\n{seg.content}",
                    "segment_kind": "markdown",
                    **base_meta,
                }
            )
            continue

        if seg.tag == "Code":
            ops.append(
                {
                    "id": _op_id(),
                    "op": "insert_cell",
                    "path": paths.scratch_path,
                    "cell_type": "markdown",
                    "source": "### Code",
                    "segment_kind": "header",
                    **base_meta,
                }
            )
            ops.append(
                {
                    "id": _op_id(),
                    "op": "insert_cell",
                    "path": paths.scratch_path,
                    "cell_type": "code",
                    "source": extract_code(seg.content),
                    "segment_kind": "code",
                    **base_meta,
                }
            )
            if include_run_after_code:
                ops.append(
                    {
                        "id": _op_id(),
                        "op": "run_last_cell",
                        "path": paths.scratch_path,
                        "segment_kind": "code",
                        **base_meta,
                    }
                )
            continue

        if seg.tag == "Answer":
            # 1) scratch：保留完整模型输出（便于回放/追踪）
            ops.append(
                {
                    "id": _op_id(),
                    "op": "insert_cell",
                    "path": paths.scratch_path,
                    "cell_type": "markdown",
                    "source": f"### Answer\n\n{seg.content}",
                    "segment_kind": "markdown",
                    **base_meta,
                }
            )
            # 2) output：最终答案展示
            ops.append(
                {
                    "id": _op_id(),
                    "op": "insert_cell",
                    "path": paths.output_path,
                    "cell_type": "markdown",
                    "source": seg.content,
                    "segment_kind": "output_markdown",
                    **base_meta,
                }
            )
            continue

    return ops
