"""API Key Management System for Anox Workspace.

Provides functionality to add, edit, delete, and auto-detect AI provider API keys.
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict


@dataclass
class APIKeyConfig:
    """Configuration for an API key."""
    provider: str  # anthropic, openai, google, etc.
    api_key: str
    name: str  # User-friendly name
    model: str = "auto"  # Default model to use
    enabled: bool = True
    created_at: Optional[str] = None
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return asdict(self)


class APIKeyManager:
    """Manages API keys for multiple AI providers."""
    
    # Provider detection patterns
    PROVIDER_PATTERNS = {
        'anthropic': ['sk-ant-'],
        'openai': ['sk-', 'sk-proj-'],
        'google': ['AIza'],
        'cohere': ['co-'],
        'huggingface': ['hf_'],
    }
    
    # Default models for each provider (using latest stable versions)
    DEFAULT_MODELS = {
        'anthropic': 'claude-3-5-sonnet-20241022',  # Primary model
        'openai': 'gpt-4-turbo-preview',
        'google': 'gemini-pro',
        'cohere': 'command',
        'huggingface': 'auto',
    }
    
    def __init__(self, config_file: Optional[Path] = None):
        """Initialize API key manager.
        
        Args:
            config_file: Path to config file. Defaults to ~/.anox/api_keys.json
        """
        if config_file is None:
            config_dir = Path.home() / '.anox'
            config_dir.mkdir(parents=True, exist_ok=True)
            config_file = config_dir / 'api_keys.json'
        
        self.config_file = config_file
        self._keys: Dict[str, APIKeyConfig] = {}
        self._load()
    
    def _load(self) -> None:
        """Load API keys from config file."""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    data = json.load(f)
                    for key_id, key_data in data.items():
                        self._keys[key_id] = APIKeyConfig(**key_data)
            except (json.JSONDecodeError, Exception) as e:
                print(f"⚠️  Failed to load API keys: {e}")
    
    def _save(self) -> None:
        """Save API keys to config file."""
        data = {key_id: key.to_dict() for key_id, key in self._keys.items()}
        with open(self.config_file, 'w') as f:
            json.dump(data, f, indent=2)
        
        # Set restrictive permissions
        os.chmod(self.config_file, 0o600)
    
    def detect_provider(self, api_key: str) -> str:
        """Auto-detect provider from API key format.
        
        Args:
            api_key: The API key to analyze.
            
        Returns:
            Provider name or 'unknown' if not detected.
        """
        for provider, patterns in self.PROVIDER_PATTERNS.items():
            for pattern in patterns:
                if api_key.startswith(pattern):
                    return provider
        return 'unknown'
    
    def add(self, api_key: str, name: Optional[str] = None, 
            provider: Optional[str] = None, model: Optional[str] = None) -> str:
        """Add a new API key.
        
        Args:
            api_key: The API key to add.
            name: User-friendly name. Auto-generated if None.
            provider: Provider name. Auto-detected if None.
            model: Model to use. Uses default if None.
            
        Returns:
            ID of the added key.
        """
        # Auto-detect provider if not specified
        if provider is None:
            provider = self.detect_provider(api_key)
            if provider == 'unknown':
                raise ValueError("Could not detect provider. Please specify manually.")
        
        # Generate name if not provided
        if name is None:
            name = f"{provider.capitalize()} API Key"
        
        # Use default model if not specified
        if model is None:
            model = self.DEFAULT_MODELS.get(provider, 'auto')
        
        # Generate unique ID
        key_id = f"{provider}_{len([k for k in self._keys.values() if k.provider == provider]) + 1}"
        
        # Create config
        from datetime import datetime
        config = APIKeyConfig(
            provider=provider,
            api_key=api_key,
            name=name,
            model=model,
            created_at=datetime.utcnow().isoformat()
        )
        
        self._keys[key_id] = config
        self._save()
        
        return key_id
    
    def edit(self, key_id: str, api_key: Optional[str] = None,
             name: Optional[str] = None, model: Optional[str] = None,
             enabled: Optional[bool] = None) -> bool:
        """Edit an existing API key.
        
        Args:
            key_id: ID of the key to edit.
            api_key: New API key value.
            name: New name.
            model: New model.
            enabled: New enabled status.
            
        Returns:
            True if successful, False if key not found.
        """
        if key_id not in self._keys:
            return False
        
        config = self._keys[key_id]
        
        if api_key is not None:
            # Verify provider matches
            detected_provider = self.detect_provider(api_key)
            if detected_provider != 'unknown' and detected_provider != config.provider:
                raise ValueError(f"New API key is for {detected_provider}, but existing key is for {config.provider}")
            config.api_key = api_key
        
        if name is not None:
            config.name = name
        
        if model is not None:
            config.model = model
        
        if enabled is not None:
            config.enabled = enabled
        
        self._save()
        return True
    
    def delete(self, key_id: str) -> bool:
        """Delete an API key.
        
        Args:
            key_id: ID of the key to delete.
            
        Returns:
            True if successful, False if key not found.
        """
        if key_id not in self._keys:
            return False
        
        del self._keys[key_id]
        self._save()
        return True
    
    def list(self, provider: Optional[str] = None, enabled_only: bool = False) -> List[Dict]:
        """List all API keys.
        
        Args:
            provider: Filter by provider. Returns all if None.
            enabled_only: Only return enabled keys.
            
        Returns:
            List of API key info (without exposing full keys).
        """
        results = []
        
        for key_id, config in self._keys.items():
            if provider and config.provider != provider:
                continue
            
            if enabled_only and not config.enabled:
                continue
            
            # Mask the API key
            masked_key = self._mask_key(config.api_key)
            
            results.append({
                'id': key_id,
                'provider': config.provider,
                'name': config.name,
                'model': config.model,
                'enabled': config.enabled,
                'api_key_masked': masked_key,
                'created_at': config.created_at
            })
        
        return results
    
    def get(self, key_id: str) -> Optional[APIKeyConfig]:
        """Get an API key configuration.
        
        Args:
            key_id: ID of the key to get.
            
        Returns:
            APIKeyConfig or None if not found.
        """
        return self._keys.get(key_id)
    
    def get_active_key(self, provider: Optional[str] = None) -> Optional[Tuple[str, APIKeyConfig]]:
        """Get the first active API key for a provider.
        
        Args:
            provider: Provider to get key for. Returns any if None.
            
        Returns:
            Tuple of (key_id, config) or None if not found.
        """
        for key_id, config in self._keys.items():
            if not config.enabled:
                continue
            
            if provider is None or config.provider == provider:
                return (key_id, config)
        
        return None
    
    def _mask_key(self, api_key: str) -> str:
        """Mask an API key for display.
        
        Args:
            api_key: The key to mask.
            
        Returns:
            Masked key showing only first 8 and last 4 characters.
        """
        if len(api_key) <= 12:
            return api_key[:4] + '...' + api_key[-2:]
        return api_key[:8] + '...' + api_key[-4:]
    
    def import_from_env(self) -> Dict[str, str]:
        """Import API keys from environment variables.
        
        Returns:
            Dictionary mapping provider to key_id for imported keys.
        """
        imported = {}
        
        env_vars = {
            'ANTHROPIC_API_KEY': 'anthropic',
            'OPENAI_API_KEY': 'openai',
            'GOOGLE_API_KEY': 'google',
            'COHERE_API_KEY': 'cohere',
            'HUGGINGFACE_API_KEY': 'huggingface',
        }
        
        for env_var, provider in env_vars.items():
            api_key = os.getenv(env_var)
            if api_key:
                # Check if already exists
                existing = self.get_active_key(provider)
                if not existing:
                    key_id = self.add(
                        api_key=api_key,
                        name=f"{provider.capitalize()} (from env)",
                        provider=provider
                    )
                    imported[provider] = key_id
        
        return imported


# Global instance
_manager_instance: Optional[APIKeyManager] = None


def get_api_key_manager() -> APIKeyManager:
    """Get the global API key manager instance."""
    global _manager_instance
    if _manager_instance is None:
        _manager_instance = APIKeyManager()
    return _manager_instance
