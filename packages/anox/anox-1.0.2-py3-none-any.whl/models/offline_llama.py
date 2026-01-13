"""Enhanced offline model adapter with llama.cpp support."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Dict, Optional

from models.base import BaseModel


class OfflineLlamaAdapter(BaseModel):
    """
    Offline model adapter supporting llama.cpp with GGUF models.
    
    Supports local models for true offline operation.
    Falls back to mock mode if llama-cpp-python is not installed.
    """

    def __init__(
        self,
        model_path: Optional[str] = None,
        name: str = "axon-offline-llama",
        n_ctx: int = 4096,
        n_threads: Optional[int] = None,
        use_gpu: bool = False,
    ) -> None:
        super().__init__(name=name)
        self.model_path = model_path
        self.n_ctx = n_ctx
        self.n_threads = n_threads or os.cpu_count() or 4
        self.use_gpu = use_gpu
        self._llama = None
        self._mock_mode = False

        if model_path:
            self._initialize_model()
        else:
            self._mock_mode = True

    def _initialize_model(self) -> None:
        """Initialize the llama.cpp model."""
        try:
            from llama_cpp import Llama

            if not self.model_path or not Path(self.model_path).exists():
                print(f"⚠️  Model file not found: {self.model_path}")
                print("   Falling back to mock mode")
                self._mock_mode = True
                return

            print(f"Loading model: {self.model_path}")
            self._llama = Llama(
                model_path=self.model_path,
                n_ctx=self.n_ctx,
                n_threads=self.n_threads,
                n_gpu_layers=-1 if self.use_gpu else 0,
                verbose=False,
            )
            print("✓ Model loaded successfully")

        except ImportError:
            print("⚠️  llama-cpp-python not installed")
            print("   Install with: pip install llama-cpp-python")
            print("   For GPU: CMAKE_ARGS='-DLLAMA_CUBLAS=on' pip install llama-cpp-python")
            print("   Falling back to mock mode")
            self._mock_mode = True
        except Exception as e:
            print(f"⚠️  Failed to load model: {e}")
            print("   Falling back to mock mode")
            self._mock_mode = True

    def generate(self, prompt: str, context: Dict[str, Any]) -> str:
        """Generate response using the model."""
        if self._mock_mode or not self._llama:
            return self._mock_generate(prompt, context)

        try:
            # Extract parameters from context
            max_tokens = context.get("max_tokens", 512)
            temperature = context.get("temperature", 0.7)
            top_p = context.get("top_p", 0.9)

            # Build system prompt based on context
            system_prompt = self._build_system_prompt(context)
            full_prompt = f"{system_prompt}\n\nUser: {prompt}\n\nAssistant:"

            # Generate response
            response = self._llama(
                full_prompt,
                max_tokens=max_tokens,
                temperature=temperature,
                top_p=top_p,
                stop=["User:", "\n\n"],
                echo=False,
            )

            return response["choices"][0]["text"].strip()

        except Exception as e:
            print(f"⚠️  Generation error: {e}")
            return self._mock_generate(prompt, context)



    def _mock_generate(self, prompt: str, context: Dict[str, Any]) -> str:
        """Mock generation for when model is not available."""
        intent_action = context.get("intent_action", "unknown_action")
        role = context.get("identity_role", "unknown_role")
        domain = context.get("intent_domain", "unknown_domain")
        task_type = context.get("task_type", "general")

        return (
            f"[OFFLINE-MOCK:{self.name}] "
            f"role={role} domain={domain} task={task_type} action={intent_action}\n"
            f"Query: {prompt[:100]}{'...' if len(prompt) > 100 else ''}"
        )

    def health_check(self) -> bool:
        """Check if the model is healthy."""
        if self._mock_mode:
            return True
        return self._llama is not None

    def get_info(self) -> Dict[str, Any]:
        """Get model information."""
        return {
            "name": self.name,
            "type": "offline-llama",
            "model_path": self.model_path,
            "mock_mode": self._mock_mode,
            "context_size": self.n_ctx,
            "threads": self.n_threads,
            "gpu_enabled": self.use_gpu,
        }
