"""AXON reset command contracts."""

from __future__ import annotations

from control.setup import SetupController


def reset_state() -> None:
    """Reset local state, sessions, and caches.

    Delegates to the control layer to enforce kill switch and audit rules.
    """
    controller = SetupController()
    controller.reset()
