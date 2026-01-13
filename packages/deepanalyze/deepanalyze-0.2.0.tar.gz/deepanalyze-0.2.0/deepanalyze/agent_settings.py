from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache


def _env(key: str, default: str) -> str:
    raw = os.getenv(key)
    if raw is None:
        return default
    value = str(raw).strip()
    return value if value else default


def _env_int(key: str, default: int) -> int:
    raw = os.getenv(key)
    if raw is None:
        return default
    try:
        return int(str(raw).strip())
    except Exception:  # noqa: BLE001
        return default


def _env_float(key: str, default: float) -> float:
    raw = os.getenv(key)
    if raw is None:
        return default
    try:
        return float(str(raw).strip())
    except Exception:  # noqa: BLE001
        return default


def _env_bool(key: str, default: bool) -> bool:
    raw = os.getenv(key)
    if raw is None:
        return default
    normalized = str(raw).strip().lower()
    if normalized in {"1", "true", "yes", "y", "on"}:
        return True
    if normalized in {"0", "false", "no", "n", "off"}:
        return False
    return default


def _env_int_list(key: str, default: list[int]) -> list[int]:
    raw = os.getenv(key)
    if raw is None:
        return default
    s = str(raw).strip()
    if not s:
        return default
    items: list[int] = []
    for part in s.split(","):
        p = part.strip()
        if not p:
            continue
        try:
            items.append(int(p))
        except Exception:  # noqa: BLE001
            continue
    return items if items else default


@dataclass(frozen=True)
class DeepAnalyzeAgentSettings:
    """
    DeepAnalyze 智能体/编排层配置（后端）。

    说明：
    - 本阶段先以环境变量为主，保证部署/调参简单可控。
    - 后续可扩展为：读取 jupyter_server_config、按用户/会话覆写等。
    """

    vllm_base_url: str
    vllm_model: str
    vllm_timeout_s: float
    max_turns: int
    max_data_files: int
    max_file_size_kb: int
    enable_stream: bool
    system_prompt_path: str
    system_prompt_name: str
    vllm_add_generation_prompt: bool
    vllm_stop_token_ids: list[int]
    vllm_max_new_tokens: int
    llm_backend: str
    active_model_id: str
    llm_temperature: float
    log_dir: str
    log_level: str
    log_max_bytes: int
    log_backup_count: int


@lru_cache(maxsize=1)
def get_agent_settings() -> DeepAnalyzeAgentSettings:
    """
    读取环境变量并返回设置（带默认值）。

    环境变量约定：
    - DEEPANALYZE_VLLM_BASE_URL: vLLM OpenAI-Compatible baseUrl（默认 http://127.0.0.1:8000/v1）
    - DEEPANALYZE_VLLM_MODEL: 模型 id（默认 DeepAnalyze-8B）
    - DEEPANALYZE_VLLM_TIMEOUT_S: 单次请求超时秒数（默认 120）
    - DEEPANALYZE_MAX_TURNS: 最大多轮次数（默认 12）
    - DEEPANALYZE_MAX_DATA_FILES: 注入 #Data 的文件数量上限（默认 30）
    - DEEPANALYZE_MAX_FILE_SIZE_KB: 注入/展示前的单文件大小阈值（默认 10240KB = 10MB）
    - DEEPANALYZE_ENABLE_STREAM: 是否启用 vLLM 流式（默认 false）
    - DEEPANALYZE_SYSTEM_PROMPT_PATH: system prompt 模板路径（为空则使用内置默认）
    - DEEPANALYZE_SYSTEM_PROMPT_NAME: system prompt 模板名（从 deepanalyze/prompts/index.json 选择；默认 general）
    - DEEPANALYZE_LLM_BACKEND: LLM 后端类型（默认 vllm；后续可扩展 openai/azure/xxx）
    - DEEPANALYZE_VLLM_ADD_GENERATION_PROMPT: 透传给 vLLM（默认 false，DeepAnalyze-8B 推荐）
    - DEEPANALYZE_VLLM_STOP_TOKEN_IDS: 透传给 vLLM（默认 151676,151645，DeepAnalyze-8B 推荐）
    - DEEPANALYZE_VLLM_MAX_NEW_TOKENS: 透传给 vLLM（默认 8192；如模型支持更长上下文可调大）
    - DEEPANALYZE_LOG_DIR: 日志目录（默认 DeepAnalyze/logs）
    - DEEPANALYZE_LOG_LEVEL: 日志级别（默认 INFO）
    - DEEPANALYZE_LOG_MAX_BYTES: 单个日志文件上限（默认 10485760 = 10MB）
    - DEEPANALYZE_LOG_BACKUP_COUNT: 轮转备份数量（默认 10）
    - DEEPANALYZE_ACTIVE_MODEL_ID: 默认“模型选择器”选中的 model_id（默认 deepanalyze_8b；一般由前端传入覆盖）
    - DEEPANALYZE_LLM_TEMPERATURE: 默认温度（默认 0.4；可被模型配置覆盖）
    """

    base_url = _env("DEEPANALYZE_VLLM_BASE_URL", "http://127.0.0.1:8000/v1").rstrip("/")
    return DeepAnalyzeAgentSettings(
        vllm_base_url=base_url,
        vllm_model=_env("DEEPANALYZE_VLLM_MODEL", "DeepAnalyze-8B"),
        vllm_timeout_s=_env_float("DEEPANALYZE_VLLM_TIMEOUT_S", 120.0),
        max_turns=_env_int("DEEPANALYZE_MAX_TURNS", 12),
        max_data_files=_env_int("DEEPANALYZE_MAX_DATA_FILES", 30),
        max_file_size_kb=_env_int("DEEPANALYZE_MAX_FILE_SIZE_KB", 10_240),
        enable_stream=_env_bool("DEEPANALYZE_ENABLE_STREAM", True),
        system_prompt_path=_env("DEEPANALYZE_SYSTEM_PROMPT_PATH", ""),
        system_prompt_name=_env("DEEPANALYZE_SYSTEM_PROMPT_NAME", "general"),
        vllm_add_generation_prompt=_env_bool("DEEPANALYZE_VLLM_ADD_GENERATION_PROMPT", False),
        vllm_stop_token_ids=_env_int_list("DEEPANALYZE_VLLM_STOP_TOKEN_IDS", [151676, 151645]),
        vllm_max_new_tokens=_env_int("DEEPANALYZE_VLLM_MAX_NEW_TOKENS", 8192),
        llm_backend=_env("DEEPANALYZE_LLM_BACKEND", "vllm"),
        active_model_id=_env("DEEPANALYZE_ACTIVE_MODEL_ID", "deepanalyze_8b"),
        llm_temperature=_env_float("DEEPANALYZE_LLM_TEMPERATURE", 0.4),
        log_dir=_env("DEEPANALYZE_LOG_DIR", "DeepAnalyze/logs"),
        log_level=_env("DEEPANALYZE_LOG_LEVEL", "INFO"),
        log_max_bytes=_env_int("DEEPANALYZE_LOG_MAX_BYTES", 10 * 1024 * 1024),
        log_backup_count=_env_int("DEEPANALYZE_LOG_BACKUP_COUNT", 10),
    )
