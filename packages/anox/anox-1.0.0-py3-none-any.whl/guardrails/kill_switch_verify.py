# guardrails/kill_switch_verify.py
"""Kill switch state verification and recovery utilities."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

from guardrails.kill_switch import KillSwitch, KillSwitchState


def verify_state_file(state_path: Path) -> tuple[bool, str]:
    """
    Verify kill switch state file integrity.
    
    Args:
        state_path: Path to state file
    
    Returns:
        (valid, reason) tuple
        - valid: True if file is valid
        - reason: Explanation of validity/invalidity
    
    Checks:
    1. File exists
    2. Valid JSON
    3. Expected structure
    4. Boolean types correct
    """
    if not state_path.exists():
        return False, "State file does not exist"

    try:
        with open(state_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        return False, f"Invalid JSON: {e}"
    except IOError as e:
        return False, f"Cannot read file: {e}"

    # Check structure
    if not isinstance(data, dict):
        return False, "State file is not a dictionary"

    # Check required fields exist and have correct types
    if "global_enabled" in data and not isinstance(data["global_enabled"], bool):
        return False, "global_enabled must be boolean"

    if "intel_enabled" in data and not isinstance(data["intel_enabled"], bool):
        return False, "intel_enabled must be boolean"

    if "per_domain" in data:
        if not isinstance(data["per_domain"], dict):
            return False, "per_domain must be dictionary"
        
        # Check all domain values are boolean
        for domain, enabled in data["per_domain"].items():
            if not isinstance(enabled, bool):
                return False, f"per_domain[{domain}] must be boolean"

    # Try to deserialize
    try:
        KillSwitchState.from_dict(data)
    except Exception as e:
        return False, f"Cannot deserialize state: {e}"

    return True, "State file is valid"


def check_kill_switch_health(kill_switch: KillSwitch) -> dict:
    """
    Get health status of kill switch system.
    
    Args:
        kill_switch: KillSwitch instance
    
    Returns:
        Health report dictionary with:
        - healthy: bool
        - state_file_exists: bool
        - state_file_valid: bool
        - current_state: dict
        - issues: list of problems
    """
    state_path = kill_switch._state_path
    issues = []

    # Check state file existence
    state_file_exists = state_path.exists()
    if not state_file_exists:
        issues.append("State file does not exist (will be created on first change)")

    # Check state file validity
    state_file_valid = False
    if state_file_exists:
        valid, reason = verify_state_file(state_path)
        state_file_valid = valid
        if not valid:
            issues.append(f"State file invalid: {reason}")

    # Get current state
    current_state = kill_switch.get_state_snapshot()

    # Check for suspicious states
    if current_state["global_enabled"]:
        issues.append("ALERT: Global kill switch is ENGAGED")

    if not current_state["intel_enabled"]:
        issues.append("INFO: Intel automation is disabled")

    engaged_domains = [
        domain for domain, enabled in current_state["per_domain"].items()
        if enabled
    ]
    if engaged_domains:
        issues.append(f"INFO: Domain kill switches engaged: {', '.join(engaged_domains)}")

    healthy = state_file_valid and len([i for i in issues if i.startswith("ALERT")]) == 0

    return {
        "healthy": healthy,
        "state_file_exists": state_file_exists,
        "state_file_valid": state_file_valid,
        "current_state": current_state,
        "issues": issues
    }


def recover_state_file(
    state_path: Path,
    backup_path: Optional[Path] = None,
    safe_state: bool = True
) -> bool:
    """
    Recover corrupted kill switch state file.
    
    Args:
        state_path: Path to corrupted state file
        backup_path: Optional backup location for corrupted file
        safe_state: If True, create fail-closed state (all engaged)
                   If False, create default state (all disengaged)
    
    Returns:
        True if recovery successful
    
    Strategy:
    1. Backup corrupted file (if requested)
    2. Create new state with safe defaults
    3. Verify new state
    
    WARNING: This will reset all kill switch states!
    """
    # Backup corrupted file
    if backup_path and state_path.exists():
        try:
            import shutil
            shutil.copy2(state_path, backup_path)
            print(f"Corrupted state backed up to: {backup_path}")
        except IOError as e:
            print(f"WARNING: Could not backup corrupted state: {e}")

    # Create safe state
    if safe_state:
        # Fail-closed: Engage all switches
        new_state = KillSwitchState(
            global_enabled=True,
            intel_enabled=False,
            per_domain={}
        )
        print("Creating fail-closed state (all switches ENGAGED)")
    else:
        # Default: Disengage all switches
        new_state = KillSwitchState()
        print("Creating default state (all switches OFF)")

    # Write new state
    try:
        state_path.parent.mkdir(parents=True, exist_ok=True)
        with open(state_path, "w", encoding="utf-8") as f:
            json.dump(new_state.to_dict(), f, indent=2, sort_keys=True)
        print(f"New state file created: {state_path}")
    except IOError as e:
        print(f"ERROR: Could not create new state file: {e}")
        return False

    # Verify recovery
    valid, reason = verify_state_file(state_path)
    if valid:
        print("✓ Recovery successful")
        return True
    else:
        print(f"✗ Recovery failed: {reason}")
        return False


def print_kill_switch_status(kill_switch: KillSwitch) -> None:
    """
    Print human-readable kill switch status.
    
    Args:
        kill_switch: KillSwitch instance
    
    Output:
        Status report to stdout
    """
    state = kill_switch.get_state_snapshot()

    print("=== Kill Switch Status ===")
    print()
    print(f"Global Kill Switch:  {'🔴 ENGAGED' if state['global_enabled'] else '🟢 OFF'}")
    print(f"Intel Automation:    {'🟢 ENABLED' if state['intel_enabled'] else '🔴 DISABLED'}")
    print()

    if state["per_domain"]:
        print("Domain Kill Switches:")
        for domain, enabled in sorted(state["per_domain"].items()):
            status = "🔴 ENGAGED" if enabled else "🟢 OFF"
            print(f"  {domain:15} {status}")
    else:
        print("Domain Kill Switches: None configured")

    print()
    print(f"State File: {state['state_file']}")

    # Check health
    health = check_kill_switch_health(kill_switch)
    if health["healthy"]:
        print("Health: ✓ OK")
    else:
        print("Health: ✗ ISSUES DETECTED")
        for issue in health["issues"]:
            print(f"  - {issue}")


def force_engage_all(kill_switch: KillSwitch) -> None:
    """
    Emergency function: Engage ALL kill switches.
    
    Args:
        kill_switch: KillSwitch instance
    
    Use case: Security incident, manual shutdown
    
    WARNING: This will block ALL operations!
    """
    print("⚠️  ENGAGING ALL KILL SWITCHES")
    
    kill_switch.engage_global()
    print("✓ Global kill switch ENGAGED")
    
    kill_switch.engage_intel()
    print("✓ Intel automation DISABLED")
    
    # Note: Per-domain switches not needed when global is engaged,
    # but we could engage known domains for explicitness
    
    print("✓ All kill switches engaged - system halted")


def force_disengage_all(kill_switch: KillSwitch, confirm: bool = False) -> None:
    """
    Emergency function: Disengage ALL kill switches.
    
    Args:
        kill_switch: KillSwitch instance
        confirm: Must be True to proceed (safety check)
    
    Use case: Recovery after false alarm
    
    WARNING: Use with extreme caution!
    """
    if not confirm:
        print("ERROR: Must explicitly confirm to disengage all kill switches")
        print("Call with confirm=True if you are certain")
        return

    print("⚠️  DISENGAGING ALL KILL SWITCHES")
    print("This will resume all operations!")
    
    kill_switch.disengage_global()
    print("✓ Global kill switch disengaged")
    
    kill_switch.disengage_intel()
    print("✓ Intel automation enabled")
    
    # Clear all domain switches
    state = kill_switch.get_state_snapshot()
    for domain in state["per_domain"]:
        if state["per_domain"][domain]:
            kill_switch.disengage_domain(domain)
            print(f"✓ Domain '{domain}' kill switch disengaged")
    
    print("✓ All kill switches disengaged - system operational")
