"""Red team role definition (WHITE-HAT ONLY)."""

from __future__ import annotations

from roles.base_role import BaseRole, RoleDefinition


RED_TEAM_ROLE = RoleDefinition(
    name="red_team",
    domains=["red", "malware"],
    allowed_actions=[
        "red_team_vulnerability_analysis",
        "exploit_patterns_non_operational",
    ],
    forbidden_actions=[
        "real_world_exploitation",
        "malware_execution",
        "autonomous_attack",
    ],
    risk_ceiling="HIGH",
    confirmation_required=True,
)


class RedTeamRole(BaseRole):
    """Red team role implementation."""

    def __init__(self) -> None:
        super().__init__(RED_TEAM_ROLE)
