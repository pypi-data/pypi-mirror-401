"""Entry point for `axon` CLI command."""

from __future__ import annotations

from cli.brain import BrainCLI


def run_brain_cli() -> None:
    """Launch the interactive Brain CLI."""
    BrainCLI().start()
