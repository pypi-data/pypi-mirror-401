# core/policy.py
"""Policy engine for AXON Phase 1 (deterministic, auditable)."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Sequence, Tuple

import yaml


@dataclass(frozen=True)
class PolicyDecision:
    decision: str
    reason: str
    trace: Tuple[str, ...]


@dataclass(frozen=True)
class PolicyRegistry:
    forbidden: Tuple[str, ...]
    conditional: Tuple[str, ...]
    allowed: Tuple[str, ...]
    default_action: str

    def evaluate(self, action: str, trace: List[str]) -> PolicyDecision:
        if action in self.forbidden:
            trace.append("policy:forbidden")
            return PolicyDecision("REFUSE", "policy.forbidden", tuple(trace))
        if action in self.conditional:
            trace.append("policy:conditional")
            return PolicyDecision(
                "REQUIRE_CONFIRMATION",
                "policy.conditional",
                tuple(trace),
            )
        if action in self.allowed:
            trace.append("policy:allowed")
            return PolicyDecision("ALLOW", "policy.allowed", tuple(trace))
        trace.append("policy:default")
        return PolicyDecision(self.default_action, "policy.default", tuple(trace))


class PolicyEngine:
    """Deterministic evaluator for global policy rules."""

    def __init__(self, policy_path: Path) -> None:
        self.policy_path = policy_path
        policy = self._load_policy(policy_path)
        self.registry = PolicyRegistry(
            forbidden=self._sorted_unique(policy.get("forbidden", ())),
            conditional=self._sorted_unique(policy.get("conditional", ())),
            allowed=self._sorted_unique(policy.get("allowed", ())),
            default_action=(policy.get("rules", {}) or {}).get("default_action", "REFUSE"),
        )

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def evaluate(self, action: str) -> str:
        return self.evaluate_with_trace(action).decision

    def evaluate_with_trace(self, action: str) -> PolicyDecision:
        if not action:
            raise ValueError("Policy evaluation failed: empty action")
        trace = [f"action:{action}"]
        return self.registry.evaluate(action, trace)

    def is_forbidden(self, action: str) -> bool:
        return action in self.registry.forbidden

    def is_allowed(self, action: str) -> bool:
        return action in self.registry.allowed

    def requires_confirmation(self, action: str) -> bool:
        return action in self.registry.conditional

    def get_forbidden_actions(self) -> List[str]:
        return list(self.registry.forbidden)

    def get_allowed_actions(self) -> List[str]:
        return list(self.registry.allowed)

    def get_conditional_actions(self) -> List[str]:
        return list(self.registry.conditional)

    def get_default_action(self) -> str:
        return self.registry.default_action

    def reload(self) -> None:
        policy = self._load_policy(self.policy_path)
        self.registry = PolicyRegistry(
            forbidden=self._sorted_unique(policy.get("forbidden", ())),
            conditional=self._sorted_unique(policy.get("conditional", ())),
            allowed=self._sorted_unique(policy.get("allowed", ())),
            default_action=(policy.get("rules", {}) or {}).get("default_action", "REFUSE"),
        )

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
    @staticmethod
    def _load_policy(path: Path) -> Dict[str, Sequence[str]]:
        if not path.exists():
            raise FileNotFoundError(f"Policy file not found: {path}")
        with open(path, "r", encoding="utf-8") as handle:
            policy = yaml.safe_load(handle)
        if not policy:
            raise ValueError("Policy file is empty or invalid")
        return policy

    @staticmethod
    def _sorted_unique(values: Iterable[str]) -> Tuple[str, ...]:
        return tuple(sorted({*values}))


class PolicyViolation(Exception):
    def __init__(self, action: str, reason: str):
        self.action = action
        self.reason = reason
        super().__init__(f"Policy violation: {action} - {reason}")
