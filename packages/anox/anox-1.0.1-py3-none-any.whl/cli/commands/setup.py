"""AXON setup command contracts."""

from __future__ import annotations

from typing import Optional

from control.setup import SetupController


def run_setup(profile: Optional[str] = None) -> None:
    """Run the setup workflow via control layer.

    This function only delegates to the control layer; it never mutates
    state directly and never skips guardrails.
    """
    controller = SetupController()
    controller.run(profile_override=profile)
