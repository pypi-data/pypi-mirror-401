"""Simple key store for credentials during Phase 1."""

from __future__ import annotations

from pathlib import Path
from typing import Optional


class KeyStore:
    """File-based key storage (gitignored)."""

    def __init__(self, root: Path) -> None:
        self._root = root
        self._root.mkdir(parents=True, exist_ok=True)

    def set_key(self, name: str, value: str) -> None:
        """Store a key (Phase 1: plaintext)."""
        (self._root / f"{name}.key").write_text(value, encoding="utf-8")

    def get_key(self, name: str) -> Optional[str]:
        """Retrieve a key, returning None if missing."""
        path = self._root / f"{name}.key"
        if not path.exists():
            return None
        return path.read_text(encoding="utf-8").strip()
