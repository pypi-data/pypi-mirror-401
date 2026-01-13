# core/orchestrator.py
"""Phase 1 decision orchestrator (rule-based, auditable)."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from audit.log import AuditLogger
from core.identity import Identity, IdentityResolver
from core.intent import Intent, IntentClassifier
from core.planner import ExecutionPlan, Planner
from core.policy import PolicyDecision, PolicyEngine
from core.risk import RiskAssessor, RiskDecision, RiskLevel
from core.executor import TaskExecutor, ExecutionResult
from domains._boundary import BoundaryValidator
from domains._enforcer import DomainDecision, DomainEnforcer
from guardrails.kill_switch import KillSwitch
from guardrails.roles_registry import RoleDefinition, RoleRegistry
from memory.short_term import ShortTermMemory
from memory.task_memory import TaskMemory, TaskMemoryEntry
from memory.working_memory import WorkingMemory
from models.base import BaseModel
from models.router import ModelRouter


@dataclass
class OrchestratorDecision:
    decision: str
    identity: Identity
    intent: Intent
    risk_level: str
    response: Optional[str] = None
    veto_reason: Optional[str] = None
    decision_trace: tuple[str, ...] = tuple()
    execution_result: Optional[ExecutionResult] = None  # Added to track task execution


class DecisionOrchestrator:
    """Coordinates the Phase 1 rule-based pipeline."""

    def __init__(
        self,
        *,
        identity_resolver: IdentityResolver,
        intent_classifier: IntentClassifier,
        policy_engine: PolicyEngine,
        risk_assessor: RiskAssessor,
        planner: Planner,
        task_executor: TaskExecutor,
        model_router: ModelRouter,
        short_term_memory: ShortTermMemory,
        working_memory: WorkingMemory,
        task_memory: TaskMemory,
        audit_logger: AuditLogger,
        kill_switch: Optional[KillSwitch] = None,
        role_registry: Optional[RoleRegistry] = None,
        domains_path: Optional[Path] = None,
    ) -> None:
        self.identity_resolver = identity_resolver
        self.intent_classifier = intent_classifier
        self.policy = policy_engine
        self.risk = risk_assessor
        self.planner = planner
        self.executor = task_executor
        self.model_router = model_router
        self.short_term_memory = short_term_memory
        self.working_memory = working_memory
        self.task_memory = task_memory
        self.audit = audit_logger
        self.kill_switch = kill_switch
        self.role_registry = role_registry
        self.domain_enforcer: Optional[DomainEnforcer] = None
        if domains_path:
            boundary_validator = BoundaryValidator(domains_path)
            self.domain_enforcer = DomainEnforcer(domains_path, boundary_validator)

    # ------------------------------------------------------------------
    def execute_pipeline(
        self,
        raw_input: str,
        source: str,
        role: str,
        subject_id: Optional[str] = None,
    ) -> OrchestratorDecision:
        trace: list[str] = []
        if self.kill_switch and self.kill_switch.is_global_engaged():
            trace.append("kill_switch:engaged")
            return self._veto("KILL_SWITCH_ENGAGED", "Global kill switch engaged", trace=trace)

        user_input = raw_input.strip()
        try:
            self._validate_input(user_input)
        except ValueError as exc:
            trace.append("input:invalid")
            return self._veto("INPUT_INVALID", str(exc), trace=trace)
        trace.append("input:valid")

        try:
            identity = self.identity_resolver.resolve(source, role, subject_id)
        except ValueError as exc:
            trace.append("identity:invalid")
            return self._veto("IDENTITY_INVALID", str(exc), trace=trace)
        trace.append(f"identity:{identity.role}")

        role_definition: Optional[RoleDefinition] = None
        if self.role_registry:
            try:
                role_definition = self.role_registry.get(identity.role)
                trace.append("role_registry:resolved")
            except ValueError as exc:
                trace.append("role_registry:unknown")
                return self._veto("ROLE_UNKNOWN", str(exc), identity=identity, trace=trace)

        try:
            intent = self.intent_classifier.classify(user_input)
        except ValueError as exc:
            trace.append("intent:invalid")
            return self._veto("INTENT_INVALID", str(exc), identity=identity, trace=trace)
        trace.extend(intent.decision_trace)

        domain_decision = self._evaluate_domain(intent, identity.role)
        trace.extend(domain_decision.trace)
        if domain_decision.decision == "REFUSE":
            return self._veto(
                "DOMAIN_FORBIDDEN",
                domain_decision.reason,
                identity=identity,
                intent=intent,
                trace=trace,
            )

        policy_decision = self.policy.evaluate_with_trace(intent.action)
        trace.extend(policy_decision.trace)
        if policy_decision.decision == "REFUSE":
            return self._veto(
                "POLICY_FORBIDDEN",
                policy_decision.reason,
                identity=identity,
                intent=intent,
                trace=trace,
            )

        risk_decision = self.risk.assess(intent.domain, intent.action, intent.passive)
        trace.extend(risk_decision.trace)
        if role_definition and risk_decision.requires_confirmation(RiskLevel(role_definition.risk_ceiling)):
            return self._require_confirmation(identity, intent, policy_decision, risk_decision, trace)

        if policy_decision.decision == "REQUIRE_CONFIRMATION" or domain_decision.requires_confirmation:
            return self._require_confirmation(identity, intent, policy_decision, risk_decision, trace)

        plan = self._plan(intent, identity.role, trace)
        if plan.requires_confirmation:
            return self._require_confirmation(identity, intent, policy_decision, risk_decision, trace)

        # Execute the plan tasks
        execution_result = self.executor.execute_plan(plan)
        trace.extend(execution_result.trace)
        
        # Store execution results in working memory for model context
        self.working_memory.set("execution_result", execution_result)

        worker_model = self._route_model()
        if worker_model is None:
            trace.append("model:unavailable")
            return self._veto(
                "MODEL_UNAVAILABLE",
                "No worker model available",
                identity=identity,
                intent=intent,
                trace=trace,
            )
        trace.append("model:offline")

        response = self._generate_response(worker_model, user_input, identity, intent, plan, execution_result)
        trace.append("response:generated")

        self._update_memory(identity, intent, response, plan, execution_result)
        trace.append("memory:updated")

        decision = OrchestratorDecision(
            decision="ALLOW",
            identity=identity,
            intent=intent,
            risk_level=risk_decision.level.value,
            response=response,
            decision_trace=tuple(trace),
            execution_result=execution_result,
        )
        self._log_decision(decision, veto_reason=None)
        return decision

    # ------------------------------------------------------------------
    def _evaluate_domain(self, intent: Intent, role: str) -> DomainDecision:
        if not self.domain_enforcer:
            return DomainDecision("ALLOW", "domain:disabled", ("domain_enforcer:disabled",))
        return self.domain_enforcer.evaluate_action(intent.domain, role, intent.action)

    def _plan(self, intent: Intent, role: str, trace: list[str]) -> ExecutionPlan:
        plan = self.planner.create_plan(
            intent_action=intent.action,
            intent_domain=intent.domain,
            intent_passive=intent.passive,
            role=role,
        )
        trace.extend(plan.trace)
        return plan

    def _route_model(self) -> Optional[BaseModel]:
        worker = self.model_router.select_worker()
        if worker and worker.health_check():
            return worker
        return None

    def _generate_response(
        self,
        worker_model: BaseModel,
        prompt: str,
        identity: Identity,
        intent: Intent,
        plan: ExecutionPlan,
        execution_result: ExecutionResult,
    ) -> str:
        context = {
            "identity_source": identity.source,
            "identity_role": identity.role,
            "intent_domain": intent.domain,
            "intent_action": intent.action,
            "plan_id": plan.plan_id,
            "plan_trace": plan.trace,
            "execution_success": execution_result.success,
            "execution_results": execution_result.results,
            "memory_context": self.short_term_memory.items(),
        }
        return worker_model.generate(prompt, context)

    def _update_memory(
        self,
        identity: Identity,
        intent: Intent,
        response: str,
        plan: ExecutionPlan,
        execution_result: ExecutionResult,
    ) -> None:
        entry = f"{identity.role}:{intent.action}:{plan.plan_id}"
        self.short_term_memory.add(entry)
        self.working_memory.set("last_response", response)
        self.working_memory.set("last_execution", execution_result)
        if plan.tasks:
            self.task_memory.record(
                TaskMemoryEntry(task_id=plan.plan_id, summary=f"tasks={len(plan.tasks)},success={execution_result.success}")
            )

    # ------------------------------------------------------------------
    def _require_confirmation(
        self,
        identity: Identity,
        intent: Intent,
        policy_decision: PolicyDecision,
        risk_decision: RiskDecision,
        trace: list[str],
    ) -> OrchestratorDecision:
        trace.append("confirmation:required")
        decision = OrchestratorDecision(
            decision="REQUIRE_CONFIRMATION",
            identity=identity,
            intent=intent,
            risk_level=risk_decision.level.value,
            veto_reason=policy_decision.reason,
            decision_trace=tuple(trace),
        )
        self._log_decision(decision, veto_reason=policy_decision.reason)
        return decision

    def _veto(
        self,
        reason: str,
        details: str,
        *,
        identity: Optional[Identity] = None,
        intent: Optional[Intent] = None,
        risk_level: str = "UNKNOWN",
        trace: Optional[list[str]] = None,
    ) -> OrchestratorDecision:
        identity = identity or Identity("unknown", "unknown", None)
        intent = intent or Intent("unknown", "unknown", True)
        trace = trace or []
        trace.append(f"veto:{reason}")
        decision = OrchestratorDecision(
            decision="REFUSE",
            identity=identity,
            intent=intent,
            risk_level=risk_level,
            veto_reason=details,
            decision_trace=tuple(trace),
        )
        self._log_decision(decision, veto_reason=details)
        return decision

    def _log_decision(self, decision: OrchestratorDecision, veto_reason: Optional[str]) -> None:
        response_preview = None
        if decision.response:
            response_preview = decision.response.strip()[0:160]
        self.audit.log(
            {
                "event": "DECISION",
                "source": decision.identity.source,
                "role": decision.identity.role,
                "subject_id": decision.identity.subject_id,
                "action": decision.intent.action,
                "domain": decision.intent.domain,
                "passive": decision.intent.passive,
                "risk_level": decision.risk_level,
                "decision": decision.decision,
                "veto_reason": veto_reason,
                "response_preview": response_preview,
                "trace": decision.decision_trace,
            }
        )

    @staticmethod
    def _validate_input(raw_input: str) -> None:
        if not raw_input:
            raise ValueError("Empty input")
        if len(raw_input) > 2000:
            raise ValueError("Input too long for Phase 1 limits")
