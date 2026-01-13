"""Model configuration management."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Optional

try:
    import yaml
except ImportError:
    yaml = None


@dataclass
class ModelConfig:
    """Configuration for a model."""
    name: str
    type: str  # "offline" or "online"
    provider: Optional[str] = None  # For online models
    model_name: Optional[str] = None
    model_path: Optional[str] = None  # For offline models
    api_key: Optional[str] = None
    base_url: Optional[str] = None
    enabled: bool = True
    options: Dict[str, Any] = None

    def __post_init__(self):
        if self.options is None:
            self.options = {}


@dataclass
class RouterConfig:
    """Configuration for model router."""
    prefer_online: bool = False
    auto_fallback: bool = True
    offline_model: str = "default_offline"
    online_model: Optional[str] = None


class ModelConfigManager:
    """
    Manages model configurations.
    
    Loads from:
    1. config/models.yaml (if exists)
    2. Environment variables
    3. Default values
    """

    def __init__(self, config_path: Optional[Path] = None) -> None:
        self.config_path = config_path or Path("config/models.yaml")
        self._models: Dict[str, ModelConfig] = {}
        self._router_config: RouterConfig = RouterConfig()
        self._load_config()

    def _load_config(self) -> None:
        """Load configuration from file and environment."""
        # Try to load from YAML
        if self.config_path.exists() and yaml:
            try:
                with open(self.config_path, "r") as f:
                    config_data = yaml.safe_load(f)
                    self._parse_config(config_data or {})
            except Exception as e:
                print(f"⚠️  Failed to load config from {self.config_path}: {e}")
        
        # Load from environment variables
        self._load_from_env()
        
        # Ensure at least default models exist
        self._ensure_defaults()

    def _parse_config(self, config_data: Dict[str, Any]) -> None:
        """Parse configuration data."""
        # Parse models
        models_data = config_data.get("models", {})
        for model_id, model_info in models_data.items():
            self._models[model_id] = ModelConfig(
                name=model_info.get("name", model_id),
                type=model_info.get("type", "offline"),
                provider=model_info.get("provider"),
                model_name=model_info.get("model_name"),
                model_path=model_info.get("model_path"),
                api_key=model_info.get("api_key"),
                base_url=model_info.get("base_url"),
                enabled=model_info.get("enabled", True),
                options=model_info.get("options", {}),
            )
        
        # Parse router config
        router_data = config_data.get("router", {})
        self._router_config = RouterConfig(
            prefer_online=router_data.get("prefer_online", False),
            auto_fallback=router_data.get("auto_fallback", True),
            offline_model=router_data.get("offline_model", "default_offline"),
            online_model=router_data.get("online_model"),
        )

    def _load_from_env(self) -> None:
        """Load configuration from environment variables."""
        # Anthropic (Priority 1 - Primary Model)
        if os.environ.get("ANTHROPIC_API_KEY"):
            model_id = "anthropic_claude"
            if model_id not in self._models:
                self._models[model_id] = ModelConfig(
                    name="Anthropic Claude 3.5 Sonnet",
                    type="online",
                    provider="anthropic",
                    model_name="claude-3-5-sonnet-20241022",
                    api_key=os.environ.get("ANTHROPIC_API_KEY"),
                    enabled=True,
                )
        
        # OpenAI (Priority 2 - Fallback)
        if os.environ.get("OPENAI_API_KEY"):
            model_id = "openai_gpt35"
            if model_id not in self._models:
                self._models[model_id] = ModelConfig(
                    name="OpenAI GPT-3.5",
                    type="online",
                    provider="openai",
                    model_name="gpt-3.5-turbo",
                    api_key=os.environ.get("OPENAI_API_KEY"),
                )
        
        # Google
        if os.environ.get("GOOGLE_API_KEY"):
            model_id = "google_gemini"
            if model_id not in self._models:
                self._models[model_id] = ModelConfig(
                    name="Google Gemini",
                    type="online",
                    provider="google",
                    model_name="gemini-pro",
                    api_key=os.environ.get("GOOGLE_API_KEY"),
                )
        
        # Cohere
        if os.environ.get("COHERE_API_KEY"):
            model_id = "cohere_command"
            if model_id not in self._models:
                self._models[model_id] = ModelConfig(
                    name="Cohere Command",
                    type="online",
                    provider="cohere",
                    model_name="command",
                    api_key=os.environ.get("COHERE_API_KEY"),
                )
        
        # HuggingFace
        if os.environ.get("HUGGINGFACE_API_KEY"):
            model_id = "huggingface_inference"
            if model_id not in self._models:
                # Use environment variable for model name, fallback to popular default
                default_model = os.environ.get(
                    "HUGGINGFACE_MODEL", 
                    "mistralai/Mistral-7B-Instruct-v0.2"
                )
                self._models[model_id] = ModelConfig(
                    name="HuggingFace Inference",
                    type="online",
                    provider="huggingface",
                    model_name=default_model,
                    api_key=os.environ.get("HUGGINGFACE_API_KEY"),
                )
        
        # Local model path
        if os.environ.get("AXON_LOCAL_MODEL_PATH"):
            model_id = "local_llama"
            if model_id not in self._models:
                self._models[model_id] = ModelConfig(
                    name="Local LLaMA",
                    type="offline",
                    model_path=os.environ.get("AXON_LOCAL_MODEL_PATH"),
                )

    def _ensure_defaults(self) -> None:
        """Ensure default models exist."""
        if "default_offline" not in self._models:
            self._models["default_offline"] = ModelConfig(
                name="Default Offline Mock",
                type="offline",
                enabled=True,
            )

    def get_model_config(self, model_id: str) -> Optional[ModelConfig]:
        """Get configuration for a specific model."""
        return self._models.get(model_id)

    def get_router_config(self) -> RouterConfig:
        """Get router configuration."""
        return self._router_config

    def list_models(self) -> Dict[str, ModelConfig]:
        """List all configured models."""
        return self._models.copy()

    def list_enabled_models(self) -> Dict[str, ModelConfig]:
        """List all enabled models."""
        return {k: v for k, v in self._models.items() if v.enabled}

    def get_default_offline_model(self) -> ModelConfig:
        """Get the default offline model configuration."""
        model_id = self._router_config.offline_model
        return self._models.get(model_id, self._models["default_offline"])

    def get_default_online_model(self) -> Optional[ModelConfig]:
        """Get the default online model configuration."""
        if not self._router_config.online_model:
            # Find first enabled online model
            for model_id, config in self._models.items():
                if config.type == "online" and config.enabled:
                    return config
            return None
        
        return self._models.get(self._router_config.online_model)

    def save_config(self) -> None:
        """Save current configuration to file."""
        if not yaml:
            print("⚠️  PyYAML not installed. Cannot save config.")
            return
        
        config_data = {
            "models": {},
            "router": {
                "prefer_online": self._router_config.prefer_online,
                "auto_fallback": self._router_config.auto_fallback,
                "offline_model": self._router_config.offline_model,
                "online_model": self._router_config.online_model,
            },
        }
        
        for model_id, config in self._models.items():
            config_data["models"][model_id] = {
                "name": config.name,
                "type": config.type,
                "provider": config.provider,
                "model_name": config.model_name,
                "model_path": config.model_path,
                "base_url": config.base_url,
                "enabled": config.enabled,
                "options": config.options,
            }
            # Don't save API keys to file
        
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.config_path, "w") as f:
            yaml.dump(config_data, f, default_flow_style=False)
        
        print(f"✓ Configuration saved to {self.config_path}")
