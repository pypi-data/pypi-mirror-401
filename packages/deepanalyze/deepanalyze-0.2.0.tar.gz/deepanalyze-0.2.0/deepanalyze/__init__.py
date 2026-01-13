from ._version import __version__

"""
DeepAnalyze 后端包入口（Jupyter Server Extension）。

说明：
- JupyterLab 前端通过 `/deepanalyze/*` 调用本包提供的 HTTP API。
- 路由注册在 `_load_jupyter_server_extension` 中完成。
"""


def _jupyter_labextension_paths():
    return [{
        "src": "labextension",
        "dest": "deepanalyze"
    }]


def _jupyter_server_extension_points():
    return [{"module": "deepanalyze"}]

# 兼容：部分环境/工具仍会读取 legacy 的 `_jupyter_server_extension_paths`。
def _jupyter_server_extension_paths():
    return [{"module": "deepanalyze"}]


def _load_jupyter_server_extension(serverapp):
    # 将 Tornado APIHandler 挂到 Jupyter Server 的 web_app 上。
    from jupyter_server.utils import url_path_join
    from pathlib import Path

    from .store_dir import set_store_dir

    from .handlers import (
        ChatHandler,
        ChatStreamHandler,
        CellRewriteHandler,
        CellRewriteStreamHandler,
        FeedbackHandler,
        FeedbackStreamHandler,
        FrontendLogHandler,
        ModelApiKeyHandler,
        ModelUpsertHandler,
        ModelsHandler,
    )

    web_app = serverapp.web_app
    base_url = web_app.settings.get("base_url", "/")

    # 把“自定义模型配置/api_key”落盘到用户启动 Jupyter Server 的根目录下，便于随工作目录迁移/备份。
    # 例如：<jupyter_root>/.deepanalyze/{models.json,api_keys.json}
    try:
        root_dir = getattr(serverapp, "root_dir", "") or ""
        root_dir = str(root_dir).strip()
        if root_dir:
            set_store_dir(Path(root_dir) / ".deepanalyze")
    except Exception:  # noqa: BLE001
        # ignore (fallback to legacy HOME store)
        pass

    # Chat：用户消息 -> LLM -> 解析 -> frontend_ops（非流式）
    route_pattern = url_path_join(base_url, "deepanalyze", "chat")
    web_app.add_handlers(".*$", [(route_pattern, ChatHandler)])

    # Chat（流式 SSE）：返回 start/delta/final
    stream_route_pattern = url_path_join(base_url, "deepanalyze", "chat", "stream")
    web_app.add_handlers(".*$", [(stream_route_pattern, ChatStreamHandler)])

    # Feedback：前端执行 code cell 后，把输出回传用于下一轮生成（非流式）
    feedback_pattern = url_path_join(base_url, "deepanalyze", "agent", "feedback")
    web_app.add_handlers(".*$", [(feedback_pattern, FeedbackHandler)])

    # Feedback（流式 SSE）
    feedback_stream_pattern = url_path_join(base_url, "deepanalyze", "agent", "feedback", "stream")
    web_app.add_handlers(".*$", [(feedback_stream_pattern, FeedbackStreamHandler)])

    # 单元格改写：给 scratch 单元格的“指令式编辑”使用（非流式）
    cell_rewrite_pattern = url_path_join(base_url, "deepanalyze", "cell", "rewrite")
    web_app.add_handlers(".*$", [(cell_rewrite_pattern, CellRewriteHandler)])

    # 单元格改写（流式 SSE）
    cell_rewrite_stream_pattern = url_path_join(base_url, "deepanalyze", "cell", "rewrite", "stream")
    web_app.add_handlers(".*$", [(cell_rewrite_stream_pattern, CellRewriteStreamHandler)])

    # 前端日志上报：用于记录 SSE 失败、异常堆栈等排障信息
    frontend_log_pattern = url_path_join(base_url, "deepanalyze", "frontend", "log")
    web_app.add_handlers(".*$", [(frontend_log_pattern, FrontendLogHandler)])

    # 模型选择器：列表与 api_key 管理
    models_pattern = url_path_join(base_url, "deepanalyze", "models")
    web_app.add_handlers(".*$", [(models_pattern, ModelsHandler)])

    model_key_pattern = url_path_join(base_url, "deepanalyze", "models", "key")
    web_app.add_handlers(".*$", [(model_key_pattern, ModelApiKeyHandler)])

    model_upsert_pattern = url_path_join(base_url, "deepanalyze", "models", "upsert")
    web_app.add_handlers(".*$", [(model_upsert_pattern, ModelUpsertHandler)])


# 兼容：Jupyter Server 在不同版本/配置下可能调用无下划线版本。
def load_jupyter_server_extension(serverapp):
    return _load_jupyter_server_extension(serverapp)
