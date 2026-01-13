"""Task executor for running planned tasks through tools."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional, Any

from core.planner import ExecutionPlan, Task
from tools.base_tool import Tool


@dataclass
class ExecutionResult:
    """Result of executing a plan."""
    
    plan_id: str
    success: bool
    results: Dict[str, Any]  # task_id -> result
    errors: Dict[str, str]   # task_id -> error message
    trace: List[str]


class TaskExecutor:
    """
    Executes tasks from an ExecutionPlan.
    
    Phase 1: Simple sequential execution.
    Does NOT add new capabilities, just connects existing planner to tools.
    """
    
    def __init__(self, tools: Optional[Dict[str, Tool]] = None):
        """
        Initialize executor with available tools.
        
        Args:
            tools: Dictionary of tool_id -> Tool instances
        """
        self.tools = tools or {}
    
    def execute_plan(self, plan: ExecutionPlan) -> ExecutionResult:
        """
        Execute all tasks in the plan sequentially.
        
        Args:
            plan: ExecutionPlan from planner
            
        Returns:
            ExecutionResult with outcomes for each task
        """
        trace = [
            f"executor:start:{plan.plan_id}",
            f"tasks_count:{len(plan.tasks)}",
        ]
        
        results: Dict[str, Any] = {}
        errors: Dict[str, str] = {}
        
        # Execute tasks in order (respecting dependencies)
        for task in plan.tasks:
            trace.append(f"task:executing:{task.task_id}")
            
            # Check dependencies completed successfully
            if task.dependencies:
                missing_deps = [dep for dep in task.dependencies if dep not in results]
                if missing_deps:
                    error_msg = f"Missing dependencies: {missing_deps}"
                    errors[task.task_id] = error_msg
                    trace.append(f"task:error:{task.task_id}:deps_missing")
                    continue
            
            # Execute task
            try:
                result = self._execute_task(task)
                results[task.task_id] = result
                trace.append(f"task:success:{task.task_id}")
            except Exception as e:
                error_msg = str(e)
                errors[task.task_id] = error_msg
                trace.append(f"task:error:{task.task_id}:{type(e).__name__}")
        
        success = len(errors) == 0
        trace.append(f"executor:complete:success={success}")
        
        return ExecutionResult(
            plan_id=plan.plan_id,
            success=success,
            results=results,
            errors=errors,
            trace=trace,
        )
    
    def _execute_task(self, task: Task) -> Any:
        """
        Execute a single task.
        
        Now with concrete tool execution! Dispatches to appropriate tool
        based on task type and description.
        
        Args:
            task: Task to execute
            
        Returns:
            Task execution result from tool or metadata if no tool available
        """
        # Try to dispatch to appropriate tool
        task_type = task.task_type.value
        
        # Map task types to tools
        if task_type in ["read_file", "write_file", "list_files", "search_files"] and "file_tools" in self.tools:
            return self._dispatch_to_file_tool(task)
        elif task_type in ["git_status", "git_diff", "git_add", "git_commit"] and "git_tools" in self.tools:
            return self._dispatch_to_git_tool(task)
        elif task_type in ["analyze_code", "lint_code", "check_syntax"] and "analysis_tools" in self.tools:
            return self._dispatch_to_analysis_tool(task)
        else:
            # Fallback: Return metadata if no tool available
            return {
                "task_type": task_type,
                "description": task.description,
                "status": "completed",
                "note": f"No tool registered for task type: {task_type}",
            }
    
    def _dispatch_to_file_tool(self, task: Task) -> Any:
        """Dispatch task to FileTools."""
        tool = self.tools["file_tools"]
        task_type = task.task_type.value
        
        # Extract parameters from task description
        # Simple parsing for now - can be enhanced later
        payload = {
            "operation": task_type.replace("_files", "").replace("_file", ""),
        }
        
        # Add any parameters from task metadata
        if hasattr(task, "parameters") and task.parameters:
            payload.update(task.parameters)
        
        return tool.run(payload)
    
    def _dispatch_to_git_tool(self, task: Task) -> Any:
        """Dispatch task to GitTools."""
        tool = self.tools["git_tools"]
        task_type = task.task_type.value
        
        payload = {
            "operation": task_type.replace("git_", ""),
        }
        
        # Add any parameters from task metadata
        if hasattr(task, "parameters") and task.parameters:
            payload.update(task.parameters)
        
        return tool.run(payload)
    
    def _dispatch_to_analysis_tool(self, task: Task) -> Any:
        """Dispatch task to AnalysisTools."""
        tool = self.tools["analysis_tools"]
        task_type = task.task_type.value
        
        payload = {
            "operation": task_type.replace("_code", "").replace("analyze", "lint"),
        }
        
        # Add any parameters from task metadata
        if hasattr(task, "parameters") and task.parameters:
            payload.update(task.parameters)
        
        return tool.run(payload)
    
    def register_tool(self, tool_id: str, tool: Tool) -> None:
        """
        Register a tool for use by the executor.
        
        Args:
            tool_id: Unique identifier for the tool
            tool: Tool instance
        """
        self.tools[tool_id] = tool
    
    def get_available_tools(self) -> List[str]:
        """
        Get list of registered tool IDs.
        
        Returns:
            List of tool IDs
        """
        return list(self.tools.keys())
