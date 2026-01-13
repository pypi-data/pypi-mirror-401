"""Session source validation."""

from __future__ import annotations

from typing import Literal

AllowedSource = Literal["human", "api", "internal"]


def validate_source(source: str) -> AllowedSource:
    """Validate session source (Phase 1 stub)."""
    if source not in {"human", "api", "internal"}:
        raise ValueError("Invalid source")
    return source  # type: ignore[return-value]
