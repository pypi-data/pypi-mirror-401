"""Common guardrail validation helpers."""

from __future__ import annotations

from typing import Sequence


def ensure_allowed_action(action: str, allowed_actions: Sequence[str]) -> None:
    """Raise ValueError if the action is not allowed (Phase 1 stub)."""
    if action not in allowed_actions:
        raise ValueError(f"Action '{action}' not permitted in this context")
