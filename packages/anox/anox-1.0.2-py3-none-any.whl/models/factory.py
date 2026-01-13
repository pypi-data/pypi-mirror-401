"""Model Factory - Create and configure AI models with proper error handling."""

from __future__ import annotations

from typing import Optional, Dict, Any
from pathlib import Path

from models.base import BaseModel
from models.config import ModelConfigManager
from models.online_api import OnlineAPIAdapter
from models.offline_adapter import OfflineModelAdapter
from models.router import ModelRouter


class ModelFactory:
    """Factory for creating AI models with proper configuration and error handling."""
    
    def __init__(self, config_path: Optional[Path] = None):
        """Initialize model factory.
        
        Args:
            config_path: Path to config file. Defaults to config/models.yaml
        """
        self.config_manager = ModelConfigManager(config_path)
    
    def create_primary_model(self) -> BaseModel:
        """Create the primary model based on configuration.
        
        Returns:
            Configured model instance.
            
        Raises:
            RuntimeError: If primary model cannot be created.
        """
        # Try to get the configured online model (Anthropic Claude by default)
        online_config = self.config_manager.get_default_online_model()
        
        if online_config and online_config.enabled:
            try:
                return self._create_online_model(online_config)
            except Exception as e:
                print(f"⚠️  Failed to create primary online model: {e}")
                print("   Falling back to offline model")
        
        # Fallback to offline model
        offline_config = self.config_manager.get_default_offline_model()
        return self._create_offline_model(offline_config)
    
    def create_model_router(self) -> ModelRouter:
        """Create a model router with online and offline models.
        
        Returns:
            Configured ModelRouter instance.
        """
        router_config = self.config_manager.get_router_config()
        
        # Create offline model (always available)
        offline_config = self.config_manager.get_default_offline_model()
        offline_model = self._create_offline_model(offline_config)
        
        # Try to create online model
        online_model = None
        online_config = self.config_manager.get_default_online_model()
        
        if online_config and online_config.enabled:
            try:
                online_model = self._create_online_model(online_config)
                print(f"✓ Online model ({online_config.provider}) configured successfully")
            except Exception as e:
                print(f"⚠️  Could not configure online model: {e}")
                print("   System will use offline model only")
        
        return ModelRouter(
            offline_model=offline_model,
            online_model=online_model,
            prefer_online=router_config.prefer_online,
            auto_fallback=router_config.auto_fallback,
        )
    
    def create_anthropic_model(
        self,
        api_key: Optional[str] = None,
        model_name: str = "claude-3-5-sonnet-20241022"
    ) -> OnlineAPIAdapter:
        """Create an Anthropic Claude model.
        
        Args:
            api_key: API key. Uses environment variable if None.
            model_name: Model name. Defaults to Claude 3.5 Sonnet.
            
        Returns:
            Configured Anthropic model.
            
        Raises:
            ValueError: If API key is not provided and not in environment.
            ImportError: If anthropic package is not installed.
        """
        return OnlineAPIAdapter(
            provider="anthropic",
            model_name=model_name,
            api_key=api_key,
            name=f"anthropic-{model_name}",
        )
    
    def create_openai_model(
        self,
        api_key: Optional[str] = None,
        model_name: str = "gpt-4-turbo-preview"
    ) -> OnlineAPIAdapter:
        """Create an OpenAI model.
        
        Args:
            api_key: API key. Uses environment variable if None.
            model_name: Model name. Defaults to GPT-4 Turbo.
            
        Returns:
            Configured OpenAI model.
            
        Raises:
            ValueError: If API key is not provided and not in environment.
            ImportError: If openai package is not installed.
        """
        return OnlineAPIAdapter(
            provider="openai",
            model_name=model_name,
            api_key=api_key,
            name=f"openai-{model_name}",
        )
    
    def _create_online_model(self, config) -> OnlineAPIAdapter:
        """Create an online model from configuration.
        
        Args:
            config: Model configuration.
            
        Returns:
            Configured online model.
            
        Raises:
            ValueError: If configuration is invalid.
            ImportError: If required package is not installed.
        """
        return OnlineAPIAdapter(
            provider=config.provider,
            model_name=config.model_name or "auto",
            api_key=config.api_key,
            base_url=config.base_url,
            name=config.name,
        )
    
    def _create_offline_model(self, config) -> OfflineModelAdapter:
        """Create an offline model from configuration.
        
        Args:
            config: Model configuration.
            
        Returns:
            Configured offline model.
        """
        return OfflineModelAdapter(name=config.name)


# Global factory instance
_factory_instance: Optional[ModelFactory] = None


def get_model_factory() -> ModelFactory:
    """Get the global model factory instance."""
    global _factory_instance
    if _factory_instance is None:
        _factory_instance = ModelFactory()
    return _factory_instance


def create_default_router() -> ModelRouter:
    """Create a model router with default configuration.
    
    This is the main entry point for getting a configured AI model.
    
    Returns:
        Configured ModelRouter with online and offline models.
    """
    factory = get_model_factory()
    return factory.create_model_router()
