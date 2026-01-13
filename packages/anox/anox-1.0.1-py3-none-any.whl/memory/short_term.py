"""Short-term memory contracts."""

from __future__ import annotations

from typing import List


class ShortTermMemory:
    """Volatile memory cleared when a session ends."""

    def __init__(self) -> None:
        self._items: List[str] = []

    def add(self, item: str) -> None:
        self._items.append(item)

    def clear(self) -> None:
        self._items.clear()

    def items(self) -> List[str]:
        return list(self._items)
