from __future__ import annotations

import json
import os
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict

from tornado.httpclient import HTTPClientError

from .agent_logging import get_deepanalyze_logger
from .agent_openai_compat_client import validate_api_key as validate_openai_compat_api_key
from .model_registry import ModelSpec
from .store_dir import choose_read_path, primary_path

logger = get_deepanalyze_logger("deepanalyze.secrets")


def _secrets_path() -> Path:
    return primary_path("api_keys.json")


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


@dataclass(frozen=True)
class ApiKeyStatus:
    model_id: str
    status: str  # ok/missing/invalid
    has_key: bool
    last_error: str = ""
    last_validated_at_s: float = 0.0

    def to_public_dict(self) -> Dict[str, Any]:
        return {
            "model_id": self.model_id,
            "status": self.status,
            "has_key": bool(self.has_key),
            "last_error": self.last_error,
            "last_validated_at_s": float(self.last_validated_at_s or 0.0),
        }


def _load_store() -> Dict[str, Any]:
    path = choose_read_path("api_keys.json")
    if not path.exists():
        return {"keys": {}}
    data = _read_json(path)
    if not isinstance(data, dict):
        return {"keys": {}}
    data.setdefault("keys", {})
    if not isinstance(data.get("keys"), dict):
        data["keys"] = {}
    return data


def _save_store(data: Dict[str, Any]) -> None:
    _write_json_secure(_secrets_path(), data)


def get_api_key(model_id: str) -> str:
    mid = _normalize_id(model_id)
    if not mid:
        return ""
    store = _load_store()
    item = store.get("keys", {}).get(mid)
    if not isinstance(item, dict):
        return ""
    return str(item.get("api_key") or "").strip()


def get_api_key_status(model_id: str, *, requires_api_key: bool) -> ApiKeyStatus:
    mid = _normalize_id(model_id)
    if not requires_api_key:
        return ApiKeyStatus(model_id=mid, status="ok", has_key=True)

    store = _load_store()
    item = store.get("keys", {}).get(mid)
    if not isinstance(item, dict):
        return ApiKeyStatus(model_id=mid, status="missing", has_key=False)

    api_key = str(item.get("api_key") or "").strip()
    status = str(item.get("status") or "").strip().lower() or ("missing" if not api_key else "invalid")
    last_error = str(item.get("last_error") or "").strip()
    last_validated_at_s = float(item.get("last_validated_at_s") or 0.0)
    if not api_key:
        return ApiKeyStatus(
            model_id=mid,
            status="missing",
            has_key=False,
            last_error=last_error,
            last_validated_at_s=last_validated_at_s,
        )
    if status not in {"ok", "invalid", "missing"}:
        status = "invalid"
    return ApiKeyStatus(
        model_id=mid,
        status=status,
        has_key=True,
        last_error=last_error,
        last_validated_at_s=last_validated_at_s,
    )


async def set_and_validate_api_key(*, spec: ModelSpec, api_key: str, timeout_s: float = 10.0) -> ApiKeyStatus:
    mid = _normalize_id(spec.id)
    key = str(api_key or "").strip()
    store = _load_store()
    keys = store.get("keys", {})
    if not isinstance(keys, dict):
        keys = {}
        store["keys"] = keys

    if not key:
        keys.pop(mid, None)
        _save_store(store)
        return ApiKeyStatus(model_id=mid, status="missing", has_key=False)

    status = "invalid"
    last_error = ""
    now = time.time()

    try:
        ok, err = await validate_openai_compat_api_key(
            base_url=spec.base_url,
            api_key=key,
            timeout_s=timeout_s,
        )
        status = "ok" if ok else "invalid"
        last_error = str(err or "").strip()
    except HTTPClientError as e:
        status = "invalid"
        last_error = f"验证请求失败：{e}"
    except Exception as e:  # noqa: BLE001
        status = "invalid"
        last_error = f"验证异常：{e}"

    keys[mid] = {
        "api_key": key,
        "status": status,
        "last_error": last_error,
        "last_validated_at_s": now,
    }
    _save_store(store)

    if status != "ok":
        logger.info("api_key invalid model_id=%s err=%s", mid, last_error[:200])
    else:
        logger.info("api_key ok model_id=%s", mid)

    return ApiKeyStatus(
        model_id=mid,
        status=status,
        has_key=True,
        last_error=last_error,
        last_validated_at_s=now,
    )

