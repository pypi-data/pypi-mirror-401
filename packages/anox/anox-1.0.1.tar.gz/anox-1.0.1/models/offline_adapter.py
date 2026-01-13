# models/offline_adapter.py
"""Simple offline model adapter used in Phase 0."""

from __future__ import annotations

from typing import Any, Dict

from models.base import BaseModel


class OfflineModelAdapter(BaseModel):
    """Deterministic mock model that echoes intent for auditability."""

    def __init__(self, name: str = "axon-offline-mock") -> None:
        super().__init__(name=name)

    def generate(self, prompt: str, context: Dict[str, Any]) -> str:
        intent_action = context.get("intent_action", "unknown_action")
        role = context.get("identity_role", "unknown_role")
        domain = context.get("intent_domain", "unknown_domain")
        plan_id = context.get("plan_id", "plan-0")
        return (
            f"[MOCK:{self.name}] role={role} domain={domain} plan={plan_id} "
            f"action={intent_action} prompt=" + prompt.strip()
        )

    def health_check(self) -> bool:
        return True
