"""Factory for creating DecisionOrchestrator instances with all dependencies."""

from __future__ import annotations

from pathlib import Path

from audit.log import AuditLogger
from core.identity import IdentityResolver
from core.intent import IntentClassifier
from core.orchestrator import DecisionOrchestrator
from core.planner import Planner
from core.policy import PolicyEngine
from core.risk import RiskAssessor
from core.executor import TaskExecutor
from guardrails.kill_switch import KillSwitch
from guardrails.roles_registry import RoleRegistry
from memory.short_term import ShortTermMemory
from memory.task_memory import TaskMemory
from memory.working_memory import WorkingMemory
from models.router import ModelRouter
from tools.file_tools import FileTools
from tools.git_tools import GitTools
from tools.analysis_tools import AnalysisTools


def create_orchestrator(
    model_router: ModelRouter,
    log_file: str = "logs/brain.log",
    policy_file: str = "guardrails/policy.yaml",
    roles_file: str = "guardrails/roles.yaml",
    domains_path: str = "domains",
    workspace_root: str = ".",
) -> DecisionOrchestrator:
    """
    Create a fully initialized DecisionOrchestrator instance.

    This factory function centralizes the creation of all orchestrator dependencies,
    eliminating code duplication across CLI, API, and other entry points.

    Args:
        model_router: Configured ModelRouter instance
        log_file: Path to audit log file (default: "logs/brain.log")
        policy_file: Path to policy YAML file (default: "guardrails/policy.yaml")
        roles_file: Path to roles YAML file (default: "guardrails/roles.yaml")
        domains_path: Path to domains directory (default: "domains")
        workspace_root: Root directory for file operations (default: ".")

    Returns:
        Fully initialized DecisionOrchestrator instance

    Example:
        >>> from models.router import ModelRouter
        >>> from models.offline_adapter import OfflineModelAdapter
        >>>
        >>> offline_model = OfflineModelAdapter()
        >>> router = ModelRouter(offline_model=offline_model)
        >>> orchestrator = create_orchestrator(router)
    """
    # Ensure logs directory exists
    Path("logs").mkdir(parents=True, exist_ok=True)

    # Initialize all components
    audit_logger = AuditLogger(Path(log_file))
    policy_engine = PolicyEngine(Path(policy_file))
    risk_assessor = RiskAssessor()
    planner = Planner()
    
    # Initialize tools with actual implementations
    tools = {
        "file_tools": FileTools(workspace_root=workspace_root),
        "git_tools": GitTools(workspace_root=workspace_root),
        "analysis_tools": AnalysisTools(workspace_root=workspace_root),
    }
    
    # Create task executor with real tools
    task_executor = TaskExecutor(tools=tools)
    
    identity_resolver = IdentityResolver()
    intent_classifier = IntentClassifier()
    kill_switch = KillSwitch()
    role_registry = RoleRegistry(Path(roles_file))
    short_term_memory = ShortTermMemory()
    working_memory = WorkingMemory()
    task_memory = TaskMemory()

    # Create orchestrator with all dependencies
    orchestrator = DecisionOrchestrator(
        identity_resolver=identity_resolver,
        intent_classifier=intent_classifier,
        policy_engine=policy_engine,
        risk_assessor=risk_assessor,
        planner=planner,
        task_executor=task_executor,  # Include task executor with tools
        model_router=model_router,
        short_term_memory=short_term_memory,
        working_memory=working_memory,
        task_memory=task_memory,
        audit_logger=audit_logger,
        kill_switch=kill_switch,
        role_registry=role_registry,
        domains_path=Path(domains_path),
    )

    return orchestrator


def get_kill_switch() -> KillSwitch:
    """
    Get a KillSwitch instance.

    Useful for standalone kill switch operations without full orchestrator.

    Note: This creates a new KillSwitch instance, but the state is persisted
    to disk automatically by the KillSwitch class itself. Each instance loads
    the same state from session/kill_switch.state, so state is shared across
    instances. If you need to maintain references within a single context,
    store the returned instance rather than calling this function repeatedly.

    Returns:
        KillSwitch instance with persistent state
    """
    return KillSwitch()
