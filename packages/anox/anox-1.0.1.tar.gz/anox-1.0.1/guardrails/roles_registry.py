"""Role registry for AXON guardrails (Phase 0 Stub).

Loads `guardrails/roles.yaml` and exposes deterministic helpers for
risk ceilings, domain permissions, and action permissions. No runtime
mutation or auto-updates are allowed in Phase 0.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List

import yaml


@dataclass(frozen=True)
class RoleDefinition:
    """Immutable definition of a single role."""

    name: str
    domains: List[str]
    allowed_actions: List[str]
    forbidden_actions: List[str]
    risk_ceiling: str
    confirmation_required: bool

    def allows_domain(self, domain: str) -> bool:
        if domain == "unknown":
            return True
        return domain in self.domains

    def allows_action(self, action: str) -> bool:
        if action in self.forbidden_actions:
            return False
        return action in self.allowed_actions


class RoleRegistry:
    """Loads role definitions from YAML into immutable structures."""

    def __init__(self, roles_path: Path):
        self._roles_path = roles_path
        self._roles: Dict[str, RoleDefinition] = {}
        self._load()

    def _load(self) -> None:
        if not self._roles_path.exists():
            raise FileNotFoundError(f"Roles file not found: {self._roles_path}")

        with open(self._roles_path, "r", encoding="utf-8") as stream:
            raw = yaml.safe_load(stream) or {}

        roles_section = raw.get("roles")
        if not isinstance(roles_section, dict):
            raise ValueError("roles.yaml must contain top-level 'roles' mapping")

        for name, data in roles_section.items():
            role = RoleDefinition(
                name=name,
                domains=list(data.get("domains", [])),
                allowed_actions=list(data.get("allowed_actions", [])),
                forbidden_actions=list(data.get("forbidden_actions", [])),
                risk_ceiling=str(data.get("risk_ceiling", "LOW")),
                confirmation_required=bool(data.get("confirmation_required", False)),
            )
            self._roles[name] = role

    def get(self, role: str) -> RoleDefinition:
        if role not in self._roles:
            raise ValueError(f"Unknown role: {role}")
        return self._roles[role]

    def risk_ceiling(self, role: str) -> str:
        return self.get(role).risk_ceiling

    def requires_confirmation(self, role: str) -> bool:
        return self.get(role).confirmation_required

    def allows_domain(self, role: str, domain: str) -> bool:
        return self.get(role).allows_domain(domain)

    def allows_action(self, role: str, action: str) -> bool:
        return self.get(role).allows_action(action)

    def is_forbidden_action(self, role: str, action: str) -> bool:
        return action in self.get(role).forbidden_actions

    def list_roles(self) -> List[str]:
        return sorted(self._roles)
