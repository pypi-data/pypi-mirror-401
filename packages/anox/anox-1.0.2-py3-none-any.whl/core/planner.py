# core/planner.py
"""Rule-based planner for AXON Phase 1 (no execution)."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Dict, Iterable, List, Tuple


class TaskType(str, Enum):
    ANALYSIS = "analysis"
    DESIGN = "design"
    GENERATION = "generation"
    VALIDATION = "validation"


@dataclass(frozen=True)
class Task:
    task_id: str
    task_type: TaskType
    description: str
    dependencies: Tuple[str, ...]


@dataclass(frozen=True)
class ExecutionPlan:
    plan_id: str
    tasks: Tuple[Task, ...]
    required_tools: Tuple[str, ...]
    estimated_risk: str
    requires_confirmation: bool
    trace: Tuple[str, ...]


class Planner:
    """Deterministic planner that emits audit-friendly plans."""

    ACTION_TEMPLATES: Dict[str, List[Tuple[TaskType, str]]] = {
        "code_generation": [
            (TaskType.ANALYSIS, "understand_requirements"),
            (TaskType.DESIGN, "outline_solution"),
            (TaskType.GENERATION, "produce_code"),
            (TaskType.VALIDATION, "self_review"),
        ],
        "code_refactoring": [
            (TaskType.ANALYSIS, "analyze_existing_code"),
            (TaskType.DESIGN, "plan_refactors"),
            (TaskType.GENERATION, "apply_refactor"),
            (TaskType.VALIDATION, "verify_changes"),
        ],
        "architecture_design": [
            (TaskType.ANALYSIS, "collect_constraints"),
            (TaskType.DESIGN, "model_architecture"),
            (TaskType.VALIDATION, "review_architecture"),
        ],
        "documentation": [
            (TaskType.ANALYSIS, "gather_context"),
            (TaskType.GENERATION, "draft_docs"),
            (TaskType.VALIDATION, "review_docs"),
        ],
        "defensive_security_analysis": [
            (TaskType.ANALYSIS, "collect_indicators"),
            (TaskType.DESIGN, "map_defenses"),
            (TaskType.VALIDATION, "document_findings"),
        ],
        "detection_and_monitoring_design": [
            (TaskType.ANALYSIS, "assess_threats"),
            (TaskType.DESIGN, "design_detections"),
            (TaskType.VALIDATION, "review_monitoring"),
        ],
        "red_team_vulnerability_analysis": [
            (TaskType.ANALYSIS, "identify_targets"),
            (TaskType.DESIGN, "plan_assessment"),
            (TaskType.VALIDATION, "document_risks"),
        ],
        "malware_structure_analysis_static": [
            (TaskType.ANALYSIS, "parse_binary"),
            (TaskType.DESIGN, "map_components"),
            (TaskType.VALIDATION, "report_observations"),
        ],
    }

    def __init__(self) -> None:
        self._counter = 0

    def create_plan(
        self,
        *,
        intent_action: str,
        intent_domain: str,
        intent_passive: bool,
        role: str,
    ) -> ExecutionPlan:
        self._counter += 1
        plan_id = f"plan-{self._counter}"

        template = self.ACTION_TEMPLATES.get(intent_action)
        trace = [
            f"plan:{plan_id}",
            f"action:{intent_action}",
            f"domain:{intent_domain}",
            f"role:{role}",
        ]

        if not template:
            trace.append("template:default_single_task")
            task = Task(
                task_id=f"{plan_id}-task-1",
                task_type=TaskType.ANALYSIS,
                description=f"analyze_{intent_action}",
                dependencies=(),
            )
            tasks = (task,)
        else:
            trace.append("template:multi_step")
            tasks = self._build_tasks(plan_id, template)

        requires_confirmation = intent_domain in {"red", "malware"}
        if requires_confirmation:
            trace.append("confirmation:domain_requires")

        estimated_risk = "LOW" if intent_passive else "MEDIUM"
        trace.append(f"risk:{estimated_risk}")

        return ExecutionPlan(
            plan_id=plan_id,
            tasks=tasks,
            required_tools=tuple(),
            estimated_risk=estimated_risk,
            requires_confirmation=requires_confirmation,
            trace=tuple(trace),
        )

    def validate_plan(self, plan: ExecutionPlan, domain: str, role: str) -> bool:
        return bool(plan.tasks)

    def _build_tasks(
        self,
        plan_id: str,
        template: List[Tuple[TaskType, str]],
    ) -> Tuple[Task, ...]:
        tasks: List[Task] = []
        dependency: Tuple[str, ...] = ()
        for index, (task_type, description) in enumerate(template, start=1):
            task_id = f"{plan_id}-task-{index}"
            task = Task(
                task_id=task_id,
                task_type=task_type,
                description=description,
                dependencies=dependency,
            )
            tasks.append(task)
            dependency = (task_id,)
        return tuple(tasks)
