"""Session switch helper."""

from __future__ import annotations

from session.state.active import ActiveSessionState


def switch_session(state: ActiveSessionState, new_session_id: str) -> None:
    """Switch to a new session ID (Phase 1 stub)."""
    state.activate(new_session_id)
