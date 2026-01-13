# models/base.py

from abc import ABC, abstractmethod
from typing import Any, Dict


class BaseModel(ABC):
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def generate(self, prompt: str, context: Dict[str, Any]) -> str:
        pass

    @abstractmethod
    def health_check(self) -> bool:
        pass

    def _build_system_prompt(self, context: Dict[str, Any]) -> str:
        """
        Build system prompt based on context.

        This method provides a common system prompt builder for all model types,
        eliminating duplication between online and offline adapters.

        Note: This implementation standardizes the prompt format across all models.
        Previously, offline models used "System: {prompt}" prefix while online
        models did not. This version uses the online format (without "System:")
        which is more compatible with modern LLM APIs.

        Args:
            context: Context dictionary containing role, domain, and task type

        Returns:
            System prompt string
        """
        role = context.get("identity_role", "assistant")
        domain = context.get("intent_domain", "general")
        task_type = context.get("task_type", "general")

        prompts = {
            "code_analysis": (
                "You are an expert code analyzer. "
                "Analyze code for quality, bugs, security issues, and improvements. "
                "Provide specific, actionable feedback."
            ),
            "code_review": (
                "You are a thorough code reviewer. "
                "Review code critically and provide constructive feedback with examples."
            ),
            "code_completion": (
                "You are an intelligent code completion assistant. "
                "Complete code accurately, idiomatically, and following best practices."
            ),
            "test_generation": (
                "You are a test generation expert. "
                "Generate comprehensive, meaningful test cases covering edge cases."
            ),
            "explanation": (
                "You are a clear and concise technical explainer. "
                "Break down complex concepts into understandable parts."
            ),
            "refactoring": (
                "You are a code refactoring expert. "
                "Suggest improvements for code structure, readability, and maintainability."
            ),
        }

        base_prompt = "You are a helpful AI assistant specializing in software development."
        system_prompt = prompts.get(task_type, base_prompt)
        return f"{system_prompt}\nRole: {role}\nDomain: {domain}"
