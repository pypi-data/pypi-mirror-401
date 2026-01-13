"""Model selection contracts for AXON control layer."""

from __future__ import annotations

from typing import Optional

from models.router import ModelRouter
from models.base import BaseModel


class ModelSelector:
    """Decides which model adapters should be active for a profile."""

    def __init__(self, router: Optional[ModelRouter] = None) -> None:
        self._router = router

    def select_worker(self) -> BaseModel:
        """Return the worker model (Phase 1: offline only)."""
        if not self._router:
            raise RuntimeError("Model router not configured")
        return self._router.select_worker()

    def select_teacher(self) -> Optional[BaseModel]:
        """Return an optional teacher model used for validation."""
        if not self._router:
            raise RuntimeError("Model router not configured")
        return self._router.select_teacher()
