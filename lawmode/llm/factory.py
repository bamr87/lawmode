"""Factory for creating LLM backends."""

from typing import Any, Dict

from langchain_openai import ChatOpenAI

from lawmode.config import LLMConfig
from lawmode.llm.base import LLMBackend
from lawmode.llm.grok import ChatGrok


class OpenAIBackend(LLMBackend):
    """OpenAI LLM backend."""

    def _create_model(self):
        return ChatOpenAI(
            model=self.config.get("model", "gpt-4o"),
            temperature=self.config.get("temperature", 0.1),
            max_tokens=self.config.get("max_tokens", 4000),
            api_key=self.config.get("api_key"),
        )


class GrokBackend(LLMBackend):
    """xAI Grok LLM backend."""

    def _create_model(self):
        return ChatGrok(
            model_name=self.config.get("model", "grok-2-1212"),  # Default to latest stable model
            temperature=self.config.get("temperature", 0.1),
            max_tokens=self.config.get("max_tokens", 4000),
            api_key=self.config.get("api_key"),
        )


def create_llm_backend(config: LLMConfig) -> LLMBackend:
    """Create an LLM backend from configuration."""
    provider = config.provider.lower()
    
    backend_config = {
        "model": config.model,
        "temperature": config.temperature,
        "max_tokens": config.max_tokens,
        "api_key": config.api_key or _get_api_key(provider),
    }
    
    if provider == "openai":
        return OpenAIBackend(backend_config)
    elif provider == "grok":
        return GrokBackend(backend_config)
    else:
        raise ValueError(f"Unsupported LLM provider: {provider}. Supported: openai, grok")


def _get_api_key(provider: str) -> str:
    """Get API key from environment variables."""
    import os
    
    key_map = {
        "openai": "OPENAI_API_KEY",
        "grok": "XAI_API_KEY",  # xAI uses XAI_API_KEY
    }
    
    env_var = key_map.get(provider.lower())
    if env_var:
        return os.getenv(env_var, "")
    return ""

