"""xAI Grok LLM backend implementation."""

from typing import Any, Dict, List, Optional

from langchain_core.language_models import BaseChatModel
from langchain_core.messages import (
    AIMessage,
    BaseMessage,
    HumanMessage,
    SystemMessage,
)
from langchain_core.outputs import ChatGeneration, ChatResult
from langchain_core.callbacks import CallbackManagerForLLMRun
from pydantic import Field


class ChatGrok(BaseChatModel):
    """xAI Grok chat model wrapper for LangChain."""

    model_name: str = Field(default="grok-2-1212")  # Updated default model
    temperature: float = Field(default=0.1)
    max_tokens: int = Field(default=4000)
    api_key: Optional[str] = Field(default=None)
    base_url: str = Field(default="https://api.x.ai/v1")

    @property
    def _llm_type(self) -> str:
        """Return type of LLM."""
        return "grok"

    def _generate(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> ChatResult:
        """Generate a response from the model."""
        try:
            import requests
        except ImportError:
            raise ImportError(
                "requests package is required. Install with: pip install requests"
            )

        # Convert LangChain messages to xAI format
        xai_messages = []
        for msg in messages:
            if isinstance(msg, SystemMessage):
                xai_messages.append({"role": "system", "content": msg.content})
            elif isinstance(msg, HumanMessage):
                xai_messages.append({"role": "user", "content": msg.content})
            elif isinstance(msg, AIMessage):
                xai_messages.append({"role": "assistant", "content": msg.content})

        # Prepare API request
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": self.model_name,
            "messages": xai_messages,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
        }

        if stop:
            payload["stop"] = stop

        # Make API request
        response = requests.post(
            f"{self.base_url}/chat/completions",
            headers=headers,
            json=payload,
            timeout=30,
        )

        if response.status_code != 200:
            error_msg = f"xAI API error: {response.status_code}"
            try:
                error_data = response.json()
                error_msg += f" - {error_data}"
            except:
                error_msg += f" - {response.text}"
            raise RuntimeError(error_msg)

        result = response.json()

        # Extract response
        if "choices" not in result or len(result["choices"]) == 0:
            raise RuntimeError("No choices in xAI API response")

        choice = result["choices"][0]
        message_content = choice["message"]["content"]

        # Create LangChain message
        message = AIMessage(content=message_content)

        # Create generation
        generation = ChatGeneration(message=message)

        return ChatResult(generations=[generation])

    def bind_tools(self, tools: List[Any]) -> "ChatGrok":
        """Bind tools to the model (xAI Grok supports function calling)."""
        # For now, return self - tool binding can be enhanced later
        # xAI Grok supports function calling via the API
        return self

