"""Blue team role definition."""

from __future__ import annotations

from roles.base_role import BaseRole, RoleDefinition


BLUE_TEAM_ROLE = RoleDefinition(
    name="blue_team",
    domains=["cyber", "malware"],
    allowed_actions=[
        "defensive_security_analysis",
        "detection_and_monitoring_design",
        "static_malware_analysis",
    ],
    forbidden_actions=[
        "real_world_exploitation",
        "malware_execution",
    ],
    risk_ceiling="MEDIUM",
    confirmation_required=True,
)


class BlueTeamRole(BaseRole):
    """Blue team role implementation."""

    def __init__(self) -> None:
        super().__init__(BLUE_TEAM_ROLE)
