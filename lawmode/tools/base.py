"""Base class for legal research tools."""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

from langchain_core.tools import StructuredTool
from pydantic import BaseModel, Field


class LegalTool(StructuredTool, ABC):
    """Base class for legal research tools."""

    @abstractmethod
    def _run(self, *args: Any, **kwargs: Any) -> str:
        """Execute the tool and return results."""
        pass

    async def _arun(self, *args: Any, **kwargs: Any) -> str:
        """Async version of _run."""
        return self._run(*args, **kwargs)

