"""Session limits contracts."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class SessionLimitConfig:
    """Stores configurable session limits."""

    max_duration_minutes: int = 120
    max_messages: int = 100

    def reset(self) -> None:
        self.max_duration_minutes = 120
        self.max_messages = 100
