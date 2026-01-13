"""Base tool contract (Phase 1 non-executing)."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict


class Tool(ABC):
    """Abstract representation of an off-core capability."""

    tool_id: str

    @abstractmethod
    def run(self, payload: Dict[str, Any]) -> Dict[str, Any]:  # pragma: no cover - stub
        """Execute the tool (Phase 1 should raise)."""
        raise NotImplementedError
