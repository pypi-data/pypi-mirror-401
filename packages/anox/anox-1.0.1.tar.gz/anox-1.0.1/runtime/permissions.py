"""Runtime permission checks."""

from __future__ import annotations

from typing import Sequence


def ensure_permissions(granted: Sequence[str], required: Sequence[str]) -> None:
    """Ensure required permissions are present."""
    missing = [perm for perm in required if perm not in granted]
    if missing:
        raise PermissionError(f"Missing permissions: {', '.join(missing)}")
