"""Developer role definition."""

from __future__ import annotations

from roles.base_role import BaseRole, RoleDefinition


DEVELOPER_ROLE = RoleDefinition(
    name="developer",
    domains=["dev", "data", "cloud"],
    allowed_actions=[
        "code_generation",
        "code_refactoring",
        "architecture_design",
        "documentation",
    ],
    forbidden_actions=[
        "red_team_vulnerability_analysis",
        "malware_execution",
    ],
    risk_ceiling="MEDIUM",
    confirmation_required=False,
)


class DeveloperRole(BaseRole):
    """Developer role implementation."""

    def __init__(self) -> None:
        super().__init__(DEVELOPER_ROLE)
