"""LLM backend abstraction layer."""

from lawmode.llm.base import LLMBackend
from lawmode.llm.factory import create_llm_backend
from lawmode.llm.grok import ChatGrok

__all__ = ["LLMBackend", "create_llm_backend", "ChatGrok"]

