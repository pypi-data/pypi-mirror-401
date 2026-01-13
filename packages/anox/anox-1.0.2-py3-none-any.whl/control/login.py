"""Login orchestration contracts for the control layer."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from control.auth.login_flow import LoginFlow
from control.auth.validator import CredentialValidator


@dataclass(frozen=True)
class LoginRequest:
    """Structured login request from CLI/UI/API."""

    source: str
    role: str
    subject_id: Optional[str] = None


class LoginController:
    """Coordinates the login flow without handling I/O directly."""

    def __init__(self) -> None:
        self._validator = CredentialValidator()
        self._flow = LoginFlow()

    def login(self, request: LoginRequest) -> None:
        """Run the login flow for a request.

        Phase 1: Validate structure only. Phase 2+: integrate session
        state, guardrails, and audit logging.
        """
        self._validator.validate_request(request)
        self._flow.start(request)
