"""API server skeleton for AXON."""

from __future__ import annotations

from typing import Any

from api.schemas import DecisionRequest
from control.login import LoginController, LoginRequest
from core.sentry_config import capture_exception, add_breadcrumb


class AxonAPIServer:
    """Serves HTTP or IPC requests (Phase 1 stub)."""

    def __init__(self) -> None:
        self._login = LoginController()

    def handle_decision(self, payload: DecisionRequest) -> Any:
        """Handle a decision request via orchestrator (stub)."""
        add_breadcrumb(
            message="Decision request received",
            category="api",
            data={"intent": payload.intent if hasattr(payload, 'intent') else None}
        )
        raise NotImplementedError("API server not implemented in Phase 1")

    def handle_login(self, payload: LoginRequest) -> None:
        """Forward login payloads to control layer."""
        try:
            add_breadcrumb(
                message="Login request received",
                category="api",
                data={"user": payload.username if hasattr(payload, 'username') else None}
            )
            self._login.login(payload)
        except Exception as e:
            capture_exception(e, context={'operation': 'login'})
            raise
