"""Maps roles/profiles to model capabilities (skeleton)."""

from __future__ import annotations

from typing import Dict


def capability_for_role(role: str) -> Dict[str, str]:
    """Return capability identifiers for a role (Phase 1 stub)."""
    return {"role": role, "capability": "default"}
