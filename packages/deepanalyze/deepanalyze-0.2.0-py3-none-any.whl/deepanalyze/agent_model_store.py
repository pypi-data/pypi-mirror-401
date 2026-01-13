from __future__ import annotations

import json
import os
import time
import uuid
from pathlib import Path
from typing import Any, Dict, Optional

from .agent_logging import get_deepanalyze_logger
from .store_dir import choose_read_path, primary_path

logger = get_deepanalyze_logger("deepanalyze.model_store")


def _models_path() -> Path:
    return primary_path("models.json")


def _read_json(path: Path) -> Dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:  # noqa: BLE001
        return {}


def _write_json_secure(path: Path, data: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    try:
        os.chmod(tmp, 0o600)
    except Exception:  # noqa: BLE001
        pass
    tmp.replace(path)
    try:
        os.chmod(path, 0o600)
    except Exception:  # noqa: BLE001
        pass


def _normalize_id(raw: str) -> str:
    return str(raw or "").strip().lower().replace(" ", "_")


def _normalize_base_url(raw: str) -> str:
    return str(raw or "").strip().rstrip("/")


def load_models_store() -> Dict[str, Any]:
    path = choose_read_path("models.json")
    if not path.exists():
        return {"models": {}}
    data = _read_json(path)
    if not isinstance(data, dict):
        return {"models": {}}
    data.setdefault("models", {})
    if not isinstance(data.get("models"), dict):
        data["models"] = {}
    return data


def save_models_store(data: Dict[str, Any]) -> None:
    _write_json_secure(_models_path(), data)


def generate_custom_model_id(label: str) -> str:
    base = _normalize_id(label).strip("_")
    if not base:
        base = "custom_model"
    suffix = uuid.uuid4().hex[:6]
    return f"{base}_{suffix}"


def upsert_model(
    *,
    model_id: str,
    label: str,
    backend: str,
    base_url: str,
    model: str,
    temperature: float,
    prompt_name: str,
    requires_api_key: bool,
    is_custom: bool,
) -> Dict[str, Any]:
    mid = _normalize_id(model_id)
    now = time.time()
    store = load_models_store()
    models = store.get("models", {})
    if not isinstance(models, dict):
        models = {}
        store["models"] = models

    existing = models.get(mid) if isinstance(models.get(mid), dict) else {}
    created_at = float(existing.get("created_at_s") or now)

    record = {
        "id": mid,
        "label": str(label or "").strip() or mid,
        "backend": _normalize_id(backend) or "openai_compat",
        "base_url": _normalize_base_url(base_url),
        "model": str(model or "").strip(),
        "temperature": float(temperature),
        "prompt_name": _normalize_id(prompt_name) or "universal_llm",
        "requires_api_key": bool(requires_api_key),
        "is_custom": bool(is_custom),
        "created_at_s": created_at,
        "updated_at_s": now,
    }
    models[mid] = record
    save_models_store(store)
    logger.info("model upsert id=%s backend=%s base_url=%s", mid, record["backend"], record["base_url"])
    return record


def get_model_override(model_id: str) -> Optional[Dict[str, Any]]:
    mid = _normalize_id(model_id)
    store = load_models_store()
    item = store.get("models", {}).get(mid)
    return item if isinstance(item, dict) else None


def list_model_overrides() -> Dict[str, Dict[str, Any]]:
    store = load_models_store()
    models = store.get("models", {})
    if not isinstance(models, dict):
        return {}
    out: Dict[str, Dict[str, Any]] = {}
    for k, v in models.items():
        if not isinstance(k, str) or not isinstance(v, dict):
            continue
        out[_normalize_id(k)] = v
    return out
