"""Credential validation contracts."""

from __future__ import annotations

from control.login import LoginRequest


class CredentialValidator:
    """Validates login requests before the flow starts."""

    def validate_request(self, request: LoginRequest) -> None:
        """Phase 1: ensure required fields exist."""
        if not request.source:
            raise ValueError("source is required")
        if not request.role:
            raise ValueError("role is required")
        # Phase 2+: Validate role vs roles.yaml, subject vs key store
