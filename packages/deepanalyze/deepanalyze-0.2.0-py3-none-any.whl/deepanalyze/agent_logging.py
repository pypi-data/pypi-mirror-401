from __future__ import annotations

import logging
import tempfile
from pathlib import Path
from threading import Lock
from typing import Optional

from .agent_settings import DeepAnalyzeAgentSettings, get_agent_settings

_lock = Lock()
_configured = False
_BASE_LOGGER_NAME = "deepanalyze"
_HANDLER_NAME = "deepanalyze.rotating_file"


def _parse_level(level: str) -> int:
    value = str(level or "").strip().upper()
    if not value:
        return logging.INFO
    return getattr(logging, value, logging.INFO)


def _ensure_log_dir(settings: DeepAnalyzeAgentSettings) -> Path:
    raw = str(settings.log_dir or "").strip()
    if not raw:
        raw = "DeepAnalyze/logs"

    p = Path(raw)
    if not p.is_absolute():
        p = (Path.cwd() / p).resolve()

    try:
        p.mkdir(parents=True, exist_ok=True)
        return p
    except Exception:  # noqa: BLE001
        fallback = Path(tempfile.gettempdir()) / "deepanalyze-logs"
        fallback.mkdir(parents=True, exist_ok=True)
        return fallback


def _configure_base_logger(settings: DeepAnalyzeAgentSettings) -> logging.Logger:
    global _configured  # noqa: PLW0603

    base_logger = logging.getLogger(_BASE_LOGGER_NAME)
    if _configured:
        return base_logger

    level = _parse_level(settings.log_level)
    base_logger.setLevel(level)

    log_dir = _ensure_log_dir(settings)
    log_path = log_dir / "deepanalyze.log"

    formatter = logging.Formatter(
        fmt="%(asctime)s %(levelname)s [%(name)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    try:
        from logging.handlers import RotatingFileHandler

        # 避免重复添加（在 Jupyter 里可能会多次 import / reload）
        for h in base_logger.handlers:
            if getattr(h, "name", "") == _HANDLER_NAME:
                _configured = True
                base_logger.propagate = True
                return base_logger

        file_handler = RotatingFileHandler(
            filename=str(log_path),
            maxBytes=max(0, int(settings.log_max_bytes)),
            backupCount=max(0, int(settings.log_backup_count)),
            encoding="utf-8",
        )
        file_handler.name = _HANDLER_NAME
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        base_logger.addHandler(file_handler)
    except Exception:  # noqa: BLE001
        # 兜底：至少保证不因日志初始化失败而影响功能
        pass

    # 不打断 Jupyter Server 自身 logging；同时写文件 + root handler（console）
    base_logger.propagate = True
    _configured = True
    return base_logger


def get_deepanalyze_logger(
    name: str = _BASE_LOGGER_NAME,
    settings: Optional[DeepAnalyzeAgentSettings] = None,
) -> logging.Logger:
    """
    获取 DeepAnalyze 专用 logger（带文件轮转）。

    - 默认写入 `${DEEPANALYZE_LOG_DIR}/deepanalyze.log`
    - 避免重复添加 handler（多次 import / 多实例 handler 时也稳定）
    """

    settings = settings or get_agent_settings()

    with _lock:
        _configure_base_logger(settings)

        logger = logging.getLogger(name)
        # 子 logger 不挂 handler，靠层级传播到 deepanalyze 基座 logger
        if name != _BASE_LOGGER_NAME:
            logger.setLevel(logging.NOTSET)
        logger.propagate = True
        return logger
