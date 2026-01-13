# core/brain.py
"""
Core Brain Decision System

Responsibilities:
- Coordinate decision-making components
- Enforce decision pipeline
- Log all decisions to audit trail
- Never bypass policy or risk assessment

This is the central decision coordinator.
It does NOT contain business logic.
It orchestrates policy, risk, and audit components.
"""

from core.identity import Identity
from core.intent import Intent
from core.policy import PolicyEngine
from core.risk import RiskAssessor
from audit.log import AuditLogger

# Risk level constants
RISK_HIGH = "HIGH"
RISK_MEDIUM = "MEDIUM"
RISK_LOW = "LOW"

# Decision constants
DECISION_ALLOW = "ALLOW"
DECISION_CONFIRM = "REQUIRE_CONFIRMATION"
DECISION_REFUSE = "REFUSE"


class BrainDecision:
    """
    Central decision coordinator.
    
    Orchestrates:
    - Policy evaluation
    - Risk assessment
    - Audit logging
    
    Does NOT:
    - Make autonomous decisions
    - Bypass guardrails
    - Generate responses directly
    """

    def __init__(
        self,
        policy_engine: PolicyEngine,
        risk_assessor: RiskAssessor,
        audit_logger: AuditLogger
    ):
        self.policy = policy_engine
        self.risk = risk_assessor
        self.audit = audit_logger

    def decide(self, identity: Identity, intent: Intent) -> str:
        """
        Make a decision based on identity and intent.
        
        Returns one of:
        - "ALLOW"
        - "REQUIRE_CONFIRMATION"
        - "REFUSE"
        
        Always logs decision to audit trail.
        """
        # Pre-decision validation
        if not identity or not intent:
            self.audit.log({
                "source": "system",
                "decision": DECISION_REFUSE,
                "reason": "Invalid identity or intent"
            })
            return DECISION_REFUSE
        
        # Check if action or domain is empty/invalid
        if not intent.action or not intent.domain:
            self.audit.log({
                "source": identity.source,
                "role": identity.role,
                "decision": DECISION_REFUSE,
                "reason": "Missing action or domain"
            })
            return DECISION_REFUSE
        
        policy_result = self.policy.evaluate(intent.action)
        risk_level = self.risk.assess(intent.domain)

        # Compare risk level against identity role ceiling
        # High risk actions require confirmation
        decision = policy_result
        if risk_level == RISK_HIGH and decision == DECISION_ALLOW:
            decision = DECISION_CONFIRM

        self.audit.log({
            "source": identity.source,
            "role": identity.role,
            "action": intent.action,
            "domain": intent.domain,
            "risk": risk_level,
            "decision": decision
        })

        return decision
