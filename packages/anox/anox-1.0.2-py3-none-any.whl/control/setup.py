"""Setup orchestration for AXON."""

from __future__ import annotations

from pathlib import Path
from typing import Optional

from control.profile_wizard import ProfileWizard
from session.limits import SessionLimitConfig


class SetupController:
    """Coordinates initial configuration tasks (Phase 0 runnable)."""

    def __init__(self) -> None:
        self._wizard = ProfileWizard()

    def run(self, profile_override: Optional[str] = None) -> dict:
        """Run the guided setup and return the active profile."""
        profile = self._wizard.select(profile_override)
        self._ensure_directories()
        return profile

    def reset(self) -> None:
        """Reset local state, caches, and sessions (Phase 1 stub)."""
        SessionLimitConfig().reset()
        # TODO: Phase 2 - Clear audit logs, caches, memory state

    def _ensure_directories(self) -> None:
        required = [
            Path("logs"),
            Path("session"),
            Path("profiles"),
            Path("secrets"),
            Path("knowledge"),
            Path("intel"),
        ]
        for directory in required:
            directory.mkdir(parents=True, exist_ok=True)
