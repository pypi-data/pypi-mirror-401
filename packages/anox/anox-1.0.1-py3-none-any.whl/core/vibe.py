"""Vibe Policy System - Behavioral control for ANOX operations.

Vibe codes control how ANOX behaves during operations. Each vibe has
specific policies about risk, change scope, verbosity, and tool usage.

This is NOT just a parameter - it's a behavioral contract that changes
how the AI brain makes decisions.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any
from typing import Dict
from typing import Optional


class VibeMode(Enum):
    """Available vibe modes for ANOX operations."""
    
    CHILL = "chill"      # Safe, minimal changes, detailed explanations
    FOCUS = "focus"      # Targeted, fix only what's broken
    HACKER = "hacker"    # Aggressive, willing to refactor
    EXPLAIN = "explain"  # No code changes, explanation only


@dataclass
class VibeBehavior:
    """Behavioral contract for a vibe mode."""
    
    # Risk tolerance
    max_risk_level: str  # LOW, MEDIUM, HIGH
    
    # Change scope
    max_files_changed: int  # Maximum files to modify in one operation
    allow_refactor: bool    # Whether refactoring is allowed
    allow_new_files: bool   # Whether creating new files is allowed
    allow_delete: bool      # Whether deleting code is allowed
    
    # Explanation style
    verbosity: str          # minimal, normal, detailed, verbose
    explain_reasoning: bool  # Show reasoning behind changes
    show_alternatives: bool  # Show alternative approaches
    
    # Tool usage
    auto_commit: bool       # Generate commit messages automatically
    require_confirmation: bool  # Require user confirmation before applying
    
    # Performance
    quick_mode: bool        # Optimize for speed over thoroughness


# Vibe Policy Definitions
VIBE_POLICIES: Dict[VibeMode, VibeBehavior] = {
    VibeMode.CHILL: VibeBehavior(
        max_risk_level="LOW",
        max_files_changed=1,
        allow_refactor=False,
        allow_new_files=False,
        allow_delete=False,
        verbosity="detailed",
        explain_reasoning=True,
        show_alternatives=True,
        auto_commit=False,
        require_confirmation=True,
        quick_mode=False,
    ),
    
    VibeMode.FOCUS: VibeBehavior(
        max_risk_level="MEDIUM",
        max_files_changed=3,
        allow_refactor=False,
        allow_new_files=False,
        allow_delete=False,
        verbosity="normal",
        explain_reasoning=True,
        show_alternatives=False,
        auto_commit=True,
        require_confirmation=False,
        quick_mode=True,
    ),
    
    VibeMode.HACKER: VibeBehavior(
        max_risk_level="HIGH",
        max_files_changed=10,
        allow_refactor=True,
        allow_new_files=True,
        allow_delete=True,
        verbosity="normal",
        explain_reasoning=True,
        show_alternatives=False,
        auto_commit=True,
        require_confirmation=False,
        quick_mode=False,
    ),
    
    VibeMode.EXPLAIN: VibeBehavior(
        max_risk_level="NONE",
        max_files_changed=0,
        allow_refactor=False,
        allow_new_files=False,
        allow_delete=False,
        verbosity="verbose",
        explain_reasoning=True,
        show_alternatives=True,
        auto_commit=False,
        require_confirmation=False,
        quick_mode=False,
    ),
}


class VibePolicy:
    """Vibe policy manager - enforces behavioral contracts."""
    
    def __init__(self, mode: VibeMode = VibeMode.FOCUS):
        """Initialize vibe policy with a mode.
        
        Args:
            mode: The vibe mode to use (default: FOCUS)
        """
        self.mode = mode
        self.behavior = VIBE_POLICIES[mode]
    
    @classmethod
    def from_string(cls, vibe_str: str) -> "VibePolicy":
        """Create policy from string representation.
        
        Args:
            vibe_str: String like "chill", "focus", "hacker", "explain"
            
        Returns:
            VibePolicy instance
            
        Raises:
            ValueError: If vibe string is invalid
        """
        try:
            mode = VibeMode(vibe_str.lower())
            return cls(mode)
        except ValueError:
            valid_modes = [v.value for v in VibeMode]
            raise ValueError(
                f"Invalid vibe: {vibe_str}. Must be one of: {valid_modes}"
            )
    
    def can_modify_files(self, file_count: int) -> bool:
        """Check if modifying N files is allowed under this vibe.
        
        Args:
            file_count: Number of files to modify
            
        Returns:
            True if allowed, False otherwise
        """
        return file_count <= self.behavior.max_files_changed
    
    def can_refactor(self) -> bool:
        """Check if refactoring is allowed."""
        return self.behavior.allow_refactor
    
    def can_create_files(self) -> bool:
        """Check if creating new files is allowed."""
        return self.behavior.allow_new_files
    
    def can_delete_code(self) -> bool:
        """Check if deleting code is allowed."""
        return self.behavior.allow_delete
    
    def should_auto_commit(self) -> bool:
        """Check if commit messages should be auto-generated."""
        return self.behavior.auto_commit
    
    def needs_confirmation(self) -> bool:
        """Check if user confirmation is required."""
        return self.behavior.require_confirmation
    
    def get_verbosity(self) -> str:
        """Get explanation verbosity level."""
        return self.behavior.verbosity
    
    def should_show_reasoning(self) -> bool:
        """Check if reasoning should be shown."""
        return self.behavior.explain_reasoning
    
    def should_show_alternatives(self) -> bool:
        """Check if alternatives should be shown."""
        return self.behavior.show_alternatives
    
    def is_quick_mode(self) -> bool:
        """Check if quick mode is enabled."""
        return self.behavior.quick_mode
    
    def get_max_risk(self) -> str:
        """Get maximum risk level."""
        return self.behavior.max_risk_level
    
    def get_max_files_changed(self) -> int:
        """Get maximum number of files that can be changed."""
        return self.behavior.max_files_changed
    
    def enforce_limits(self, proposed_changes: Dict[str, Any]) -> Dict[str, Any]:
        """Enforce vibe limits on proposed changes.
        
        This is the key method that makes vibes "real" - it actively
        constrains what can be done based on the vibe policy.
        
        Args:
            proposed_changes: Dictionary with:
                - files_to_modify: List of file paths
                - needs_refactor: Whether refactoring is needed
                - needs_new_files: Whether new files are needed
                - needs_delete: Whether deletion is needed
                
        Returns:
            Dictionary with:
                - allowed: bool - Whether changes are allowed
                - reason: str - Why changes were blocked (if blocked)
                - limited_files: List of files after applying limits
        """
        files = proposed_changes.get("files_to_modify", [])
        needs_refactor = proposed_changes.get("needs_refactor", False)
        needs_new_files = proposed_changes.get("needs_new_files", False)
        needs_delete = proposed_changes.get("needs_delete", False)
        
        # EXPLAIN mode: block ALL changes
        if self.mode == VibeMode.EXPLAIN:
            if files:
                return {
                    "allowed": False,
                    "reason": "EXPLAIN mode does not allow code modifications",
                    "limited_files": [],
                }
        
        # Check file count limits
        if len(files) > self.behavior.max_files_changed:
            return {
                "allowed": False,
                "reason": f"{self.mode.value} mode allows max {self.behavior.max_files_changed} files, but {len(files)} files would be modified",
                "limited_files": files[:self.behavior.max_files_changed],
            }
        
        # Check refactoring permission
        if needs_refactor and not self.behavior.allow_refactor:
            return {
                "allowed": False,
                "reason": f"{self.mode.value} mode does not allow refactoring",
                "limited_files": [],
            }
        
        # Check new file permission
        if needs_new_files and not self.behavior.allow_new_files:
            return {
                "allowed": False,
                "reason": f"{self.mode.value} mode does not allow creating new files",
                "limited_files": [],
            }
        
        # Check delete permission
        if needs_delete and not self.behavior.allow_delete:
            return {
                "allowed": False,
                "reason": f"{self.mode.value} mode does not allow deleting code",
                "limited_files": [],
            }
        
        # All checks passed
        return {
            "allowed": True,
            "reason": "Changes allowed by vibe policy",
            "limited_files": files,
        }
    
    def get_confidence_level(self) -> str:
        """Get how confident/aggressive the AI should be.
        
        Returns:
            Confidence level: cautious, balanced, confident, aggressive
        """
        if self.mode == VibeMode.CHILL:
            return "cautious"
        elif self.mode == VibeMode.FOCUS:
            return "balanced"
        elif self.mode == VibeMode.HACKER:
            return "aggressive"
        else:  # EXPLAIN
            return "analytical"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert policy to dictionary.
        
        Returns:
            Dictionary representation of the policy
        """
        return {
            "mode": self.mode.value,
            "behavior": {
                "max_risk_level": self.behavior.max_risk_level,
                "max_files_changed": self.behavior.max_files_changed,
                "allow_refactor": self.behavior.allow_refactor,
                "allow_new_files": self.behavior.allow_new_files,
                "allow_delete": self.behavior.allow_delete,
                "verbosity": self.behavior.verbosity,
                "explain_reasoning": self.behavior.explain_reasoning,
                "show_alternatives": self.behavior.show_alternatives,
                "auto_commit": self.behavior.auto_commit,
                "require_confirmation": self.behavior.require_confirmation,
                "quick_mode": self.behavior.quick_mode,
            }
        }
    
    def __str__(self) -> str:
        """String representation of the policy."""
        return f"VibePolicy({self.mode.value})"
    
    def __repr__(self) -> str:
        """Detailed string representation."""
        return f"VibePolicy(mode={self.mode.value}, behavior={self.behavior})"


def get_vibe_description(mode: VibeMode) -> str:
    """Get human-readable description of a vibe mode.
    
    Args:
        mode: The vibe mode
        
    Returns:
        Description string
    """
    descriptions = {
        VibeMode.CHILL: "🌊 Safe, minimal changes, detailed explanations. Best for critical code.",
        VibeMode.FOCUS: "🎯 Targeted fixes only. Quick and precise. Best for bug fixing.",
        VibeMode.HACKER: "⚡ Aggressive refactoring allowed. Best for major improvements.",
        VibeMode.EXPLAIN: "📚 No code changes. Explanation only. Best for learning.",
    }
    return descriptions[mode]


def list_all_vibes() -> str:
    """Get formatted list of all available vibes.
    
    Returns:
        Formatted string with all vibes and their descriptions
    """
    lines = ["Available Vibe Modes:", ""]
    for mode in VibeMode:
        desc = get_vibe_description(mode)
        lines.append(f"  {mode.value:8} - {desc}")
    return "\n".join(lines)
