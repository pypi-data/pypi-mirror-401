from __future__ import annotations

import asyncio
import json
import posixpath
from dataclasses import dataclass
from datetime import datetime
from inspect import isawaitable
from typing import Any, Dict, List, Optional, Tuple

import nbformat
from nbformat import NotebookNode

from .agent_settings import get_agent_settings
from .agent_workspace_scanner import list_workspace_files


def _norm_path(path: str) -> str:
    return str(path or "").lstrip("/")


def _posix_join(*parts: str) -> str:
    cleaned = [p.strip("/") for p in parts if str(p or "").strip("/")]
    return "/".join(cleaned)


def _truncate(text: str, limit: int = 120) -> str:
    raw = str(text or "")
    if len(raw) <= limit:
        return raw
    return raw[: limit - 1] + "…"


def _op_id() -> str:
    return datetime.utcnow().strftime("%Y%m%d%H%M%S%f")


@dataclass(frozen=True)
class ExecutionResult:
    stdout: str
    result: str
    outputs: List[Dict[str, Any]]


class DeepAnalyzeNotebookTool:
    """
    DeepAnalyze 模式下的 Notebook 工具类（后端）。

    目标：
    - 为 chat 对话框提供统一的“工具调用”入口（JSON op）。
    - 在“方案A”下：后端只下发指令（frontend_ops），由前端直接操作 NotebookPanel，
      以获得更好的实时性（插入/删除/更新/运行后，立刻同步到浏览器）。
    - contents_manager 仍用于工作区目录的发现与管理（如列出/创建工作区）。

    说明：
    - 方案A 下，读取/修改/执行 cell 的动作都在前端完成；后端不会直接改 ipynb 文件，
      避免“外部修改提示延迟”等问题。
    """

    def __init__(
        self,
        *,
        contents_manager: Any,
        kernel_manager: Any,
        state: Optional[Dict[str, Any]] = None,
        workspaces_root_candidates: Optional[List[str]] = None,
        default_kernel_name: str = "python3",
    ) -> None:
        self._cm = contents_manager
        self._km = kernel_manager
        self._state: Dict[str, Any] = state if isinstance(state, dict) else {}
        self._default_kernel_name = default_kernel_name
        self._workspace_roots = workspaces_root_candidates or [
            "DeepAnalyze/workspaces",
            "jupyter/deepanalyze/DeepAnalyze/workspaces",
        ]
        self._resolved_workspaces_root: str | None = None

    def _as_dict(self, value: Any) -> Dict[str, Any]:
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

    async def _maybe_await(self, value: Any) -> Any:
        if isawaitable(value):
            return await value
        return value

    async def _cm_get(self, path: str, *, content: bool) -> Dict[str, Any]:
        return self._as_dict(await self._maybe_await(self._cm.get(path, content=content)))

    async def _cm_save(self, model: Dict[str, Any], path: str) -> Dict[str, Any]:
        return self._as_dict(await self._maybe_await(self._cm.save(model, path)))

    async def _cm_new_untitled(self, *, path: str, type: str) -> Dict[str, Any]:
        return self._as_dict(await self._maybe_await(self._cm.new_untitled(path=path, type=type)))

    async def _cm_rename(self, old_path: str, new_path: str) -> Dict[str, Any]:
        return self._as_dict(await self._maybe_await(self._cm.rename(old_path, new_path)))

    async def _cm_delete(self, path: str) -> None:
        await self._maybe_await(self._cm.delete(path))

    # ---------------------------------------------------------------------
    # 工作区 / 路径
    # ---------------------------------------------------------------------
    async def resolve_workspaces_root(self) -> str:
        if self._resolved_workspaces_root:
            return self._resolved_workspaces_root

        last_error: Exception | None = None
        for candidate in self._workspace_roots:
            path = _norm_path(candidate)
            if not path:
                continue
            try:
                model = await self._cm_get(path, content=False)
                if model.get("type") == "directory":
                    self._resolved_workspaces_root = path
                    return path
            except Exception as e:  # noqa: BLE001
                last_error = e
                continue

        # 没有就创建默认的第一个候选
        target = _norm_path(self._workspace_roots[0])
        if not target:
            raise RuntimeError("工作区根目录配置为空")
        await self.ensure_directory(target)
        try:
            model = await self._cm_get(target, content=False)
            if model.get("type") != "directory":
                raise RuntimeError(f"工作区根路径不是目录：{target}")
        except Exception as e:  # noqa: BLE001
            raise RuntimeError(f"无法初始化工作区根目录：{target}，错误：{e or last_error}") from e
        self._resolved_workspaces_root = target
        return target

    def set_active_context(
        self,
        *,
        workspace_dir: Optional[str] = None,
        output_path: Optional[str] = None,
        scratch_path: Optional[str] = None,
    ) -> None:
        if workspace_dir:
            self._state["workspace_dir"] = _norm_path(workspace_dir)
        if output_path:
            self._state["output_path"] = _norm_path(output_path)
        if scratch_path:
            self._state["scratch_path"] = _norm_path(scratch_path)

    def active_context(self) -> Dict[str, Any]:
        return {
            "workspace_dir": self._state.get("workspace_dir"),
            "output_path": self._state.get("output_path"),
            "scratch_path": self._state.get("scratch_path"),
        }

    def _resolve_path_from_payload(self, payload: Dict[str, Any]) -> str:
        path = str(payload.get("path") or "").strip()
        if path:
            return _norm_path(path)

        workspace = str(payload.get("workspace") or "").strip()
        kind = str(payload.get("kind") or "").strip()
        if workspace and kind:
            root = self._resolved_workspaces_root or _norm_path(self._workspace_roots[0])
            filename = "scratch.ipynb" if kind == "scratch" else "model-output.ipynb"
            return _posix_join(root, workspace, filename)

        preferred = self._state.get("scratch_path") or self._state.get("output_path")
        if preferred:
            return _norm_path(str(preferred))

        raise ValueError("缺少 path（也可通过 workspace+kind 或先由前端上报 context）")

    async def ensure_directory(self, path: str) -> None:
        p = _norm_path(path)
        if not p or p == ".":
            return
        try:
            model = await self._cm_get(p, content=False)
            if model.get("type") != "directory":
                raise RuntimeError(f"路径已存在但不是目录：{p}")
            return
        except Exception:  # noqa: BLE001
            pass

        parent = posixpath.dirname(p)
        name = posixpath.basename(p)
        if parent and parent != ".":
            await self.ensure_directory(parent)
        else:
            parent = ""

        tmp = await self._cm_new_untitled(path=parent, type="directory")
        await self._cm_rename(tmp["path"], _posix_join(parent, name))

    def workspace_dir(self, workspace: str) -> str:
        root = self._resolved_workspaces_root or _norm_path(self._workspace_roots[0])
        name = str(workspace or "").strip().strip("/")
        if not name:
            raise ValueError("workspace 不能为空")
        return _posix_join(root, name)

    async def workspace_dir_async(self, workspace: str) -> str:
        root = await self.resolve_workspaces_root()
        name = str(workspace or "").strip().strip("/")
        if not name:
            raise ValueError("workspace 不能为空")
        return _posix_join(root, name)

    async def notebook_path(self, workspace: str, kind: str) -> str:
        kind_map = {
            "output": "model-output.ipynb",
            "model-output": "model-output.ipynb",
            "scratch": "scratch.ipynb",
        }
        filename = kind_map.get(kind, kind)
        if not str(filename).endswith(".ipynb"):
            raise ValueError(f"notebook 名称必须是 .ipynb：{filename}")
        return _posix_join(await self.workspace_dir_async(workspace), filename)

    # ---------------------------------------------------------------------
    # Notebook 读写
    # ---------------------------------------------------------------------
    async def load_notebook(self, path: str) -> NotebookNode:
        p = _norm_path(path)
        model = await self._cm_get(p, content=True)
        if model.get("type") != "notebook":
            raise ValueError(f"不是 notebook：{p}")
        content = model.get("content")
        if isinstance(content, NotebookNode):
            return content
        return nbformat.from_dict(content)

    async def save_notebook(self, path: str, nb: NotebookNode) -> None:
        p = _norm_path(path)
        payload = {"type": "notebook", "format": "json", "content": nb}
        await self._cm_save(payload, p)

    async def list_cells(self, path: str) -> List[Dict[str, Any]]:
        nb = await self.load_notebook(path)
        items: List[Dict[str, Any]] = []
        for i, cell in enumerate(nb.cells):
            src = str(cell.get("source") or "")
            first_line = src.splitlines()[0] if src.splitlines() else ""
            items.append(
                {
                    "index": i,
                    "cell_type": cell.get("cell_type"),
                    "preview": _truncate(first_line, 80),
                    "lines": len(src.splitlines()),
                }
            )
        return items

    async def get_cell(self, path: str, index: int) -> NotebookNode:
        nb = await self.load_notebook(path)
        if index < 0 or index >= len(nb.cells):
            raise IndexError(f"cell index 越界：{index}")
        return nb.cells[index]

    async def insert_cell(
        self,
        path: str,
        index: int,
        *,
        cell_type: str,
        source: str,
    ) -> Dict[str, Any]:
        nb = await self.load_notebook(path)
        if index < 0:
            index = 0
        if index > len(nb.cells):
            index = len(nb.cells)

        if cell_type == "markdown":
            cell = nbformat.v4.new_markdown_cell(source=source)
        elif cell_type == "raw":
            cell = nbformat.v4.new_raw_cell(source=source)
        else:
            cell = nbformat.v4.new_code_cell(source=source)

        nb.cells.insert(index, cell)
        await self.save_notebook(path, nb)
        return {"index": index, "cell_type": cell.cell_type}

    async def delete_cell(self, path: str, index: int) -> Dict[str, Any]:
        nb = await self.load_notebook(path)
        if index < 0 or index >= len(nb.cells):
            raise IndexError(f"cell index 越界：{index}")
        removed = nb.cells.pop(index)
        await self.save_notebook(path, nb)
        return {"index": index, "cell_type": removed.get("cell_type")}

    async def update_cell_source(self, path: str, index: int, source: str) -> Dict[str, Any]:
        nb = await self.load_notebook(path)
        if index < 0 or index >= len(nb.cells):
            raise IndexError(f"cell index 越界：{index}")
        nb.cells[index]["source"] = source
        await self.save_notebook(path, nb)
        return {"index": index}

    # ---------------------------------------------------------------------
    # Kernel 执行（用于 chat 测试）
    # ---------------------------------------------------------------------
    async def execute_code(
        self,
        code: str,
        *,
        kernel_name: Optional[str] = None,
        timeout_s: float = 30.0,
    ) -> ExecutionResult:
        kernel_id = await self.get_or_start_kernel(
            kernel_name=kernel_name or self._default_kernel_name
        )
        km = self._km.get_kernel(kernel_id)
        connection_info = await self._maybe_await(km.get_connection_info())

        def _run_blocking() -> Tuple[str, str, List[Dict[str, Any]]]:
            from jupyter_client import BlockingKernelClient

            kc = BlockingKernelClient()
            kc.load_connection_info(connection_info)
            kc.start_channels()
            try:
                try:
                    kc.wait_for_ready(timeout=timeout_s)
                except Exception:  # noqa: BLE001
                    pass

                msg_id = kc.execute(code)
                stdout_parts: List[str] = []
                result_text = ""
                outputs: List[Dict[str, Any]] = []

                while True:
                    msg = kc.get_iopub_msg(timeout=timeout_s)
                    if msg.get("parent_header", {}).get("msg_id") != msg_id:
                        continue
                    msg_type = msg.get("header", {}).get("msg_type")
                    content = msg.get("content", {}) or {}

                    if msg_type == "stream":
                        if content.get("name") == "stdout":
                            stdout_parts.append(str(content.get("text", "")))
                        outputs.append(
                            {
                                "output_type": "stream",
                                "name": content.get("name", "stdout"),
                                "text": content.get("text", ""),
                            }
                        )
                    elif msg_type in ("execute_result", "display_data"):
                        data = content.get("data", {}) or {}
                        text = data.get("text/plain", "")
                        if text and not result_text:
                            result_text = str(text)
                        outputs.append(
                            {
                                "output_type": "execute_result",
                                "data": data,
                                "metadata": content.get("metadata", {}) or {},
                                "execution_count": content.get("execution_count"),
                            }
                        )
                    elif msg_type == "error":
                        outputs.append(
                            {
                                "output_type": "error",
                                "ename": content.get("ename"),
                                "evalue": content.get("evalue"),
                                "traceback": content.get("traceback", []) or [],
                            }
                        )
                    elif msg_type == "status" and content.get("execution_state") == "idle":
                        break

                return ("".join(stdout_parts), result_text, outputs)
            finally:
                try:
                    kc.stop_channels()
                except Exception:  # noqa: BLE001
                    pass
                try:
                    kc.close()
                except Exception:  # noqa: BLE001
                    pass

        stdout, result_text, outputs = await asyncio.to_thread(_run_blocking)
        return ExecutionResult(stdout=stdout, result=result_text, outputs=outputs)

    async def get_or_start_kernel(self, *, kernel_name: str) -> str:
        existing = self._state.get("kernel_id")
        if existing:
            try:
                self._km.get_kernel(existing)
                return str(existing)
            except Exception:  # noqa: BLE001
                self._state.pop("kernel_id", None)

        kernel_id = await self._km.start_kernel(kernel_name=kernel_name)
        self._state["kernel_id"] = kernel_id
        return str(kernel_id)

    async def shutdown_kernel(self) -> None:
        kernel_id = self._state.get("kernel_id")
        if not kernel_id:
            return
        try:
            await self._maybe_await(self._km.shutdown_kernel(kernel_id, now=True))
        finally:
            self._state.pop("kernel_id", None)

    async def run_cell(
        self,
        path: str,
        index: int,
        *,
        kernel_name: Optional[str] = None,
        timeout_s: float = 30.0,
        write_outputs: bool = True,
    ) -> Dict[str, Any]:
        nb = await self.load_notebook(path)
        if index < 0 or index >= len(nb.cells):
            raise IndexError(f"cell index 越界：{index}")
        cell = nb.cells[index]
        if cell.get("cell_type") != "code":
            raise ValueError("只能执行 code cell")
        code = str(cell.get("source") or "")

        result = await self.execute_code(code, kernel_name=kernel_name, timeout_s=timeout_s)
        if write_outputs:
            cell["outputs"] = result.outputs
            cell["execution_count"] = None
            await self.save_notebook(path, nb)

        return {
            "index": index,
            "stdout": _truncate(result.stdout, 2000),
            "result": _truncate(result.result, 2000),
        }

    # ---------------------------------------------------------------------
    # 便捷：创建 notebook
    # ---------------------------------------------------------------------
    async def create_notebook(self, path: str, *, overwrite: bool = False) -> str:
        p = _norm_path(path)
        parent = posixpath.dirname(p)
        if parent and parent != ".":
            await self.ensure_directory(parent)

        try:
            existing = await self._cm_get(p, content=False)
            if existing and not overwrite:
                return p
        except Exception:  # noqa: BLE001
            pass

        nb = nbformat.v4.new_notebook(cells=[], metadata={"deepanalyze": {"created_by": "backend"}})
        await self.save_notebook(p, nb)
        return p

    def to_help_text(self) -> str:
        return (
            "DeepAnalyze 后端工具已启用。你可以在聊天框发送 JSON 来测试，例如：\n"
            '1) {"op":"current_workspace"}  # 查看前端上报的当前工作区/默认 notebook\n'
            '1.1) {"op":"list_workspace_files"}  # 读取工作区文件列表（过滤 ipynb 等，用于 # Data）\n'
            '2) {"op":"list_workspaces"}\n'
            '3) {"op":"list_cells"}  # 由前端实时读取\n'
            '4) {"op":"insert_cell","index":0,"cell_type":"code","source":"print(1+2)"}\n'
            '5) {"op":"run_cell","index":0}  # 由前端使用 NotebookPanel kernel 执行\n'
            '6) {"op":"get_cell","index":0}  # 读取单元格源代码/文本\n'
            '7) {"op":"read_cell","index":0}  # 读取单元格（含输出/执行计数等）\n'
            '8) {"op":"create_notebook","path":"DeepAnalyze/workspaces/<ws>/demo.ipynb"}\n'
            '   {"op":"create_notebook","path":".../a.ipynb","target":"output"}  # 打开在 model-output 栏\n'
            '   {"op":"create_notebook","path":".../b.ipynb","target":"scratch"} # 打开在 scratch 栏\n'
            '   {"op":"create_notebook","path":".../c.ipynb","open":false}       # 仅创建，不打开\n'
            "说明：当前采用方案A：后端只下发指令（frontend_ops），由前端直接修改/执行 NotebookPanel，实时反映在浏览器里。"
        )

    async def handle_op(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        op = str(payload.get("op") or "").strip()
        if not op:
            raise ValueError("缺少 op")

        if op == "help":
            return {"ok": True, "reply": self.to_help_text()}

        if op == "resolve_workspaces_root":
            root = await self.resolve_workspaces_root()
            return {"ok": True, "root": root, "reply": f"workspaces_root = {root}"}

        if op == "current_workspace":
            ctx = self.active_context()
            return {"ok": True, "context": ctx, "reply": json.dumps(ctx, ensure_ascii=False)}

        if op == "list_workspace_files":
            workspace_dir = (
                str(payload.get("workspaceDir") or payload.get("workspace_dir") or "").strip()
                or str(self._state.get("workspace_dir") or "").strip()
            )
            if not workspace_dir:
                raise ValueError("缺少 workspaceDir（或先由前端上报 context）")
            settings = get_agent_settings()
            data_block, files = await list_workspace_files(
                contents_manager=self._cm,
                workspace_dir=_norm_path(workspace_dir),
                settings=settings,
            )
            reply = data_block or "(empty)"
            return {
                "ok": True,
                "workspace_dir": _norm_path(workspace_dir),
                "data_block": data_block,
                "files": files,
                "reply": reply,
            }

        if op == "list_workspaces":
            root = await self.resolve_workspaces_root()
            model = await self._cm_get(root, content=True)
            items = model.get("content") or []
            names = sorted(
                [
                    self._as_dict(it).get("name")
                    for it in items
                    if self._as_dict(it).get("type") == "directory"
                ],
                key=lambda x: str(x),
            )
            return {"ok": True, "workspaces": names, "reply": json.dumps(names, ensure_ascii=False)}

        if op == "ensure_workspace":
            ws = str(payload.get("workspace") or "").strip()
            root = await self.resolve_workspaces_root()
            path = _posix_join(root, ws)
            await self.ensure_directory(path)
            return {"ok": True, "workspace_dir": path, "reply": f"已确保工作区目录存在：{path}"}

        # 方案A：返回前端可执行的 ops，由前端直接操作 NotebookPanel（实时生效）
        if op in {
            "create_notebook",
            "list_cells",
            "get_cell",
            "read_cell",
            "insert_cell",
            "delete_cell",
            "update_cell",
            "run_cell",
        }:
            path = self._resolve_path_from_payload(payload)
            op_id = _op_id()
            frontend_op: Dict[str, Any] = {"id": op_id, "op": op, "path": path}
            for key in ("index", "cell_type", "source", "overwrite", "timeout_s", "target", "open"):
                if key in payload:
                    frontend_op[key] = payload[key]
            return {
                "ok": True,
                "op_id": op_id,
                "frontend_ops": [frontend_op],
                "reply": f"已下发指令：{op}（path={path}）",
            }

        raise ValueError(f"不支持的 op：{op}")
