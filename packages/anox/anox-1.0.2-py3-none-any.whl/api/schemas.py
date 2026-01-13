"""Pydantic-free dataclasses for API contracts."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class DecisionRequest:
    """Input payload for decision endpoint (Phase 1 skeleton)."""

    raw_input: str
    source: str
    role: str
    subject_id: str
