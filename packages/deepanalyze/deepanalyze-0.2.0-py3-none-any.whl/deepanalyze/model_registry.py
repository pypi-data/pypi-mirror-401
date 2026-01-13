from __future__ import annotations

import json
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any, Dict, List, Optional

from .agent_settings import DeepAnalyzeAgentSettings
from .agent_model_store import list_model_overrides


@dataclass(frozen=True)
class ModelSpec:
    """
    模型注册表中的一条配置。

    说明：
    - “model spec” 在本项目里更接近“调用后端/提供商配置”，并非严格意义的“具体模型版本”。
    - `backend` 当前支持：
      - vllm：本地 vLLM（无需 api_key）
      - openai_compat：外部 OpenAI-Compatible API（需要 api_key）
    """

    id: str
    label: str
    backend: str
    prompt_name: str
    requires_api_key: bool
    base_url: str = ""
    model: str = ""
    temperature: float = 0.4
    is_custom: bool = False

    def to_public_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "label": self.label,
            "backend": self.backend,
            "prompt_name": self.prompt_name,
            "requires_api_key": bool(self.requires_api_key),
            "base_url": self.base_url,
            "model": self.model,
            "temperature": float(self.temperature),
            "is_custom": bool(self.is_custom),
        }


def _default_models_index_path() -> Path:
    return Path(__file__).resolve().parent / "models" / "index.json"


@lru_cache(maxsize=4)
def _load_models_index(path: str) -> Dict[str, Any]:
    p = Path(path).expanduser()
    raw = p.read_text(encoding="utf-8")
    return json.loads(raw)


def _normalize_id(raw: str) -> str:
    return str(raw or "").strip().lower().replace(" ", "_")


def _safe_str(raw: Any) -> str:
    return str(raw or "").strip()

def _safe_float(raw: Any, default: float) -> float:
    try:
        return float(raw)
    except Exception:  # noqa: BLE001
        return float(default)


def load_model_specs(*, settings: DeepAnalyzeAgentSettings) -> List[ModelSpec]:
    """
    读取 models/index.json 并返回 ModelSpec 列表。

    特殊处理：
    - `deepanalyze_8b` 的 `base_url/model` 默认从环境变量配置（agent_settings）里取，
      便于仍按原部署方式使用本地 vLLM。
    """

    index_path = _default_models_index_path()
    if not index_path.exists():
        # 兜底：至少保证本地 vLLM 可用
        base = [
            ModelSpec(
                id="deepanalyze_8b",
                label="DeepAnalyze 8B",
                backend="vllm",
                prompt_name="deepanalyze_8b",
                requires_api_key=False,
                base_url=settings.vllm_base_url,
                model=settings.vllm_model,
                temperature=0.4,
                is_custom=False,
            )
        ]
        return _apply_user_overrides(base, settings=settings)

    try:
        data = _load_models_index(str(index_path))
    except Exception:  # noqa: BLE001
        data = {}

    items = data.get("models") if isinstance(data, dict) else None
    if not isinstance(items, list):
        items = []

    specs: List[ModelSpec] = []
    for it in items:
        if not isinstance(it, dict):
            continue
        mid = _normalize_id(it.get("id"))
        if not mid:
            continue
        label = _safe_str(it.get("label")) or mid
        backend = _normalize_id(it.get("backend")) or "vllm"
        prompt_name = _normalize_id(it.get("prompt_name")) or "general"
        requires_api_key = bool(it.get("requires_api_key"))

        base_url = _safe_str(it.get("base_url"))
        model = _safe_str(it.get("model"))
        temperature = _safe_float(it.get("temperature"), 0.4)

        # 对本地 vLLM 条目做默认值填充（保持与既有环境变量兼容）
        if backend == "vllm":
            base_url = base_url or settings.vllm_base_url
            model = model or settings.vllm_model

        specs.append(
            ModelSpec(
                id=mid,
                label=label,
                backend=backend,
                prompt_name=prompt_name,
                requires_api_key=requires_api_key,
                base_url=base_url,
                model=model,
                temperature=temperature,
                is_custom=False,
            )
        )

    if specs:
        return _apply_user_overrides(specs, settings=settings)

    base = [
        ModelSpec(
            id="deepanalyze_8b",
            label="DeepAnalyze 8B",
            backend="vllm",
            prompt_name="deepanalyze_8b",
            requires_api_key=False,
            base_url=settings.vllm_base_url,
            model=settings.vllm_model,
            temperature=0.4,
            is_custom=False,
        )
    ]
    return _apply_user_overrides(base, settings=settings)


def _apply_user_overrides(base: List[ModelSpec], *, settings: DeepAnalyzeAgentSettings) -> List[ModelSpec]:
    overrides = list_model_overrides()
    if not overrides:
        return base

    by_id = {s.id: s for s in base}
    merged: List[ModelSpec] = []

    for s in base:
        ov = overrides.get(_normalize_id(s.id))
        if not ov:
            merged.append(s)
            continue
        merged.append(_merge_override(s, ov, settings=settings))

    # 追加用户自定义模型（id 不在默认列表中）
    for mid, ov in overrides.items():
        if mid in by_id:
            continue
        custom = _spec_from_override(mid, ov, settings=settings)
        if custom is not None:
            merged.append(custom)

    return merged


def _merge_override(spec: ModelSpec, ov: Dict[str, Any], *, settings: DeepAnalyzeAgentSettings) -> ModelSpec:
    label = _safe_str(ov.get("label")) or spec.label
    base_url = _safe_str(ov.get("base_url")) or spec.base_url
    model = _safe_str(ov.get("model")) or spec.model
    temperature = _safe_float(ov.get("temperature"), spec.temperature)

    # builtin 模型默认不可更改 backend/prompt/是否需要 key，但允许覆盖 label/base_url/model/temperature
    backend = spec.backend
    prompt_name = spec.prompt_name
    requires_api_key = spec.requires_api_key
    is_custom = bool(ov.get("is_custom")) if "is_custom" in ov else spec.is_custom

    if backend == "vllm":
        base_url = base_url or settings.vllm_base_url
        model = model or settings.vllm_model

    return ModelSpec(
        id=spec.id,
        label=label,
        backend=backend,
        prompt_name=prompt_name,
        requires_api_key=requires_api_key,
        base_url=base_url,
        model=model,
        temperature=temperature,
        is_custom=is_custom,
    )


def _spec_from_override(model_id: str, ov: Dict[str, Any], *, settings: DeepAnalyzeAgentSettings) -> Optional[ModelSpec]:
    mid = _normalize_id(model_id)
    if not mid:
        return None
    backend = _normalize_id(ov.get("backend")) or "openai_compat"
    label = _safe_str(ov.get("label")) or mid
    base_url = _safe_str(ov.get("base_url"))
    model = _safe_str(ov.get("model"))
    prompt_name = _normalize_id(ov.get("prompt_name")) or "universal_llm"
    requires_api_key = bool(ov.get("requires_api_key", True))
    temperature = _safe_float(ov.get("temperature"), 0.4)
    is_custom = bool(ov.get("is_custom", True))

    if backend == "vllm":
        base_url = base_url or settings.vllm_base_url
        model = model or settings.vllm_model
        requires_api_key = False

    if backend != "vllm" and not base_url:
        # 自定义外部模型必须有 base_url
        return None
    if backend != "vllm" and not model:
        return None

    return ModelSpec(
        id=mid,
        label=label,
        backend=backend,
        prompt_name=prompt_name,
        requires_api_key=requires_api_key,
        base_url=base_url,
        model=model,
        temperature=temperature,
        is_custom=is_custom,
    )


def get_default_model_id(*, settings: DeepAnalyzeAgentSettings) -> str:
    index_path = _default_models_index_path()
    if not index_path.exists():
        return "deepanalyze_8b"
    try:
        data = _load_models_index(str(index_path))
    except Exception:  # noqa: BLE001
        return "deepanalyze_8b"
    raw = data.get("default_model_id") if isinstance(data, dict) else None
    mid = _normalize_id(raw)
    return mid or "deepanalyze_8b"


def resolve_model_spec(*, settings: DeepAnalyzeAgentSettings, model_id: str) -> ModelSpec:
    desired = _normalize_id(model_id)
    specs = load_model_specs(settings=settings)
    if desired:
        for s in specs:
            if s.id == desired:
                return s
    default_id = get_default_model_id(settings=settings)
    for s in specs:
        if s.id == default_id:
            return s
    return specs[0]

