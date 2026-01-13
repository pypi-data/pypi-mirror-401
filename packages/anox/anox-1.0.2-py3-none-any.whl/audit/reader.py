"""Audit log reader contracts."""

from __future__ import annotations

from pathlib import Path
from typing import Iterator


class AuditReader:
    """Iterates through audit log entries."""

    def __init__(self, log_path: Path) -> None:
        self._log_path = log_path

    def stream(self) -> Iterator[str]:
        with open(self._log_path, "r", encoding="utf-8") as handle:
            yield from handle
