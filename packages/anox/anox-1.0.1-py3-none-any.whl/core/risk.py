# core/risk.py
"""Deterministic risk assessment for AXON Phase 1."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Dict, Iterable, List, Sequence, Tuple


class RiskLevel(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

    @property
    def weight(self) -> int:
        return {
            RiskLevel.LOW: 1,
            RiskLevel.MEDIUM: 2,
            RiskLevel.HIGH: 3,
            RiskLevel.CRITICAL: 4,
        }[self]


@dataclass(frozen=True)
class RiskDecision:
    level: RiskLevel
    reason: str
    trace: Tuple[str, ...]

    def requires_confirmation(self, role_ceiling: RiskLevel | None = None) -> bool:
        if self.level in (RiskLevel.HIGH, RiskLevel.CRITICAL):
            return True
        if role_ceiling and self.level.weight > role_ceiling.weight:
            return True
        return False


class RiskAssessor:
    """Rule-based risk scoring engine."""

    BASE_DOMAIN_RISK: Dict[str, RiskLevel] = {
        "dev": RiskLevel.LOW,
        "data": RiskLevel.LOW,
        "cloud": RiskLevel.MEDIUM,
        "blue": RiskLevel.MEDIUM,
        "read_only": RiskLevel.LOW,
        "red": RiskLevel.HIGH,
        "malware": RiskLevel.HIGH,
    }

    ACTION_OVERRIDES: Dict[str, RiskLevel] = {
        "auto_execute_attack": RiskLevel.CRITICAL,
        "real_world_exploitation": RiskLevel.CRITICAL,
        "malware_execution": RiskLevel.CRITICAL,
        "bypass_authorization": RiskLevel.CRITICAL,
        "disable_audit_logging": RiskLevel.CRITICAL,
        "hidden_or_unaudited_actions": RiskLevel.CRITICAL,
        "self_modifying_policy": RiskLevel.CRITICAL,
        "red_team_vulnerability_analysis": RiskLevel.HIGH,
        "exploit_patterns_non_operational": RiskLevel.HIGH,
        "malware_structure_analysis_static": RiskLevel.HIGH,
        "security_sensitive_code_generation": RiskLevel.HIGH,
        "system_configuration_change": RiskLevel.MEDIUM,
    }

    PASSIVE_REDUCTION = 1  # subtract one weight level for passive intents

    def assess(self, domain: str, action: str, passive: bool) -> RiskDecision:
        trace: List[str] = [
            f"domain:{domain}",
            f"action:{action}",
            f"passive:{passive}",
        ]

        base_level = self.BASE_DOMAIN_RISK.get(domain, RiskLevel.MEDIUM)
        trace.append(f"domain_base:{base_level.value}")

        action_override = self.ACTION_OVERRIDES.get(action)
        if action_override:
            trace.append(f"action_override:{action_override.value}")
            level = action_override
        else:
            level = base_level

        if passive and level != RiskLevel.LOW:
            reduced_weight = max(1, level.weight - self.PASSIVE_REDUCTION)
            level = self._level_from_weight(reduced_weight)
            trace.append("passive:reduced")

        trace.append(f"final:{level.value}")
        return RiskDecision(level=level, reason="risk.assessed", trace=tuple(trace))

    def assess_multi_factor(
        self,
        domain: str,
        action: str,
        passive: bool,
        tools: Sequence[str] | None = None,
    ) -> RiskDecision:
        return self.assess(domain, action, passive)

    @staticmethod
    def aggregate(decisions: Iterable[RiskDecision]) -> RiskDecision:
        decisions = list(decisions)
        if not decisions:
            return RiskDecision(RiskLevel.LOW, "risk.aggregate.none", ("aggregate:none",))
        highest = max(decisions, key=lambda d: d.level.weight)
        trace = tuple(["aggregate"] + [f"include:{d.level.value}" for d in decisions])
        return RiskDecision(highest.level, "risk.aggregate.max", trace)

    @staticmethod
    def _level_from_weight(weight: int) -> RiskLevel:
        mapping = {
            1: RiskLevel.LOW,
            2: RiskLevel.MEDIUM,
            3: RiskLevel.HIGH,
            4: RiskLevel.CRITICAL,
        }
        return mapping.get(max(1, min(4, weight)), RiskLevel.CRITICAL)
