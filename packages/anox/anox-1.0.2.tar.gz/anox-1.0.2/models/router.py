# models/router.py

from __future__ import annotations

from typing import Any, Dict, Optional

from models.base import BaseModel


class ModelRouter:
    """
    Enhanced model router with intelligent selection.
    
    Supports:
    - Automatic fallback from online to offline
    - Task-based model selection
    - Load balancing between models
    """

    def __init__(
        self,
        *,
        offline_model: BaseModel,
        online_model: Optional[BaseModel] = None,
        prefer_online: bool = False,
        auto_fallback: bool = True,
    ) -> None:
        self.offline = offline_model
        self.online = online_model
        self.prefer_online = prefer_online
        self.auto_fallback = auto_fallback

    def select_worker(self, context: Optional[Dict[str, Any]] = None) -> BaseModel:
        """
        Select the appropriate worker model based on context.
        
        Args:
            context: Optional context for selection (task type, complexity, etc.)
            
        Returns:
            Selected model
        """
        # If prefer online and online model is available and healthy
        if self.prefer_online and self.online and self.online.health_check():
            return self.online
        
        # Check if task requires online model
        if context:
            task_type = context.get("task_type", "")
            requires_online = context.get("requires_online", False)
            
            # Some tasks benefit from online models
            online_preferred_tasks = [
                "code_review",
                "complex_analysis",
                "test_generation",
            ]
            
            if requires_online or task_type in online_preferred_tasks:
                if self.online and self.online.health_check():
                    return self.online
                elif not self.auto_fallback:
                    raise RuntimeError("Online model required but not available")
        
        # Default to offline model
        return self.offline

    def select_teacher(self) -> Optional[BaseModel]:
        """
        Select the teacher model for validation or refinement.
        
        Returns:
            Teacher model if available, None otherwise
        """
        return self.online

    def get_model_info(self) -> Dict[str, Any]:
        """Get information about available models."""
        offline_info = self.offline.get_info() if hasattr(self.offline, "get_info") else {"name": self.offline.name}
        online_info = None
        if self.online:
            online_info = self.online.get_info() if hasattr(self.online, "get_info") else {"name": self.online.name}
        
        return {
            "offline_model": offline_info,
            "online_model": online_info,
            "prefer_online": self.prefer_online,
            "auto_fallback": self.auto_fallback,
        }
