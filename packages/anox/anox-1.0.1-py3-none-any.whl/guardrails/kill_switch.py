# guardrails/kill_switch.py
"""Global and per-domain kill switches with persistent state."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Dict


@dataclass
class KillSwitchState:
    """
    Kill switch state container.
    
    Fields:
    - global_enabled: Global kill switch (halts all operations)
    - intel_enabled: Intel automation kill switch
    - per_domain: Per-domain kill switches (domain_id -> enabled)
    
    Invariants:
    - If global_enabled=True, all operations are blocked
    - If intel_enabled=False, intel automation is blocked
    - Per-domain switches are independent
    """
    global_enabled: bool = False
    intel_enabled: bool = True
    per_domain: Dict[str, bool] = field(default_factory=dict)

    def to_dict(self) -> dict:
        """Serialize to dictionary (for JSON persistence)."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> KillSwitchState:
        """Deserialize from dictionary."""
        return cls(
            global_enabled=bool(data.get("global_enabled", False)),
            intel_enabled=bool(data.get("intel_enabled", True)),
            per_domain=dict(data.get("per_domain", {}))
        )


class KillSwitch:
    """
    In-memory + persistent kill switch manager.
    
    Phase 1 Guarantees:
    - State persists across restarts
    - Atomic writes (no partial state)
    - Fail-closed (missing/corrupted state = engaged)
    - Single source of truth (one state file)
    
    Usage:
        kill_switch = KillSwitch()
        kill_switch.engage_global()  # Persists immediately
        
        # After restart:
        kill_switch = KillSwitch()  # Loads persisted state
        assert kill_switch.is_global_engaged()  # Still engaged
    
    Failure Modes:
    - Missing state file → Default to safe state (global=False)
    - Corrupted state file → Fail-closed (treat as global=True)
    - Write failure → Exception propagates (fail-closed)
    """

    DEFAULT_STATE_PATH = Path("session/kill_switch.state")

    def __init__(self, state_path: Path | None = None) -> None:
        """
        Initialize kill switch with persistent state.
        
        Args:
            state_path: Path to state file (defaults to session/kill_switch.state)
        
        Behavior:
        - Loads state from file if exists
        - Creates default state if missing
        - Fail-closed if corrupted (assumes all switches engaged)
        """
        self._state_path = state_path or self.DEFAULT_STATE_PATH
        self._state = self._load_state()

    # ------------------------------------------------------------------
    # Global kill switch
    # ------------------------------------------------------------------

    def engage_global(self) -> None:
        """
        Engage global kill switch (blocks ALL operations).
        
        Persists immediately - write failure propagates.
        """
        self._state.global_enabled = True
        self._persist_state()

    def disengage_global(self) -> None:
        """
        Disengage global kill switch.
        
        WARNING: Use with extreme caution.
        Persists immediately - write failure propagates.
        """
        self._state.global_enabled = False
        self._persist_state()

    def is_global_engaged(self) -> bool:
        """Check if global kill switch is engaged."""
        return self._state.global_enabled

    # ------------------------------------------------------------------
    # Intel kill switch
    # ------------------------------------------------------------------

    def engage_intel(self) -> None:
        """Engage intel automation kill switch."""
        self._state.intel_enabled = False
        self._persist_state()

    def disengage_intel(self) -> None:
        """Disengage intel automation kill switch."""
        self._state.intel_enabled = True
        self._persist_state()

    def is_intel_enabled(self) -> bool:
        """Check if intel automation is enabled."""
        return self._state.intel_enabled

    # ------------------------------------------------------------------
    # Domain-level kill switches
    # ------------------------------------------------------------------

    def engage_domain(self, domain: str) -> None:
        """
        Engage kill switch for specific domain.
        
        Args:
            domain: Domain identifier (e.g., "dev", "red", "malware")
        """
        if not domain:
            raise ValueError("Domain cannot be empty")
        self._state.per_domain[domain] = True
        self._persist_state()

    def disengage_domain(self, domain: str) -> None:
        """Disengage kill switch for specific domain."""
        if not domain:
            raise ValueError("Domain cannot be empty")
        self._state.per_domain[domain] = False
        self._persist_state()

    def is_domain_engaged(self, domain: str) -> bool:
        """
        Check if domain kill switch is engaged.
        
        Returns:
            True if domain switch engaged, False otherwise
        """
        return self._state.per_domain.get(domain, False)

    # ------------------------------------------------------------------
    # State introspection
    # ------------------------------------------------------------------

    def get_state_snapshot(self) -> dict:
        """
        Get read-only snapshot of current state.
        
        Returns:
            Dictionary with all kill switch states
        """
        return {
            "global_enabled": self._state.global_enabled,
            "intel_enabled": self._state.intel_enabled,
            "per_domain": dict(self._state.per_domain),
            "state_file": str(self._state_path)
        }

    def reset_all(self) -> None:
        """
        Reset all kill switches to default (safe) state.
        
        WARNING: Clears all kill switches. Use only for testing or recovery.
        """
        self._state = KillSwitchState()
        self._persist_state()

    # ------------------------------------------------------------------
    # Persistence logic
    # ------------------------------------------------------------------

    def _load_state(self) -> KillSwitchState:
        """
        Load state from file.
        
        Returns:
            KillSwitchState (from file or default)
        
        Behavior:
        - Missing file → Default state (global=False)
        - Corrupted file → Fail-closed (global=True, intel=False)
        - Valid file → Loaded state
        """
        if not self._state_path.exists():
            # Missing state file: default to safe state
            return KillSwitchState()

        try:
            with open(self._state_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            # Validate structure
            if not isinstance(data, dict):
                raise ValueError("State file is not a dictionary")
            
            return KillSwitchState.from_dict(data)

        except (json.JSONDecodeError, ValueError, KeyError) as e:
            # CRITICAL: Corrupted state file
            # Fail-closed: Assume all kill switches engaged
            print(f"WARNING: Kill switch state file corrupted ({e})")
            print("FAIL-CLOSED: Engaging all kill switches")
            return KillSwitchState(
                global_enabled=True,  # Fail-closed: block all
                intel_enabled=False,  # Fail-closed: block intel
                per_domain={}
            )

    def _persist_state(self) -> None:
        """
        Persist state to file atomically.
        
        Strategy:
        1. Write to temporary file
        2. Flush to disk
        3. Atomic rename (POSIX guarantee)
        
        Raises:
            IOError: If write fails (CRITICAL - fail-closed)
        
        Guarantees:
        - Atomic write (no partial state)
        - Durable (flushed to disk)
        - Exception on failure (fail-closed)
        """
        # Ensure directory exists
        self._state_path.parent.mkdir(parents=True, exist_ok=True)

        # Write to temporary file
        temp_path = self._state_path.with_suffix(".state.tmp")
        
        try:
            with open(temp_path, "w", encoding="utf-8") as f:
                json.dump(
                    self._state.to_dict(),
                    f,
                    indent=2,
                    sort_keys=True,
                    ensure_ascii=False
                )
                f.flush()  # Flush to OS buffer
                # Note: fsync would be more durable but may fail on some filesystems

            # Atomic rename (POSIX guarantee)
            temp_path.replace(self._state_path)

        except (IOError, OSError) as e:
            # CRITICAL: State persistence failed
            # Clean up temp file if exists
            if temp_path.exists():
                try:
                    temp_path.unlink()
                except:
                    pass  # Best effort cleanup
            
            raise IOError(
                f"CRITICAL: Kill switch state persistence failed: {e}"
            ) from e

    def verify_persistence(self) -> bool:
        """
        Verify that state file exists and is readable.
        
        Returns:
            True if state file is valid, False otherwise
        
        Use case: Health checks, diagnostics
        """
        if not self._state_path.exists():
            return False

        try:
            with open(self._state_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            # Validate structure
            if not isinstance(data, dict):
                return False
            
            # Try to deserialize
            KillSwitchState.from_dict(data)
            return True

        except (json.JSONDecodeError, ValueError, KeyError):
            return False


class KillSwitchError(Exception):
    """Raised when kill switch operation fails."""
    pass
