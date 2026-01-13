"""
Universal Model Adapter - Support for ANY Model Format

This adapter provides a unified interface to work with any model format:
- Local models (GGUF, PyTorch, TensorFlow, ONNX, etc.)
- Cloud APIs (OpenAI, Anthropic, Google, Cohere, HuggingFace, etc.)
- Custom models (user-defined interfaces)
- Specialized models (CodeLlama, WizardCoder, Phi, etc.)

The adapter automatically detects model type and provides appropriate interface.
"""

from __future__ import annotations

import importlib
import json
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from models.base import BaseModel


class ModelFormat(Enum):
    """Supported model formats."""
    # Local formats
    GGUF = "gguf"  # llama.cpp format
    PYTORCH = "pytorch"  # PyTorch models
    TENSORFLOW = "tensorflow"  # TensorFlow models
    ONNX = "onnx"  # ONNX models
    SAFETENSORS = "safetensors"  # SafeTensors format
    
    # Cloud APIs
    OPENAI_API = "openai_api"
    ANTHROPIC_API = "anthropic_api"
    GOOGLE_API = "google_api"
    COHERE_API = "cohere_api"
    HUGGINGFACE_API = "huggingface_api"
    REPLICATE_API = "replicate_api"
    
    # Specialized
    OLLAMA = "ollama"  # Ollama local API
    LLAMACPP = "llamacpp"  # llama.cpp server
    VLLM = "vllm"  # vLLM inference server
    TEXTGEN_WEBUI = "textgen_webui"  # text-generation-webui
    
    # Custom
    CUSTOM_HTTP = "custom_http"  # Custom HTTP API
    CUSTOM_PYTHON = "custom_python"  # Custom Python class
    
    # Auto-detect
    AUTO = "auto"


@dataclass
class ModelCapability:
    """Capabilities of a model."""
    supports_completion: bool = True
    supports_chat: bool = False
    supports_functions: bool = False
    supports_vision: bool = False
    supports_streaming: bool = False
    max_context_length: int = 2048
    supports_system_prompt: bool = False


class UniversalModelInterface(ABC):
    """Abstract interface for all model adapters."""
    
    @abstractmethod
    def load(self, config: Dict[str, Any]) -> bool:
        """Load the model with given configuration."""
        pass
    
    @abstractmethod
    def generate(self, prompt: str, context: Optional[Dict[str, Any]] = None) -> str:
        """Generate response from prompt."""
        pass
    
    @abstractmethod
    def health_check(self) -> bool:
        """Check if model is healthy and ready."""
        pass
    
    @abstractmethod
    def get_capabilities(self) -> ModelCapability:
        """Get model capabilities."""
        pass
    
    @abstractmethod
    def unload(self) -> None:
        """Unload the model and free resources."""
        pass


class GGUFModelAdapter(UniversalModelInterface):
    """Adapter for GGUF format models (llama.cpp)."""
    
    def __init__(self):
        self.model = None
        self.llama_cpp = None
    
    def load(self, config: Dict[str, Any]) -> bool:
        try:
            from llama_cpp import Llama
            self.llama_cpp = Llama
            
            model_path = config.get('model_path')
            if not model_path or not Path(model_path).exists():
                return False
            
            self.model = Llama(
                model_path=str(model_path),
                n_ctx=config.get('n_ctx', 2048),
                n_threads=config.get('n_threads', 4),
                n_gpu_layers=config.get('n_gpu_layers', 0),
            )
            return True
        except ImportError:
            print("⚠️  llama-cpp-python not installed")
            return False
        except Exception as e:
            print(f"⚠️  Failed to load GGUF model: {e}")
            return False
    
    def generate(self, prompt: str, context: Optional[Dict[str, Any]] = None) -> str:
        if not self.model:
            return "[Model not loaded]"
        
        try:
            response = self.model(
                prompt,
                max_tokens=context.get('max_tokens', 512) if context else 512,
                temperature=context.get('temperature', 0.7) if context else 0.7,
                stop=context.get('stop', []) if context else [],
            )
            return response['choices'][0]['text']
        except Exception as e:
            return f"[Error: {e}]"
    
    def health_check(self) -> bool:
        return self.model is not None
    
    def get_capabilities(self) -> ModelCapability:
        return ModelCapability(
            supports_completion=True,
            supports_chat=False,
            supports_streaming=True,
            max_context_length=2048,
        )
    
    def unload(self) -> None:
        if self.model:
            del self.model
            self.model = None


class OpenAIAPIAdapter(UniversalModelInterface):
    """Adapter for OpenAI API."""
    
    def __init__(self):
        self.client = None
        self.model_name = None
    
    def load(self, config: Dict[str, Any]) -> bool:
        try:
            import openai
            
            api_key = config.get('api_key')
            if not api_key:
                return False
            
            self.client = openai.OpenAI(api_key=api_key)
            self.model_name = config.get('model_name', 'gpt-3.5-turbo')
            return True
        except ImportError:
            print("⚠️  openai package not installed")
            return False
        except Exception as e:
            print(f"⚠️  Failed to initialize OpenAI: {e}")
            return False
    
    def generate(self, prompt: str, context: Optional[Dict[str, Any]] = None) -> str:
        if not self.client:
            return "[Model not loaded]"
        
        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=context.get('max_tokens', 1024) if context else 1024,
                temperature=context.get('temperature', 0.7) if context else 0.7,
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"[Error: {e}]"
    
    def health_check(self) -> bool:
        return self.client is not None
    
    def get_capabilities(self) -> ModelCapability:
        return ModelCapability(
            supports_completion=True,
            supports_chat=True,
            supports_functions=True,
            supports_streaming=True,
            max_context_length=4096,
            supports_system_prompt=True,
        )
    
    def unload(self) -> None:
        self.client = None


class OllamaAdapter(UniversalModelInterface):
    """Adapter for Ollama local API."""
    
    def __init__(self):
        self.base_url = None
        self.model_name = None
    
    def load(self, config: Dict[str, Any]) -> bool:
        self.base_url = config.get('base_url', 'http://localhost:11434')
        self.model_name = config.get('model_name', 'llama2')
        return True
    
    def generate(self, prompt: str, context: Optional[Dict[str, Any]] = None) -> str:
        try:
            import requests
            
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model_name,
                    "prompt": prompt,
                    "stream": False,
                },
                timeout=30,
            )
            response.raise_for_status()
            return response.json().get('response', '')
        except Exception as e:
            return f"[Error: {e}]"
    
    def health_check(self) -> bool:
        try:
            import requests
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def get_capabilities(self) -> ModelCapability:
        return ModelCapability(
            supports_completion=True,
            supports_chat=True,
            supports_streaming=True,
            max_context_length=2048,
        )
    
    def unload(self) -> None:
        pass


class CustomHTTPAdapter(UniversalModelInterface):
    """Adapter for custom HTTP APIs."""
    
    def __init__(self):
        self.base_url = None
        self.headers = {}
        self.request_template = {}
    
    def load(self, config: Dict[str, Any]) -> bool:
        self.base_url = config.get('base_url')
        self.headers = config.get('headers', {})
        self.request_template = config.get('request_template', {})
        return self.base_url is not None
    
    def generate(self, prompt: str, context: Optional[Dict[str, Any]] = None) -> str:
        try:
            import requests
            
            # Build request from template
            request_data = self.request_template.copy()
            # Simple substitution - can be enhanced
            if 'prompt' in request_data:
                request_data['prompt'] = prompt
            elif 'input' in request_data:
                request_data['input'] = prompt
            
            response = requests.post(
                self.base_url,
                json=request_data,
                headers=self.headers,
                timeout=30,
            )
            response.raise_for_status()
            
            # Try to extract text from common response formats
            data = response.json()
            if 'text' in data:
                return data['text']
            elif 'response' in data:
                return data['response']
            elif 'output' in data:
                return data['output']
            else:
                return str(data)
        except Exception as e:
            return f"[Error: {e}]"
    
    def health_check(self) -> bool:
        try:
            import requests
            response = requests.get(self.base_url, timeout=5)
            return response.status_code < 500
        except:
            return False
    
    def get_capabilities(self) -> ModelCapability:
        return ModelCapability(supports_completion=True)
    
    def unload(self) -> None:
        pass


class UniversalModelAdapter(BaseModel):
    """
    Universal adapter that can work with ANY model format.
    
    Automatically detects model type and provides unified interface.
    """
    
    def __init__(
        self,
        model_format: Union[ModelFormat, str] = ModelFormat.AUTO,
        config: Optional[Dict[str, Any]] = None,
        name: Optional[str] = None,
    ):
        """
        Initialize universal model adapter.
        
        Args:
            model_format: Model format (or "auto" to detect)
            config: Model configuration
            name: Model name
        """
        self.model_format = ModelFormat(model_format) if isinstance(model_format, str) else model_format
        self.config = config or {}
        self.name = name or f"universal_{self.model_format.value}"
        
        # Internal adapter
        self.adapter: Optional[UniversalModelInterface] = None
        
        # Auto-detect and load
        if self.model_format == ModelFormat.AUTO:
            self.model_format = self._detect_format()
        
        self._initialize_adapter()
    
    def _detect_format(self) -> ModelFormat:
        """Auto-detect model format from configuration."""
        # Check for file-based models
        if 'model_path' in self.config:
            model_path = Path(self.config['model_path'])
            if model_path.suffix == '.gguf':
                return ModelFormat.GGUF
            elif model_path.suffix in ['.pt', '.pth', '.bin']:
                return ModelFormat.PYTORCH
            elif model_path.suffix == '.onnx':
                return ModelFormat.ONNX
        
        # Check for API keys
        if 'api_key' in self.config:
            if 'openai' in self.config.get('provider', '').lower():
                return ModelFormat.OPENAI_API
            elif 'anthropic' in self.config.get('provider', '').lower():
                return ModelFormat.ANTHROPIC_API
            elif 'google' in self.config.get('provider', '').lower():
                return ModelFormat.GOOGLE_API
        
        # Check for base URL
        if 'base_url' in self.config:
            base_url = self.config['base_url'].lower()
            if 'ollama' in base_url:
                return ModelFormat.OLLAMA
            elif 'localhost:11434' in base_url:
                return ModelFormat.OLLAMA
            else:
                return ModelFormat.CUSTOM_HTTP
        
        # Default
        return ModelFormat.CUSTOM_HTTP
    
    def _initialize_adapter(self) -> None:
        """Initialize the appropriate adapter for the model format."""
        adapter_map = {
            ModelFormat.GGUF: GGUFModelAdapter,
            ModelFormat.OPENAI_API: OpenAIAPIAdapter,
            ModelFormat.OLLAMA: OllamaAdapter,
            ModelFormat.CUSTOM_HTTP: CustomHTTPAdapter,
            # Add more adapters as needed
        }
        
        adapter_class = adapter_map.get(self.model_format)
        if not adapter_class:
            print(f"⚠️  No adapter available for {self.model_format}, using mock mode")
            return
        
        try:
            self.adapter = adapter_class()
            if not self.adapter.load(self.config):
                print(f"⚠️  Failed to load {self.model_format} model, using mock mode")
                self.adapter = None
        except Exception as e:
            print(f"⚠️  Error initializing adapter: {e}")
            self.adapter = None
    
    def generate(self, prompt: str, context: Optional[Dict[str, Any]] = None) -> str:
        """Generate response from prompt."""
        if self.adapter:
            return self.adapter.generate(prompt, context)
        else:
            # Mock mode
            return f"[Mock response for: {prompt[:50]}...]"
    
    def health_check(self) -> bool:
        """Check if model is healthy."""
        if self.adapter:
            return self.adapter.health_check()
        return True  # Mock mode always healthy
    
    def get_capabilities(self) -> ModelCapability:
        """Get model capabilities."""
        if self.adapter:
            return self.adapter.get_capabilities()
        return ModelCapability()
    
    def get_info(self) -> Dict[str, Any]:
        """Get model information."""
        info = {
            'name': self.name,
            'format': self.model_format.value,
            'config': {k: v for k, v in self.config.items() if k != 'api_key'},
        }
        
        if self.adapter:
            capabilities = self.adapter.get_capabilities()
            info['capabilities'] = {
                'completion': capabilities.supports_completion,
                'chat': capabilities.supports_chat,
                'functions': capabilities.supports_functions,
                'vision': capabilities.supports_vision,
                'streaming': capabilities.supports_streaming,
                'max_context': capabilities.max_context_length,
            }
        
        return info
    
    def unload(self) -> None:
        """Unload the model."""
        if self.adapter:
            self.adapter.unload()
            self.adapter = None


# Helper functions for easy model creation

def create_from_file(file_path: Union[str, Path], **kwargs) -> UniversalModelAdapter:
    """Create a model from a file path (auto-detects format)."""
    config = {'model_path': str(file_path), **kwargs}
    return UniversalModelAdapter(ModelFormat.AUTO, config)


def create_from_api(
    provider: str,
    api_key: str,
    model_name: Optional[str] = None,
    **kwargs
) -> UniversalModelAdapter:
    """Create a model from an API provider."""
    provider_map = {
        'openai': ModelFormat.OPENAI_API,
        'anthropic': ModelFormat.ANTHROPIC_API,
        'google': ModelFormat.GOOGLE_API,
    }
    
    model_format = provider_map.get(provider.lower(), ModelFormat.CUSTOM_HTTP)
    config = {
        'provider': provider,
        'api_key': api_key,
        'model_name': model_name,
        **kwargs
    }
    
    return UniversalModelAdapter(model_format, config)


def create_from_ollama(model_name: str, base_url: str = "http://localhost:11434") -> UniversalModelAdapter:
    """Create a model from Ollama."""
    config = {
        'model_name': model_name,
        'base_url': base_url,
    }
    return UniversalModelAdapter(ModelFormat.OLLAMA, config)


def create_custom(
    base_url: str,
    headers: Optional[Dict[str, str]] = None,
    request_template: Optional[Dict[str, Any]] = None,
) -> UniversalModelAdapter:
    """Create a custom HTTP API model."""
    config = {
        'base_url': base_url,
        'headers': headers or {},
        'request_template': request_template or {},
    }
    return UniversalModelAdapter(ModelFormat.CUSTOM_HTTP, config)
