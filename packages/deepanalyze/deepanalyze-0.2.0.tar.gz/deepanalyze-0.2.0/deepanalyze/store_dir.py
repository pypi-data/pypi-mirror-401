from __future__ import annotations

import os
from pathlib import Path
from typing import Optional

from .agent_logging import get_deepanalyze_logger

logger = get_deepanalyze_logger("deepanalyze.store_dir")

_STORE_DIR_OVERRIDE: Optional[Path] = None


def set_store_dir(path: Optional[str | Path]) -> None:
    """
    设置 DeepAnalyze 的用户侧存储目录。

    说明：
    - 用于控制“自定义模型配置(models.json)”与“api_key(api_keys.json)”的落盘位置；
    - 典型场景：在 Jupyter Server 启动时，将其设置为 `serverapp.root_dir/.deepanalyze`；
    - 若传入 None，则清空 override，回退到默认策略。
    """

    global _STORE_DIR_OVERRIDE  # noqa: PLW0603
    if path is None:
        _STORE_DIR_OVERRIDE = None
        return
    _STORE_DIR_OVERRIDE = Path(path).expanduser()


def legacy_home_store_dir() -> Path:
    return Path.home().expanduser() / ".deepanalyze"


def store_dir() -> Path:
    """
    获取当前有效的存储目录（不创建目录）。

    优先级（从高到低）：
    1) 环境变量 `DEEPANALYZE_STORE_DIR`
    2) 运行时注入的 override（`set_store_dir`）
    3) 兼容旧版本：`~/.deepanalyze`
    """

    env = str(os.environ.get("DEEPANALYZE_STORE_DIR") or "").strip()
    if env:
        return Path(env).expanduser()
    if _STORE_DIR_OVERRIDE is not None:
        return _STORE_DIR_OVERRIDE
    return legacy_home_store_dir()


def primary_path(filename: str) -> Path:
    return store_dir() / filename


def legacy_path(filename: str) -> Path:
    return legacy_home_store_dir() / filename


def choose_read_path(filename: str) -> Path:
    """
    读取时优先使用 primary；若 primary 不存在且 legacy 存在，则回退 legacy。
    """

    primary = primary_path(filename)
    if primary.exists():
        return primary
    legacy = legacy_path(filename)
    if legacy.exists() and legacy != primary:
        logger.info("fallback to legacy store path: %s", legacy)
        return legacy
    return primary

