"""Session lock primitive."""

from __future__ import annotations


class SessionLock:
    """Simple in-memory lock (Phase 1)."""

    def __init__(self) -> None:
        self._locked = False

    def acquire(self) -> None:
        if self._locked:
            raise RuntimeError("Session already locked")
        self._locked = True

    def release(self) -> None:
        self._locked = False

    def is_locked(self) -> bool:
        return self._locked
