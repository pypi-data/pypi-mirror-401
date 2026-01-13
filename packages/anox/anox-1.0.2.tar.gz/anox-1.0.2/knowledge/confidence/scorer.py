"""Confidence scoring skeleton."""

from __future__ import annotations

from typing import Dict


def score(confidence_factors: Dict[str, float]) -> float:
    """Combine factors into [0,1] score (Phase 1 stub)."""
    if not confidence_factors:
        return 0.0
    return sum(confidence_factors.values()) / len(confidence_factors)
