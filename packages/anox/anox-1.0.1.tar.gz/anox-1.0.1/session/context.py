"""Session context tracking."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict


@dataclass
class SessionContext:
    """Minimal session context (Phase 1)."""

    session_id: str
    role: str
    domain: str

    def as_dict(self) -> Dict[str, str]:
        return {
            "session_id": self.session_id,
            "role": self.role,
            "domain": self.domain,
        }
