"""Simple rate limiting primitives."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class RateLimit:
    limit: int
    interval_seconds: int


class RateLimiter:
    """Skeleton rate limiter (Phase 1 stub)."""

    def __init__(self, config: RateLimit) -> None:
        self._config = config

    def allow(self, _subject_id: str) -> bool:
        """Always allow in Phase 1 (stub)."""
        return True
