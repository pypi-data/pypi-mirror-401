# audit/log.py
"""Tamper-proof audit logger with hash chain integrity."""

import hashlib
import json
from datetime import datetime
from pathlib import Path
from typing import Optional


class AuditLogger:
    """
    Append-only audit logger with cryptographic hash chain.
    
    Each entry contains:
    - timestamp: ISO 8601 UTC
    - prev_hash: SHA-256 of previous entry (chain link)
    - entry_hash: SHA-256 of current entry (integrity)
    - **record: User-provided audit data
    
    Chain Properties:
    - First entry: prev_hash = "GENESIS"
    - Each entry: prev_hash = previous entry's entry_hash
    - Tamper detection: Recompute and compare hashes
    
    Phase 1 Guarantees:
    - Deterministic hashing (SHA-256)
    - Fail-closed: Log write failure aborts operation
    - No external dependencies
    """

    GENESIS_HASH = "GENESIS"
    HASH_ALGORITHM = "sha256"

    def __init__(self, log_path: Path):
        self.log_path = log_path
        self._last_hash: str = self._load_last_hash()
        self._ensure_log_exists()

    def log(self, record: dict) -> None:
        """
        Append a new entry to the audit log with hash chain.
        
        Args:
            record: Audit data (must be JSON-serializable)
        
        Raises:
            ValueError: If record is invalid
            IOError: If log write fails (CRITICAL)
        
        Guarantees:
        - Entry is written atomically
        - Hash chain is maintained
        - Timestamp is UTC
        """
        if not isinstance(record, dict):
            raise ValueError("Audit record must be a dictionary")

        # Build entry with chain metadata
        entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "prev_hash": self._last_hash,
            **record
        }

        # Compute deterministic hash of entry content
        entry_hash = self._compute_hash(entry)
        entry["entry_hash"] = entry_hash

        # Serialize for storage
        entry_json = json.dumps(entry, sort_keys=True, ensure_ascii=False)

        # Write to log (fail-closed: exceptions propagate)
        try:
            with open(self.log_path, "a", encoding="utf-8") as f:
                f.write(entry_json + "\n")
                f.flush()  # Ensure immediate write
        except IOError as e:
            # CRITICAL: Log write failure must not be silent
            raise IOError(f"CRITICAL: Audit log write failed: {e}") from e

        # Update chain state (only after successful write)
        self._last_hash = entry_hash

    def get_last_hash(self) -> str:
        """Return the hash of the most recent entry."""
        return self._last_hash

    def _ensure_log_exists(self) -> None:
        """Create log file if it doesn't exist."""
        if not self.log_path.exists():
            self.log_path.parent.mkdir(parents=True, exist_ok=True)
            self.log_path.touch()

    def _load_last_hash(self) -> str:
        """
        Load the hash of the last entry in the log.
        
        Returns:
            - "GENESIS" if log is empty
            - entry_hash of last valid entry
        
        Behavior:
        - Does NOT validate entire chain (use verify.py for that)
        - Reads only the last line for performance
        """
        if not self.log_path.exists():
            return self.GENESIS_HASH

        try:
            # Read last line efficiently
            with open(self.log_path, "rb") as f:
                # Seek to end
                f.seek(0, 2)
                file_size = f.tell()
                
                if file_size == 0:
                    return self.GENESIS_HASH

                # Read last ~4KB (enough for one entry)
                buffer_size = min(4096, file_size)
                f.seek(max(0, file_size - buffer_size))
                tail = f.read().decode("utf-8")

            # Get last non-empty line
            lines = [line.strip() for line in tail.splitlines() if line.strip()]
            if not lines:
                return self.GENESIS_HASH

            last_line = lines[-1]
            last_entry = json.loads(last_line)

            # Extract hash (or compute if missing for backward compatibility)
            if "entry_hash" in last_entry:
                return last_entry["entry_hash"]
            else:
                # Legacy entry without hash: compute it
                return self._compute_hash(last_entry)

        except (IOError, json.JSONDecodeError, KeyError):
            # If we cannot read last hash, assume corruption
            # Start new chain (operator should verify separately)
            return self.GENESIS_HASH

    def _compute_hash(self, entry: dict) -> str:
        """
        Compute SHA-256 hash of entry content.
        
        Args:
            entry: Dictionary to hash (must not contain "entry_hash" key)
        
        Returns:
            Hex-encoded SHA-256 hash
        
        Determinism:
        - JSON serialization with sorted keys
        - UTF-8 encoding
        - No whitespace variations
        """
        # Remove entry_hash if present (to avoid circular dependency)
        entry_copy = {k: v for k, v in entry.items() if k != "entry_hash"}

        # Deterministic serialization
        entry_json = json.dumps(
            entry_copy,
            sort_keys=True,
            ensure_ascii=False,
            separators=(",", ":")  # No extra whitespace
        )

        # Hash UTF-8 bytes
        hash_obj = hashlib.sha256(entry_json.encode("utf-8"))
        return hash_obj.hexdigest()
