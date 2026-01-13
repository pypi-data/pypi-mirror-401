"""Model capability constraints (Phase 1 skeleton)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class CapabilityConstraints:
    """Constraints attached to a model invocation."""

    max_tokens: int
    temperature: float


DEFAULT_CONSTRAINTS = CapabilityConstraints(max_tokens=2048, temperature=0.2)


def apply_constraints(params: Dict[str, float]) -> CapabilityConstraints:
    """Return constraints overriding defaults when provided."""
    return CapabilityConstraints(
        max_tokens=int(params.get("max_tokens", DEFAULT_CONSTRAINTS.max_tokens)),
        temperature=float(params.get("temperature", DEFAULT_CONSTRAINTS.temperature)),
    )
