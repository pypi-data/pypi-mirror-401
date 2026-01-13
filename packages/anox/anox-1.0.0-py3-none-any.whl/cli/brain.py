"""CLI interface for coordinating AXON's brain pipeline."""

from __future__ import annotations

from pathlib import Path
from typing import Optional

from control.setup import SetupController
from core.orchestrator import DecisionOrchestrator
from core.orchestrator_factory import create_orchestrator, get_kill_switch
from guardrails.kill_switch import KillSwitch
from models.offline_adapter import OfflineModelAdapter
from models.router import ModelRouter


class BrainCLI:
    def __init__(self) -> None:
        self._orchestrator: Optional[DecisionOrchestrator] = None
        self._running: bool = False
        self._kill_switch: Optional[KillSwitch] = None
        self._active_profile: Optional[str] = None

    def initialize(self) -> None:
        controller = SetupController()
        profile = controller.run()
        self._active_profile = (profile or {}).get("name", "default")

        offline_model = OfflineModelAdapter()
        model_router = ModelRouter(offline_model=offline_model)

        # Use factory to create orchestrator (eliminates duplication)
        self._orchestrator = create_orchestrator(model_router)
        
        # Get kill switch reference for CLI operations
        self._kill_switch = get_kill_switch()
        
        # Check if global kill switch is engaged at startup
        if self._kill_switch.is_global_engaged():
            print("\n⚠️  WARNING: Global kill switch is ENGAGED")
            print("System will refuse all operations until disengaged.")
            print("Type 'kill off' to disengage (use with caution)\n")

    def start(self) -> None:
        if not self._orchestrator:
            self.initialize()

        self._running = True
        profile_label = self._active_profile or "default"
        print(f"\n=== AXON Brain CLI (Phase 1) — profile: {profile_label} ===")
        print("Type 'help' for commands, 'exit' to quit\n")

        while self._running:
            try:
                user_input = input("axon> ").strip()
            except KeyboardInterrupt:
                print("\nUse 'exit' to quit")
                continue

            if not user_input:
                continue

            self._process_input(user_input)

    def stop(self) -> None:
        self._running = False
        print("\nShutting down...")

    def _process_input(self, user_input: str) -> None:
        command = user_input.lower()
        if command in {"exit", "quit", "q"}:
            self.stop()
            return

        if command == "help":
            self._show_help()
            return

        if command == "status":
            self._show_status()
            return

        if command == "kill on":
            self._set_kill_switch(True)
            return

        if command == "kill off":
            self._set_kill_switch(False)
            return
        
        # New: Kill switch status command
        if command == "kill status":
            self._show_kill_switch_status()
            return

        if not self._orchestrator:
            raise RuntimeError("Orchestrator not initialized")

        decision = self._orchestrator.execute_pipeline(
            raw_input=user_input,
            source="human",
            role="developer",
            subject_id="cli_user",
        )

        print(f"\nDecision: {decision.decision}")
        print(f"Risk Level: {decision.risk_level}")
        if decision.response:
            print(f"Response: {decision.response}")
        if decision.veto_reason:
            print(f"Reason: {decision.veto_reason}")
        print()

    def _set_kill_switch(self, engage: bool) -> None:
        if not self._kill_switch:
            print("Kill switch unavailable")
            return
        
        try:
            if engage:
                self._kill_switch.engage_global()
                print("✓ Global kill switch ENGAGED")
                print("All operations will be blocked until disengaged")
            else:
                print("⚠️  WARNING: Disengaging global kill switch")
                print("This will resume all operations")
                
                # Simple confirmation for CLI
                confirm = input("Type 'YES' to confirm: ").strip()
                if confirm == "YES":
                    self._kill_switch.disengage_global()
                    print("✓ Global kill switch DISENGAGED")
                else:
                    print("Disengage cancelled")
        except IOError as e:
            print(f"✗ ERROR: Kill switch operation failed: {e}")
            print("CRITICAL: State may not have persisted")

    def _show_kill_switch_status(self) -> None:
        """Show detailed kill switch status."""
        if not self._kill_switch:
            print("Kill switch unavailable")
            return
        
        from guardrails.kill_switch_verify import print_kill_switch_status
        print()
        print_kill_switch_status(self._kill_switch)
        print()

    def _show_help(self) -> None:
        help_text = """
Available commands:
  help            Show this help message
  status          Show system status
  kill on         Engage global kill switch (blocks all operations)
  kill off        Disengage global kill switch (WARNING: use with caution)
  kill status     Show detailed kill switch status
  exit/quit       Exit AXON

Enter any other text to process through the brain.
        """
        print(help_text)

    def _show_status(self) -> None:
        if self._kill_switch:
            if self._kill_switch.is_global_engaged():
                status = "🔴 ENGAGED"
            else:
                status = "🟢 OFF"
        else:
            status = "UNKNOWN"
        profile_label = self._active_profile or "default"
        print(f"\nPhase 1 Status: Online | Profile: {profile_label} | Kill Switch: {status}\n")
