"""Observer role definition."""

from __future__ import annotations

from roles.base_role import BaseRole, RoleDefinition


OBSERVER_ROLE = RoleDefinition(
    name="observer",
    domains=["dev"],
    allowed_actions=[
        "view_logs",
        "read_analysis",
    ],
    forbidden_actions=["any_modification"],
    risk_ceiling="LOW",
    confirmation_required=False,
)


class ObserverRole(BaseRole):
    """Observer role implementation (read-only)."""

    def __init__(self) -> None:
        super().__init__(OBSERVER_ROLE)
