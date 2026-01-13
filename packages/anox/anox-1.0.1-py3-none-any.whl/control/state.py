"""Session state coordinator for the control layer."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict

from session.state.active import ActiveSessionState
from session.state.lock import SessionLock


@dataclass
class ControlState:
    """Aggregated session control state."""

    active: ActiveSessionState
    lock: SessionLock


class ControlStateManager:
    """Provides high-level operations to manipulate session state."""

    def __init__(self) -> None:
        self._state = ControlState(
            active=ActiveSessionState(),
            lock=SessionLock(),
        )

    def snapshot(self) -> Dict[str, str]:
        """Return a read-only snapshot (Phase 1 stub)."""
        return {
            "active": self._state.active.status(),
            "locked": str(self._state.lock.is_locked()),
        }
