# audit/integrity.py
"""Audit log integrity checking utilities."""

from pathlib import Path
from typing import Optional

from audit.verify import AuditVerifier, VerificationResult


def check_integrity(log_path: Path, verbose: bool = False) -> bool:
    """
    Check audit log integrity and print results.
    
    Args:
        log_path: Path to audit log file
        verbose: Print detailed findings
    
    Returns:
        True if log is valid, False if corrupted
    
    Usage:
        from audit.integrity import check_integrity
        
        if not check_integrity(Path("logs/brain.log")):
            print("WARNING: Audit log corruption detected!")
    """
    verifier = AuditVerifier(log_path)
    result = verifier.verify()

    if verbose or not result.valid:
        print(str(result))
        if result.details and not result.valid:
            print("\nDetails:")
            print(result.details)

    return result.valid


def recover_to_last_valid(
    log_path: Path,
    backup_path: Optional[Path] = None
) -> bool:
    """
    Recover audit log by truncating to last valid entry.
    
    WARNING: This is a destructive operation!
    
    Args:
        log_path: Path to corrupted audit log
        backup_path: Optional path to save corrupted log
    
    Returns:
        True if recovery successful, False if log is entirely corrupted
    
    Process:
        1. Find last valid entry
        2. Backup corrupted log (if backup_path provided)
        3. Truncate log to last valid entry
        4. Verify truncated log
    
    Usage:
        from audit.integrity import recover_to_last_valid
        
        backup = Path("logs/brain.log.corrupted")
        if recover_to_last_valid(Path("logs/brain.log"), backup):
            print("Recovery successful")
        else:
            print("Log is entirely corrupted - manual intervention required")
    """
    verifier = AuditVerifier(log_path)
    
    # Find last valid entry
    last_valid = verifier.get_last_valid_entry()
    
    if last_valid is None:
        print("ERROR: No valid entries found - cannot recover")
        return False

    # Backup corrupted log
    if backup_path:
        import shutil
        shutil.copy2(log_path, backup_path)
        print(f"Corrupted log backed up to: {backup_path}")

    # Reconstruct log with valid entries only
    valid_entries = []
    for entry in verifier._read_entries():
        valid_entries.append(entry)
        if entry.get("entry_hash") == last_valid["entry_hash"]:
            break  # Stop at last valid entry

    # Write truncated log
    import json
    with open(log_path, "w", encoding="utf-8") as f:
        for entry in valid_entries:
            f.write(json.dumps(entry, sort_keys=True, ensure_ascii=False) + "\n")

    # Verify recovery
    recovery_result = verifier.verify()
    if recovery_result.valid:
        print(f"✓ Recovery successful - log truncated to {len(valid_entries)} entries")
        return True
    else:
        print("✗ Recovery failed - log still corrupted")
        return False


def get_chain_summary(log_path: Path) -> dict:
    """
    Get summary statistics about audit log chain.
    
    Returns:
        {
            "total_entries": int,
            "first_timestamp": str,
            "last_timestamp": str,
            "first_hash": str,
            "last_hash": str,
            "chain_valid": bool
        }
    
    Usage:
        from audit.integrity import get_chain_summary
        
        summary = get_chain_summary(Path("logs/brain.log"))
        print(f"Log contains {summary['total_entries']} entries")
        print(f"Chain valid: {summary['chain_valid']}")
    """
    verifier = AuditVerifier(log_path)
    result = verifier.verify()

    first_entry = None
    last_entry = None
    
    for entry in verifier._read_entries():
        if first_entry is None:
            first_entry = entry
        last_entry = entry

    return {
        "total_entries": result.total_entries,
        "first_timestamp": first_entry.get("timestamp", "N/A") if first_entry else "N/A",
        "last_timestamp": last_entry.get("timestamp", "N/A") if last_entry else "N/A",
        "first_hash": first_entry.get("entry_hash", "N/A")[:16] + "..." if first_entry else "N/A",
        "last_hash": last_entry.get("entry_hash", "N/A")[:16] + "..." if last_entry else "N/A",
        "chain_valid": result.valid,
        "corrupted_count": len(result.corrupted_entries),
        "chain_breaks": len(result.chain_breaks)
    }
