"""Task memory contracts."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass
class TaskMemoryEntry:
    task_id: str
    summary: str


class TaskMemory:
    """Tracks high-level task history."""

    def __init__(self) -> None:
        self._entries: List[TaskMemoryEntry] = []

    def record(self, entry: TaskMemoryEntry) -> None:
        self._entries.append(entry)

    def entries(self) -> List[TaskMemoryEntry]:
        return list(self._entries)
