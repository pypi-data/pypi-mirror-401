from __future__ import annotations

import json
from dataclasses import dataclass
from inspect import isawaitable
from typing import Any, Dict, List, Tuple

from .agent_settings import DeepAnalyzeAgentSettings


@dataclass(frozen=True)
class WorkspaceFileEntry:
    name: str
    path: str
    size_bytes: int
    last_modified: str | None = None

    def size_str(self) -> str:
        kb = self.size_bytes / 1024.0
        if kb < 1024:
            return f"{kb:.1f}KB"
        mb = kb / 1024.0
        return f"{mb:.1f}MB"


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
    if isawaitable(value):
        return await value
    return value


def _is_hidden_name(name: str) -> bool:
    return bool(name) and name.startswith(".")


def _contains_ipynb_checkpoints(path: str) -> bool:
    parts = [p for p in str(path or "").split("/") if p]
    return ".ipynb_checkpoints" in parts


def _ext_lower(name: str) -> str:
    if "." not in name:
        return ""
    return name.rsplit(".", 1)[-1].lower()


def _is_allowed_file(entry: WorkspaceFileEntry, settings: DeepAnalyzeAgentSettings) -> bool:
    name = entry.name
    path = entry.path

    if not name:
        return False
    if _contains_ipynb_checkpoints(path):
        return False
    if name.endswith(".ipynb"):
        return False
    if _is_hidden_name(name):
        return False

    if entry.size_bytes > max(0, settings.max_file_size_kb) * 1024:
        return False

    ext = _ext_lower(name)
    allowed = {
        "csv",
        "tsv",
        "xlsx",
        "xls",
        "json",
        "jsonl",
        "parquet",
        "txt",
        "md",
        "markdown",
        "yaml",
        "yml",
        "sql",
    }
    return ext in allowed


def build_data_block(entries: List[WorkspaceFileEntry], *, max_items: int) -> str:
    lines: List[str] = []
    for i, item in enumerate(entries[: max(0, max_items)], start=1):
        info = {"name": item.name, "size": item.size_str()}
        lines.append(f"File {i}: {json.dumps(info, ensure_ascii=False)}")
    return "\n".join(lines).strip()


async def list_workspace_files(
    *,
    contents_manager: Any,
    workspace_dir: str,
    settings: DeepAnalyzeAgentSettings,
) -> Tuple[str, List[Dict[str, Any]]]:
    """
    读取工作区目录下的文件列表（仅元信息，不读内容），并返回：
    - data_block: 可直接拼到 prompt 的 # Data 段（类似 DeepAnalyze-github 的 File N: {...}）
    - files: 结构化文件数组（用于后续扩展）
    """

    model = _as_dict(await _maybe_await(contents_manager.get(workspace_dir, content=True)))
    if model.get("type") != "directory":
        raise ValueError(f"workspaceDir 不是目录：{workspace_dir}")

    items = model.get("content") or []
    candidates: List[WorkspaceFileEntry] = []
    for raw in items:
        it = _as_dict(raw)
        if it.get("type") != "file":
            continue
        name = str(it.get("name") or "")
        path = str(it.get("path") or "")
        size = it.get("size")
        try:
            size_bytes = int(size) if size is not None else 0
        except Exception:  # noqa: BLE001
            size_bytes = 0
        last_modified = it.get("last_modified") or it.get("created") or None
        entry = WorkspaceFileEntry(
            name=name, path=path, size_bytes=size_bytes, last_modified=str(last_modified) if last_modified else None
        )
        if _is_allowed_file(entry, settings):
            candidates.append(entry)

    # 按文件名排序，保证稳定性
    candidates.sort(key=lambda x: x.name.lower())
    limited = candidates[: max(0, settings.max_data_files)]

    data_block = build_data_block(limited, max_items=settings.max_data_files)
    files = [
        {
            "name": it.name,
            "path": it.path,
            "size_bytes": it.size_bytes,
            "size": it.size_str(),
            "last_modified": it.last_modified,
        }
        for it in limited
    ]
    return data_block, files
