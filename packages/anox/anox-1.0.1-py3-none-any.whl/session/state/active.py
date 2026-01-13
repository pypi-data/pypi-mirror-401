"""Active session state tracker."""

from __future__ import annotations


class ActiveSessionState:
    """Tracks whether a session is active (Phase 1 stub)."""

    def __init__(self) -> None:
        self._status = "IDLE"

    def activate(self, session_id: str) -> None:
        self._status = f"ACTIVE:{session_id}"

    def clear(self) -> None:
        self._status = "IDLE"

    def status(self) -> str:
        return self._status
