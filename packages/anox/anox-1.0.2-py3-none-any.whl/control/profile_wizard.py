"""Profile wizard contracts for guiding users through profile selection."""

from __future__ import annotations

from typing import Optional

from profiles import default as default_profile


class ProfileWizard:
    """Interactive helper for selecting or creating profiles."""

    def __init__(self) -> None:
        self._active_profile: Optional[dict] = None

    def select(self, profile_name: Optional[str] = None) -> dict:
        """Select a profile (Phase 0: default only)."""
        if self._active_profile is not None:
            return self._active_profile

        if profile_name not in (None, "default"):
            raise NotImplementedError("Custom profiles not available in Phase 0")

        self._active_profile = default_profile.PROFILE.copy()
        return self._active_profile
