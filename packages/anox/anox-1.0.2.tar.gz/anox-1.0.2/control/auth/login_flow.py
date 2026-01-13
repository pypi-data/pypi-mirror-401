"""Login flow coordination (Phase 1 skeleton)."""

from __future__ import annotations

from typing import Optional

from control.login import LoginRequest


class LoginFlow:
    """Represents the high-level login sequence."""

    def start(self, request: LoginRequest) -> None:
        """Begin the login process (Phase 1 stub)."""
        raise NotImplementedError("Login flow not implemented (Phase 1)")
