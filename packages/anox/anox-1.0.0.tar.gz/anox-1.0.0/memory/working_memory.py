"""Working memory contracts for active tasks."""

from __future__ import annotations

from typing import Dict, Any


class WorkingMemory:
    """Holds task-scoped context during execution."""

    def __init__(self) -> None:
        self._state: Dict[str, Any] = {}

    def set(self, key: str, value: Any) -> None:
        self._state[key] = value

    def get(self, key: str) -> Any:
        return self._state.get(key)

    def clear(self) -> None:
        self._state.clear()
