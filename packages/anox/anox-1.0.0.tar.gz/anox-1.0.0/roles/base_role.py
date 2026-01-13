"""Role definitions and base class contracts for AXON."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class RoleDefinition:
    """Static role definition loaded from guardrails/roles.yaml."""

    name: str
    domains: List[str]
    allowed_actions: List[str]
    forbidden_actions: List[str]
    risk_ceiling: str
    confirmation_required: bool


class BaseRole:
    """Base role primitive used by the control layer.

    Roles never perform actions; they define permissions used by the
    orchestrator and domain enforcer.
    """

    def __init__(self, definition: RoleDefinition) -> None:
        self._definition = definition

    @property
    def definition(self) -> RoleDefinition:  # pragma: no cover - trivial accessor
        return self._definition

    def can_perform(self, action: str) -> bool:
        """Check if the role explicitly allows an action."""
        if action in self._definition.forbidden_actions:
            return False
        return action in self._definition.allowed_actions

    def can_access_domain(self, domain: str) -> bool:
        """Check if the role can access a domain."""
        return domain in self._definition.domains

    def get_risk_ceiling(self) -> str:
        """Return the highest risk level this role can accept."""
        return self._definition.risk_ceiling
