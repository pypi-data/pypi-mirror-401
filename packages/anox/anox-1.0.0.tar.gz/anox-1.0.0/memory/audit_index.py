"""Audit memory index contracts."""

from __future__ import annotations

from pathlib import Path
from typing import Iterator


class AuditIndex:
    """Indexes audit log entries for quick lookup."""

    def __init__(self, log_path: Path) -> None:
        self._log_path = log_path

    def entries(self) -> Iterator[str]:
        with open(self._log_path, "r", encoding="utf-8") as handle:
            yield from handle
