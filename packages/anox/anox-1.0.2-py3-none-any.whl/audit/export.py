"""Audit export utilities."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable


def export_logs(log_path: Path, destination: Path) -> None:
    """Copy audit log to destination (Phase 1 stub)."""
    destination.write_text(log_path.read_text(encoding="utf-8"), encoding="utf-8")
