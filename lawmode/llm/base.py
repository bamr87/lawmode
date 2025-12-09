"""Base LLM backend interface."""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

from langchain_core.language_models import BaseChatModel
from langchain_core.messages import BaseMessage


class LLMBackend(ABC):
    """Abstract base class for LLM backends."""

    def __init__(self, config: Dict[str, Any]):
        """Initialize LLM backend with configuration."""
        self.config = config
        self.model = self._create_model()

    @abstractmethod
    def _create_model(self) -> BaseChatModel:
        """Create and return the LangChain model instance."""
        pass

    def invoke(self, messages: List[BaseMessage], **kwargs: Any) -> BaseMessage:
        """Invoke the LLM with messages."""
        return self.model.invoke(messages, **kwargs)

    def stream(self, messages: List[BaseMessage], **kwargs: Any):
        """Stream responses from the LLM."""
        return self.model.stream(messages, **kwargs)

    def bind_tools(self, tools: List[Any]) -> BaseChatModel:
        """Bind tools to the model for forced tool use."""
        return self.model.bind_tools(tools)

