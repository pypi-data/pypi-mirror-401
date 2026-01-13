"""Secrets vault stub (Phase 1: plaintext, gitignored)."""

from __future__ import annotations

from pathlib import Path
from typing import Optional


class SecretsVault:
    """Encapsulates secret storage; Phase 2 will encrypt."""

    def __init__(self, root: Path) -> None:
        self._root = root
        self._root.mkdir(parents=True, exist_ok=True)

    def store(self, name: str, value: str) -> None:
        """Store a secret (plaintext in Phase 1)."""
        (self._root / name).write_text(value, encoding="utf-8")

    def fetch(self, name: str) -> Optional[str]:
        path = self._root / name
        return path.read_text(encoding="utf-8") if path.exists() else None
