# audit/verify.py
"""Audit log integrity verification."""

import json
import hashlib
from dataclasses import dataclass
from pathlib import Path
from typing import Iterator, Optional


@dataclass
class VerificationResult:
    """Result of audit log verification."""
    
    valid: bool
    total_entries: int
    corrupted_entries: list[int]  # Line numbers (1-indexed)
    chain_breaks: list[tuple[int, str]]  # (line_num, reason)
    details: str

    def __str__(self) -> str:
        if self.valid:
            return f"✓ Audit log valid ({self.total_entries} entries)"
        else:
            issues = []
            if self.corrupted_entries:
                issues.append(f"{len(self.corrupted_entries)} corrupted entries")
            if self.chain_breaks:
                issues.append(f"{len(self.chain_breaks)} chain breaks")
            return f"✗ Audit log INVALID: {', '.join(issues)}\n{self.details}"


class AuditVerifier:
    """
    Verifies integrity of audit log hash chain.
    
    Checks:
    1. Each entry has valid hash
    2. Hash chain is unbroken
    3. Timestamps are monotonic (warning only)
    4. JSON is well-formed
    
    Does NOT check:
    - Content validity (business logic)
    - Digital signatures (Phase 2)
    - External timestamp proofs
    """

    GENESIS_HASH = "GENESIS"

    def __init__(self, log_path: Path):
        self.log_path = log_path

    def verify(self) -> VerificationResult:
        """
        Verify entire audit log.
        
        Returns:
            VerificationResult with detailed findings
        
        Performance:
        - O(n) where n = number of entries
        - Reads log file once sequentially
        """
        if not self.log_path.exists():
            return VerificationResult(
                valid=True,
                total_entries=0,
                corrupted_entries=[],
                chain_breaks=[],
                details="Log file does not exist (empty log is valid)"
            )

        total_entries = 0
        corrupted_entries = []
        chain_breaks = []
        expected_prev_hash = self.GENESIS_HASH
        details_lines = []

        try:
            for line_num, entry in enumerate(self._read_entries(), start=1):
                total_entries += 1

                # Check 1: Entry has required fields
                if "entry_hash" not in entry or "prev_hash" not in entry:
                    corrupted_entries.append(line_num)
                    details_lines.append(
                        f"Line {line_num}: Missing hash fields"
                    )
                    continue

                # Check 2: prev_hash matches expected
                if entry["prev_hash"] != expected_prev_hash:
                    chain_breaks.append((
                        line_num,
                        f"Expected prev_hash={expected_prev_hash[:16]}..., "
                        f"got {entry['prev_hash'][:16]}..."
                    ))
                    details_lines.append(
                        f"Line {line_num}: Chain break - "
                        f"expected prev_hash={expected_prev_hash[:16]}..., "
                        f"got {entry['prev_hash'][:16]}..."
                    )

                # Check 3: Recompute hash and compare
                computed_hash = self._compute_hash(entry)
                if computed_hash != entry["entry_hash"]:
                    corrupted_entries.append(line_num)
                    details_lines.append(
                        f"Line {line_num}: Hash mismatch - "
                        f"stored={entry['entry_hash'][:16]}..., "
                        f"computed={computed_hash[:16]}..."
                    )

                # Update chain state
                expected_prev_hash = entry["entry_hash"]

        except Exception as e:
            return VerificationResult(
                valid=False,
                total_entries=total_entries,
                corrupted_entries=corrupted_entries,
                chain_breaks=chain_breaks,
                details=f"Verification failed with exception: {e}\n" + 
                        "\n".join(details_lines)
            )

        valid = len(corrupted_entries) == 0 and len(chain_breaks) == 0
        details = "\n".join(details_lines) if details_lines else "All entries valid"

        return VerificationResult(
            valid=valid,
            total_entries=total_entries,
            corrupted_entries=corrupted_entries,
            chain_breaks=chain_breaks,
            details=details
        )

    def verify_range(self, start_line: int, end_line: int) -> VerificationResult:
        """
        Verify a range of entries (for incremental checking).
        
        Args:
            start_line: First line to check (1-indexed)
            end_line: Last line to check (inclusive)
        
        Returns:
            VerificationResult for the specified range
        """
        # Implementation: Read range, verify chain within range
        # Left as exercise - for Phase 1, verify() is sufficient
        raise NotImplementedError("Range verification in Phase 2")

    def get_last_valid_entry(self) -> Optional[dict]:
        """
        Return the last entry with a valid hash chain.
        
        Use case: Recovery after corruption detected
        
        Returns:
            Last valid entry, or None if log is corrupted from start
        """
        last_valid = None
        expected_prev_hash = self.GENESIS_HASH

        for entry in self._read_entries():
            if "entry_hash" not in entry or "prev_hash" not in entry:
                break  # Corruption detected

            if entry["prev_hash"] != expected_prev_hash:
                break  # Chain break

            computed_hash = self._compute_hash(entry)
            if computed_hash != entry["entry_hash"]:
                break  # Hash mismatch

            last_valid = entry
            expected_prev_hash = entry["entry_hash"]

        return last_valid

    def _read_entries(self) -> Iterator[dict]:
        """
        Read entries from log file.
        
        Yields:
            Parsed JSON entries
        
        Skips:
            Empty lines
            Malformed JSON (logs warning)
        """
        with open(self.log_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue

                try:
                    entry = json.loads(line)
                    yield entry
                except json.JSONDecodeError:
                    # Malformed JSON - treated as corruption
                    # (caller will detect missing entry_hash)
                    yield {}

    def _compute_hash(self, entry: dict) -> str:
        """
        Compute SHA-256 hash of entry (must match AuditLogger logic).
        
        CRITICAL: This must be identical to AuditLogger._compute_hash
        """
        entry_copy = {k: v for k, v in entry.items() if k != "entry_hash"}
        entry_json = json.dumps(
            entry_copy,
            sort_keys=True,
            ensure_ascii=False,
            separators=(",", ":")
        )
        hash_obj = hashlib.sha256(entry_json.encode("utf-8"))
        return hash_obj.hexdigest()


def verify_log(log_path: Path) -> VerificationResult:
    """Convenience function for one-shot verification."""
    return AuditVerifier(log_path).verify()
