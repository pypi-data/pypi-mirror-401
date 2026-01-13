from __future__ import annotations

import time
from dataclasses import dataclass, field
from threading import Lock
from typing import Any, Dict, List, Optional


@dataclass
class SessionState:
    session_id: str
    messages: List[dict] = field(default_factory=list)
    meta: Dict[str, Any] = field(default_factory=dict)
    created_at_s: float = field(default_factory=lambda: time.time())
    updated_at_s: float = field(default_factory=lambda: time.time())


class InMemorySessionStore:
    def __init__(self, *, ttl_s: float = 3600.0, max_sessions: int = 200) -> None:
        self._ttl_s = float(ttl_s)
        self._max_sessions = int(max_sessions)
        self._lock = Lock()
        self._sessions: Dict[str, SessionState] = {}

    def _prune_locked(self) -> None:
        now = time.time()
        expired = [k for k, v in self._sessions.items() if now - v.updated_at_s > self._ttl_s]
        for k in expired:
            self._sessions.pop(k, None)

        # 简单上限控制：按最近更新时间保留最新的 max_sessions 个
        if len(self._sessions) <= self._max_sessions:
            return
        items = sorted(self._sessions.items(), key=lambda kv: kv[1].updated_at_s, reverse=True)
        keep = dict(items[: self._max_sessions])
        self._sessions = keep

    def get(self, session_id: str) -> Optional[SessionState]:
        sid = str(session_id or "").strip()
        if not sid:
            return None
        with self._lock:
            self._prune_locked()
            state = self._sessions.get(sid)
            if state:
                state.updated_at_s = time.time()
            return state

    def get_or_create(self, session_id: str) -> SessionState:
        sid = str(session_id or "").strip()
        if not sid:
            sid = "anonymous"
        with self._lock:
            self._prune_locked()
            state = self._sessions.get(sid)
            if state is None:
                state = SessionState(session_id=sid)
                self._sessions[sid] = state
            state.updated_at_s = time.time()
            return state

    def reset(self, session_id: str) -> None:
        sid = str(session_id or "").strip()
        if not sid:
            return
        with self._lock:
            self._sessions.pop(sid, None)


_DEFAULT_STORE = InMemorySessionStore()


def get_session_store() -> InMemorySessionStore:
    return _DEFAULT_STORE
