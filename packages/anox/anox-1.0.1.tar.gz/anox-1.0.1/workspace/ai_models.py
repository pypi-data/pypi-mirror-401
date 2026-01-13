"""
Multi-Provider AI Model System for Anox

Supports both offline and online AI models from various providers.
Provides a unified interface for all model interactions.
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum
import json


class ModelType(Enum):
    """Types of AI models."""
    OFFLINE = "offline"
    ONLINE = "online"


class ModelProvider(Enum):
    """Supported AI model providers."""
    # Online providers
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GOOGLE = "google"
    COHERE = "cohere"
    MISTRAL = "mistral"
    
    # Offline providers
    LLAMA_CPP = "llama_cpp"
    GGUF = "gguf"
    ONNX = "onnx"
    TRANSFORMERS = "transformers"
    OLLAMA = "ollama"


@dataclass
class ModelConfig:
    """Configuration for an AI model."""
    provider: ModelProvider
    model_name: str
    model_type: ModelType
    api_key: Optional[str] = None
    base_url: Optional[str] = None
    model_path: Optional[str] = None  # For offline models
    max_tokens: int = 2048
    temperature: float = 0.7
    context_window: int = 4096
    capabilities: List[str] = None  # e.g., ['code', 'chat', 'completion']
    
    def __post_init__(self):
        if self.capabilities is None:
            self.capabilities = ['chat', 'completion']


@dataclass
class ModelResponse:
    """Response from an AI model."""
    content: str
    model: str
    provider: str
    tokens_used: int = 0
    finish_reason: str = "complete"
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


class BaseModelProvider(ABC):
    """Base class for all AI model providers."""
    
    def __init__(self, config: ModelConfig):
        self.config = config
        self.is_initialized = False
    
    @abstractmethod
    def initialize(self) -> bool:
        """Initialize the model provider."""
        pass
    
    @abstractmethod
    def generate(self, prompt: str, **kwargs) -> ModelResponse:
        """Generate response from the model."""
        pass
    
    @abstractmethod
    def chat(self, messages: List[Dict[str, str]], **kwargs) -> ModelResponse:
        """Chat with the model using message history."""
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """Check if the model is available."""
        pass
    
    def get_info(self) -> Dict[str, Any]:
        """Get information about the model."""
        return {
            'provider': self.config.provider.value,
            'model_name': self.config.model_name,
            'model_type': self.config.model_type.value,
            'capabilities': self.config.capabilities,
            'context_window': self.config.context_window,
            'is_initialized': self.is_initialized
        }


# ============================================================================
# ONLINE MODEL PROVIDERS
# ============================================================================

class OpenAIProvider(BaseModelProvider):
    """OpenAI model provider (GPT-4, GPT-3.5, etc.)."""
    
    def initialize(self) -> bool:
        """Initialize OpenAI client."""
        try:
            # Placeholder for actual OpenAI initialization
            # In production: from openai import OpenAI; self.client = OpenAI(api_key=...)
            self.is_initialized = True
            return True
        except Exception as e:
            print(f"OpenAI initialization failed: {e}")
            return False
    
    def generate(self, prompt: str, **kwargs) -> ModelResponse:
        """Generate response using OpenAI API."""
        if not self.is_initialized:
            raise RuntimeError("OpenAI provider not initialized")
        
        # Placeholder implementation
        # In production: response = self.client.completions.create(...)
        return ModelResponse(
            content=f"[OpenAI {self.config.model_name}] Response to: {prompt[:50]}...",
            model=self.config.model_name,
            provider=self.config.provider.value,
            tokens_used=100
        )
    
    def chat(self, messages: List[Dict[str, str]], **kwargs) -> ModelResponse:
        """Chat using OpenAI API."""
        if not self.is_initialized:
            raise RuntimeError("OpenAI provider not initialized")
        
        # Placeholder implementation
        # In production: response = self.client.chat.completions.create(...)
        last_message = messages[-1]['content'] if messages else ""
        return ModelResponse(
            content=f"[OpenAI {self.config.model_name}] Chat response to: {last_message[:50]}...",
            model=self.config.model_name,
            provider=self.config.provider.value,
            tokens_used=150
        )
    
    def is_available(self) -> bool:
        """Check if OpenAI API is available."""
        return self.config.api_key is not None


class AnthropicProvider(BaseModelProvider):
    """Anthropic model provider (Claude)."""
    
    def initialize(self) -> bool:
        """Initialize Anthropic client."""
        try:
            # Placeholder for actual Anthropic initialization
            # In production: from anthropic import Anthropic; self.client = Anthropic(api_key=...)
            self.is_initialized = True
            return True
        except Exception as e:
            print(f"Anthropic initialization failed: {e}")
            return False
    
    def generate(self, prompt: str, **kwargs) -> ModelResponse:
        """Generate response using Anthropic API."""
        if not self.is_initialized:
            raise RuntimeError("Anthropic provider not initialized")
        
        return ModelResponse(
            content=f"[Claude {self.config.model_name}] Response to: {prompt[:50]}...",
            model=self.config.model_name,
            provider=self.config.provider.value,
            tokens_used=100
        )
    
    def chat(self, messages: List[Dict[str, str]], **kwargs) -> ModelResponse:
        """Chat using Anthropic API."""
        if not self.is_initialized:
            raise RuntimeError("Anthropic provider not initialized")
        
        last_message = messages[-1]['content'] if messages else ""
        return ModelResponse(
            content=f"[Claude {self.config.model_name}] Chat response to: {last_message[:50]}...",
            model=self.config.model_name,
            provider=self.config.provider.value,
            tokens_used=150
        )
    
    def is_available(self) -> bool:
        """Check if Anthropic API is available."""
        return self.config.api_key is not None


class GoogleProvider(BaseModelProvider):
    """Google model provider (Gemini, PaLM)."""
    
    def initialize(self) -> bool:
        """Initialize Google AI client."""
        try:
            self.is_initialized = True
            return True
        except Exception as e:
            print(f"Google AI initialization failed: {e}")
            return False
    
    def generate(self, prompt: str, **kwargs) -> ModelResponse:
        """Generate response using Google AI API."""
        if not self.is_initialized:
            raise RuntimeError("Google provider not initialized")
        
        return ModelResponse(
            content=f"[Google {self.config.model_name}] Response to: {prompt[:50]}...",
            model=self.config.model_name,
            provider=self.config.provider.value,
            tokens_used=100
        )
    
    def chat(self, messages: List[Dict[str, str]], **kwargs) -> ModelResponse:
        """Chat using Google AI API."""
        if not self.is_initialized:
            raise RuntimeError("Google provider not initialized")
        
        last_message = messages[-1]['content'] if messages else ""
        return ModelResponse(
            content=f"[Google {self.config.model_name}] Chat response to: {last_message[:50]}...",
            model=self.config.model_name,
            provider=self.config.provider.value,
            tokens_used=150
        )
    
    def is_available(self) -> bool:
        """Check if Google AI API is available."""
        return self.config.api_key is not None


# ============================================================================
# OFFLINE MODEL PROVIDERS
# ============================================================================

class LlamaCppProvider(BaseModelProvider):
    """Llama.cpp offline model provider."""
    
    def initialize(self) -> bool:
        """Initialize llama.cpp model."""
        try:
            # Placeholder for actual llama.cpp initialization
            # In production: from llama_cpp import Llama; self.model = Llama(model_path=...)
            if not self.config.model_path:
                raise ValueError("model_path required for offline models")
            self.is_initialized = True
            return True
        except Exception as e:
            print(f"Llama.cpp initialization failed: {e}")
            return False
    
    def generate(self, prompt: str, **kwargs) -> ModelResponse:
        """Generate response using llama.cpp."""
        if not self.is_initialized:
            raise RuntimeError("Llama.cpp provider not initialized")
        
        # Placeholder implementation
        # In production: response = self.model(prompt, max_tokens=..., temperature=...)
        return ModelResponse(
            content=f"[Offline Llama.cpp] Response to: {prompt[:50]}...",
            model=self.config.model_name,
            provider=self.config.provider.value,
            tokens_used=100
        )
    
    def chat(self, messages: List[Dict[str, str]], **kwargs) -> ModelResponse:
        """Chat using llama.cpp."""
        if not self.is_initialized:
            raise RuntimeError("Llama.cpp provider not initialized")
        
        # Convert messages to prompt
        prompt = "\n".join([f"{m['role']}: {m['content']}" for m in messages])
        return self.generate(prompt, **kwargs)
    
    def is_available(self) -> bool:
        """Check if llama.cpp model file exists."""
        import os
        return self.config.model_path and os.path.exists(self.config.model_path)


class OllamaProvider(BaseModelProvider):
    """Ollama offline model provider."""
    
    def initialize(self) -> bool:
        """Initialize Ollama client."""
        try:
            # Placeholder for actual Ollama initialization
            # In production: import ollama; self.client = ollama.Client(host=...)
            self.is_initialized = True
            return True
        except Exception as e:
            print(f"Ollama initialization failed: {e}")
            return False
    
    def generate(self, prompt: str, **kwargs) -> ModelResponse:
        """Generate response using Ollama."""
        if not self.is_initialized:
            raise RuntimeError("Ollama provider not initialized")
        
        # Placeholder implementation
        # In production: response = ollama.generate(model=..., prompt=...)
        return ModelResponse(
            content=f"[Ollama {self.config.model_name}] Response to: {prompt[:50]}...",
            model=self.config.model_name,
            provider=self.config.provider.value,
            tokens_used=100
        )
    
    def chat(self, messages: List[Dict[str, str]], **kwargs) -> ModelResponse:
        """Chat using Ollama."""
        if not self.is_initialized:
            raise RuntimeError("Ollama provider not initialized")
        
        # Placeholder implementation
        # In production: response = ollama.chat(model=..., messages=...)
        last_message = messages[-1]['content'] if messages else ""
        return ModelResponse(
            content=f"[Ollama {self.config.model_name}] Chat response to: {last_message[:50]}...",
            model=self.config.model_name,
            provider=self.config.provider.value,
            tokens_used=150
        )
    
    def is_available(self) -> bool:
        """Check if Ollama is running."""
        try:
            # In production: check if Ollama service is running
            # import requests; requests.get(self.config.base_url or "http://localhost:11434")
            return True
        except:
            return False


class TransformersProvider(BaseModelProvider):
    """HuggingFace Transformers offline model provider."""
    
    def initialize(self) -> bool:
        """Initialize Transformers model."""
        try:
            # Placeholder for actual Transformers initialization
            # In production: from transformers import AutoModelForCausalLM, AutoTokenizer
            # self.model = AutoModelForCausalLM.from_pretrained(...)
            # self.tokenizer = AutoTokenizer.from_pretrained(...)
            self.is_initialized = True
            return True
        except Exception as e:
            print(f"Transformers initialization failed: {e}")
            return False
    
    def generate(self, prompt: str, **kwargs) -> ModelResponse:
        """Generate response using Transformers."""
        if not self.is_initialized:
            raise RuntimeError("Transformers provider not initialized")
        
        # Placeholder implementation
        # In production: inputs = self.tokenizer(prompt, return_tensors="pt")
        # outputs = self.model.generate(**inputs, max_new_tokens=...)
        return ModelResponse(
            content=f"[Transformers {self.config.model_name}] Response to: {prompt[:50]}...",
            model=self.config.model_name,
            provider=self.config.provider.value,
            tokens_used=100
        )
    
    def chat(self, messages: List[Dict[str, str]], **kwargs) -> ModelResponse:
        """Chat using Transformers."""
        if not self.is_initialized:
            raise RuntimeError("Transformers provider not initialized")
        
        # Apply chat template
        prompt = "\n".join([f"{m['role']}: {m['content']}" for m in messages])
        return self.generate(prompt, **kwargs)
    
    def is_available(self) -> bool:
        """Check if Transformers model is available."""
        try:
            # In production: check if model files exist
            return True
        except:
            return False


# ============================================================================
# MODEL MANAGER
# ============================================================================

class ModelManager:
    """Manages multiple AI model providers."""
    
    def __init__(self):
        self.providers: Dict[str, BaseModelProvider] = {}
        self.active_provider: Optional[str] = None
        self.fallback_order: List[str] = []
    
    def register_provider(self, name: str, provider: BaseModelProvider) -> bool:
        """Register a model provider."""
        if provider.initialize():
            self.providers[name] = provider
            if not self.active_provider:
                self.active_provider = name
            return True
        return False
    
    def set_active_provider(self, name: str) -> bool:
        """Set the active model provider."""
        if name in self.providers:
            self.active_provider = name
            return True
        return False
    
    def set_fallback_order(self, provider_names: List[str]):
        """Set fallback order for providers."""
        self.fallback_order = [n for n in provider_names if n in self.providers]
    
    def get_active_provider(self) -> Optional[BaseModelProvider]:
        """Get the currently active provider."""
        if self.active_provider:
            return self.providers.get(self.active_provider)
        return None
    
    def list_providers(self) -> List[Dict[str, Any]]:
        """List all registered providers."""
        return [
            {
                'name': name,
                'info': provider.get_info(),
                'available': provider.is_available(),
                'is_active': name == self.active_provider
            }
            for name, provider in self.providers.items()
        ]
    
    def generate(self, prompt: str, use_fallback: bool = True, **kwargs) -> ModelResponse:
        """Generate response using active provider with optional fallback."""
        providers_to_try = [self.active_provider] if self.active_provider else []
        
        if use_fallback:
            providers_to_try.extend(self.fallback_order)
        
        last_error = None
        for provider_name in providers_to_try:
            provider = self.providers.get(provider_name)
            if provider and provider.is_available():
                try:
                    return provider.generate(prompt, **kwargs)
                except Exception as e:
                    last_error = e
                    continue
        
        raise RuntimeError(f"No available providers. Last error: {last_error}")
    
    def chat(self, messages: List[Dict[str, str]], use_fallback: bool = True, **kwargs) -> ModelResponse:
        """Chat using active provider with optional fallback."""
        providers_to_try = [self.active_provider] if self.active_provider else []
        
        if use_fallback:
            providers_to_try.extend(self.fallback_order)
        
        last_error = None
        for provider_name in providers_to_try:
            provider = self.providers.get(provider_name)
            if provider and provider.is_available():
                try:
                    return provider.chat(messages, **kwargs)
                except Exception as e:
                    last_error = e
                    continue
        
        raise RuntimeError(f"No available providers. Last error: {last_error}")


# ============================================================================
# FACTORY FUNCTIONS
# ============================================================================

def create_provider(config: ModelConfig) -> BaseModelProvider:
    """Factory function to create a model provider."""
    provider_map = {
        ModelProvider.OPENAI: OpenAIProvider,
        ModelProvider.ANTHROPIC: AnthropicProvider,
        ModelProvider.GOOGLE: GoogleProvider,
        ModelProvider.LLAMA_CPP: LlamaCppProvider,
        ModelProvider.OLLAMA: OllamaProvider,
        ModelProvider.TRANSFORMERS: TransformersProvider,
    }
    
    provider_class = provider_map.get(config.provider)
    if not provider_class:
        raise ValueError(f"Unsupported provider: {config.provider}")
    
    return provider_class(config)


def create_model_manager_with_defaults() -> ModelManager:
    """Create a model manager with default configurations."""
    manager = ModelManager()
    
    # Try to add offline models first (no API keys needed)
    offline_configs = [
        ModelConfig(
            provider=ModelProvider.OLLAMA,
            model_name="llama2",
            model_type=ModelType.OFFLINE,
            base_url="http://localhost:11434",
            capabilities=['chat', 'code', 'completion']
        ),
        ModelConfig(
            provider=ModelProvider.LLAMA_CPP,
            model_name="llama-7b",
            model_type=ModelType.OFFLINE,
            model_path="./models/llama-7b.gguf",
            capabilities=['chat', 'code', 'completion']
        ),
    ]
    
    for config in offline_configs:
        try:
            provider = create_provider(config)
            manager.register_provider(f"{config.provider.value}_{config.model_name}", provider)
        except Exception as e:
            print(f"Skipping {config.provider.value}: {e}")
    
    # Set fallback order (offline first, then online)
    manager.set_fallback_order([
        "ollama_llama2",
        "llama_cpp_llama-7b",
    ])
    
    return manager


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_available_models() -> Dict[str, List[str]]:
    """Get list of available models by type."""
    return {
        'online': [
            'openai/gpt-4',
            'openai/gpt-3.5-turbo',
            'anthropic/claude-3-opus',
            'anthropic/claude-3-sonnet',
            'google/gemini-pro',
            'cohere/command',
            'mistral/mistral-large',
        ],
        'offline': [
            'ollama/llama2',
            'ollama/mistral',
            'ollama/codellama',
            'llama_cpp/llama-7b',
            'llama_cpp/llama-13b',
            'transformers/gpt2',
            'transformers/codegen',
        ]
    }


def load_model_config_from_file(filepath: str) -> List[ModelConfig]:
    """Load model configurations from a JSON file."""
    with open(filepath, 'r') as f:
        data = json.load(f)
    
    configs = []
    for item in data:
        config = ModelConfig(
            provider=ModelProvider(item['provider']),
            model_name=item['model_name'],
            model_type=ModelType(item['model_type']),
            api_key=item.get('api_key'),
            base_url=item.get('base_url'),
            model_path=item.get('model_path'),
            max_tokens=item.get('max_tokens', 2048),
            temperature=item.get('temperature', 0.7),
            context_window=item.get('context_window', 4096),
            capabilities=item.get('capabilities', ['chat', 'completion'])
        )
        configs.append(config)
    
    return configs
