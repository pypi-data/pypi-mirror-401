"""Runtime environment helpers."""

from __future__ import annotations

from pathlib import Path


class RuntimeEnvironment:
    """Resolves paths and environment information."""

    def __init__(self, root: Path) -> None:
        self._root = root

    def logs_path(self) -> Path:
        return self._root / "logs"
