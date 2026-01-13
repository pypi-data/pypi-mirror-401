"""Command registry for AXON CLI."""

from __future__ import annotations

from typing import Callable, Dict


class CommandRegistry:
    """Minimal command registry.

    Phase 1 keeps an in-memory mapping. Phase 2 may support plugin loading
    but the registry must never execute commands directly—it simply routes
    to functions defined elsewhere in the CLI package.
    """

    def __init__(self) -> None:
        self._commands: Dict[str, Callable[..., None]] = {}
        self._descriptions: Dict[str, str] = {}

    def register(self, name: str, func: Callable[..., None], description: str = "") -> None:
        """Register a callable command."""
        if name in self._commands:
            raise ValueError(f"Command '{name}' already registered")
        self._commands[name] = func
        self._descriptions[name] = description

    def execute(self, name: str, *args, **kwargs) -> None:
        """Execute a command by name."""
        if name not in self._commands:
            raise ValueError(f"Unknown command: {name}")
        self._commands[name](*args, **kwargs)

    def list_commands(self) -> Dict[str, str]:
        """Return command descriptions."""
        return dict(self._descriptions)

    def has_command(self, name: str) -> bool:
        """Check whether a command exists."""
        return name in self._commands
