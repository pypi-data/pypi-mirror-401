"""Enhanced online model adapter with support for multiple AI providers."""

from __future__ import annotations

import os
from typing import Any, Dict, Optional

from models.base import BaseModel


class OnlineAPIAdapter(BaseModel):
    """
    Online model adapter supporting multiple AI API providers with usage tracking.
    
    Supported providers:
    - OpenAI (GPT-4, GPT-3.5, etc.)
    - Anthropic (Claude 3.x)
    - Google (Gemini Pro, Gemini Pro Vision)
    - Cohere (Command, Command Light)
    - HuggingFace (Inference API)
    - OpenRouter (multiple models)
    """

    def __init__(
        self,
        provider: str = "openai",
        model_name: str = "gpt-3.5-turbo",
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        name: Optional[str] = None,
        max_retries: int = 3,
        timeout: int = 30,
        track_usage: bool = True,
    ) -> None:
        display_name = name or f"axon-online-{provider}-{model_name}"
        super().__init__(name=display_name)
        
        self.provider = provider.lower()
        self.model_name = model_name
        self.api_key = api_key or self._get_api_key_from_env()
        self.base_url = base_url
        self.max_retries = max_retries
        self.timeout = timeout
        self.track_usage = track_usage
        self._client = None
        self._mock_mode = False

        if not self.api_key:
            raise ValueError(
                f"No API key found for {provider}. "
                f"Set {self._get_env_var_name()} environment variable or use 'anox config api add' command."
            )
        
        self._initialize_client()

    def _get_env_var_name(self) -> str:
        """Get the environment variable name for the API key."""
        env_vars = {
            "openai": "OPENAI_API_KEY",
            "anthropic": "ANTHROPIC_API_KEY",
            "google": "GOOGLE_API_KEY",
            "openrouter": "OPENROUTER_API_KEY",
            "cohere": "COHERE_API_KEY",
            "huggingface": "HUGGINGFACE_API_KEY",
        }
        return env_vars.get(self.provider, f"{self.provider.upper()}_API_KEY")

    def _get_api_key_from_env(self) -> Optional[str]:
        """Get API key from environment variables."""
        return os.environ.get(self._get_env_var_name())

    def _initialize_client(self) -> None:
        """Initialize the API client."""
        try:
            if self.provider == "openai":
                from openai import OpenAI
                self._client = OpenAI(
                    api_key=self.api_key,
                    base_url=self.base_url,
                    timeout=self.timeout,
                    max_retries=self.max_retries,
                )
            elif self.provider == "anthropic":
                from anthropic import Anthropic
                self._client = Anthropic(
                    api_key=self.api_key,
                    timeout=self.timeout,
                    max_retries=self.max_retries,
                )
            elif self.provider == "google":
                import google.generativeai as genai
                genai.configure(api_key=self.api_key)
                self._client = genai
            elif self.provider == "cohere":
                import cohere
                self._client = cohere.Client(
                    api_key=self.api_key,
                    timeout=self.timeout,
                )
            elif self.provider == "huggingface":
                from huggingface_hub import InferenceClient
                self._client = InferenceClient(token=self.api_key)
            else:
                # Generic OpenAI-compatible API
                from openai import OpenAI
                self._client = OpenAI(
                    api_key=self.api_key,
                    base_url=self.base_url or "https://api.openai.com/v1",
                    timeout=self.timeout,
                    max_retries=self.max_retries,
                )
            
            print(f"✓ Initialized {self.provider} client with model {self.model_name}")
            
        except ImportError as e:
            required_package = self._get_required_package()
            raise ImportError(
                f"Required library not installed for {self.provider}: {e}\n"
                f"Install with: pip install {required_package}"
            )
        except Exception as e:
            raise RuntimeError(f"Failed to initialize {self.provider} client: {e}")

    def _get_required_package(self) -> str:
        """Get the required package name for installation."""
        packages = {
            "openai": "openai",
            "anthropic": "anthropic",
            "google": "google-generativeai",
            "cohere": "cohere",
            "huggingface": "huggingface-hub",
        }
        return packages.get(self.provider, "openai")

    def generate(self, prompt: str, context: Dict[str, Any]) -> str:
        """Generate response using the online API."""
        if self._mock_mode or not self._client:
            raise RuntimeError(
                f"API client not initialized for {self.provider}. "
                f"Please configure API key using 'anox config api add' command."
            )

        try:
            if self.provider == "openai":
                return self._generate_openai(prompt, context)
            elif self.provider == "anthropic":
                return self._generate_anthropic(prompt, context)
            elif self.provider == "google":
                return self._generate_google(prompt, context)
            elif self.provider == "cohere":
                return self._generate_cohere(prompt, context)
            elif self.provider == "huggingface":
                return self._generate_huggingface(prompt, context)
            else:
                return self._generate_openai(prompt, context)
        except Exception as e:
            # Log the error and re-raise with more context
            error_msg = f"API call to {self.provider} failed: {str(e)}"
            print(f"❌ {error_msg}")
            raise RuntimeError(error_msg) from e

    def _generate_openai(self, prompt: str, context: Dict[str, Any]) -> str:
        """Generate using OpenAI API."""
        system_prompt = self._build_system_prompt(context)
        max_tokens = context.get("max_tokens", 1024)
        temperature = context.get("temperature", 0.7)

        response = self._client.chat.completions.create(
            model=self.model_name,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt},
            ],
            max_tokens=max_tokens,
            temperature=temperature,
        )

        # Track usage
        if self.track_usage and hasattr(response, 'usage'):
            self._track_usage(
                input_tokens=response.usage.prompt_tokens,
                output_tokens=response.usage.completion_tokens,
                context=context
            )

        return response.choices[0].message.content

    def _generate_anthropic(self, prompt: str, context: Dict[str, Any]) -> str:
        """Generate using Anthropic API."""
        system_prompt = self._build_system_prompt(context)
        max_tokens = context.get("max_tokens", 1024)
        temperature = context.get("temperature", 0.7)

        message = self._client.messages.create(
            model=self.model_name,
            max_tokens=max_tokens,
            temperature=temperature,
            system=system_prompt,
            messages=[{"role": "user", "content": prompt}],
        )

        # Track usage
        if self.track_usage and hasattr(message, 'usage'):
            self._track_usage(
                input_tokens=message.usage.input_tokens,
                output_tokens=message.usage.output_tokens,
                context=context
            )

        return message.content[0].text

    def _generate_google(self, prompt: str, context: Dict[str, Any]) -> str:
        """Generate using Google Gemini API."""
        system_prompt = self._build_system_prompt(context)
        full_prompt = f"{system_prompt}\n\n{prompt}"

        model = self._client.GenerativeModel(self.model_name)
        response = model.generate_content(full_prompt)

        return response.text

    def _generate_cohere(self, prompt: str, context: Dict[str, Any]) -> str:
        """Generate using Cohere API."""
        system_prompt = self._build_system_prompt(context)
        max_tokens = context.get("max_tokens", 1024)
        temperature = context.get("temperature", 0.7)

        try:
            # Try chat method first (newer API)
            response = self._client.chat(
                model=self.model_name,
                message=prompt,
                preamble=system_prompt,
                max_tokens=max_tokens,
                temperature=temperature,
            )
            return response.text
        except (AttributeError, TypeError):
            # Fallback to generate method for older API versions
            response = self._client.generate(
                model=self.model_name,
                prompt=f"{system_prompt}\n\n{prompt}",
                max_tokens=max_tokens,
                temperature=temperature,
            )
            return response.generations[0].text

    def _generate_huggingface(self, prompt: str, context: Dict[str, Any]) -> str:
        """Generate using HuggingFace Inference API."""
        system_prompt = self._build_system_prompt(context)
        max_tokens = context.get("max_tokens", 1024)
        temperature = context.get("temperature", 0.7)
        
        full_prompt = f"{system_prompt}\n\n{prompt}"

        response = self._client.text_generation(
            model=self.model_name,
            inputs=full_prompt,
            parameters={
                "max_new_tokens": max_tokens,
                "temperature": temperature,
            }
        )

        return response


    def health_check(self) -> bool:
        """Check if the API is accessible."""
        if self._mock_mode or not self._client:
            return False

        try:
            # Simple health check by making a minimal API call
            if self.provider == "openai":
                self._client.models.list()
                return True
            elif self.provider == "anthropic":
                # Anthropic doesn't have a models.list endpoint, so we make a minimal generation call
                try:
                    self._client.messages.create(
                        model=self.model_name,
                        max_tokens=10,
                        messages=[{"role": "user", "content": "Hi"}]
                    )
                    return True
                except Exception:
                    return False
            elif self.provider == "google":
                # Google Gemini health check
                try:
                    model = self._client.GenerativeModel(self.model_name)
                    return True
                except Exception:
                    return False
            else:
                # Default health check
                return True
        except Exception:
            return False

    def _track_usage(
        self,
        input_tokens: int,
        output_tokens: int,
        context: Dict[str, Any]
    ) -> None:
        """Track token usage.
        
        Args:
            input_tokens: Number of input tokens.
            output_tokens: Number of output tokens.
            context: Context dictionary with task information.
        """
        try:
            from models.usage_tracker import get_usage_tracker
            
            tracker = get_usage_tracker()
            task_type = context.get("task_type", "general")
            
            tracker.track_usage(
                provider=self.provider,
                model=self.model_name,
                input_tokens=input_tokens,
                output_tokens=output_tokens,
                task_type=task_type
            )
        except Exception as e:
            # Don't fail the request if tracking fails
            print(f"⚠️  Failed to track usage: {e}")

    def get_info(self) -> Dict[str, Any]:
        """Get model information."""
        info = {
            "name": self.name,
            "type": "online-api",
            "provider": self.provider,
            "model": self.model_name,
            "api_key_configured": bool(self.api_key),
            "max_retries": self.max_retries,
            "timeout": self.timeout,
            "track_usage": self.track_usage,
        }
        
        # Add usage stats if available
        if self.track_usage:
            try:
                from models.usage_tracker import get_usage_tracker
                tracker = get_usage_tracker()
                usage = tracker.get_total_usage(provider=self.provider)
                info["usage"] = usage
            except Exception:
                pass
        
        return info
