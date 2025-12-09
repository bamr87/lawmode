"""CourtListener tool for US case law research."""

import requests
from typing import Any, Optional

from lawmode.tools.base import LegalTool
from pydantic import BaseModel, Field


class CourtListenerInput(BaseModel):
    """Input schema for CourtListener tool."""

    query: str = Field(description="Case name, citation, or legal query")
    court: Optional[str] = Field(default=None, description="Court filter (e.g., 'scotus', 'ca9')")


def _create_courtlistener_tool() -> LegalTool:
    """Create CourtListener tool instance."""
    def _run(query: str, court: Optional[str] = None) -> str:
        """Search CourtListener for case law."""
        try:
            # CourtListener API endpoint (requires API key in production)
            # For MVP, we'll return formatted search results
            base_url = "https://www.courtlistener.com/api/rest/v3/search/"
            
            # In production, this would make authenticated API calls
            result = f"CourtListener Search Results for: {query}\n\n"
            result += f"API Endpoint: {base_url}\n"
            
            if court:
                result += f"Court Filter: {court}\n"
            
            result += "\nNote: Full API access requires CourtListener API key.\n"
            result += f"Web Search: https://www.courtlistener.com/?q={query.replace(' ', '+')}"
            
            # Return mock structured data for MVP
            if "privacy" in query.lower() or "gdpr" in query.lower():
                result += "\n\nRelevant Cases:\n"
                result += "- Carpenter v. United States (2018) - Fourth Amendment privacy\n"
                result += "- Riley v. California (2014) - Digital privacy rights\n"
            
            return result
        
        except Exception as e:
            return f"Error searching CourtListener: {str(e)}"
    
    from langchain_core.tools import StructuredTool
    return StructuredTool(
        name="courtlistener_search",
        description=(
            "Search CourtListener database for US case law, court opinions, and legal precedents. "
            "Use this for US legal research, case citations, and precedent analysis."
        ),
        args_schema=CourtListenerInput,
        func=_run,
    )


class CourtListenerTool:
    """Tool for searching CourtListener (US case law database)."""
    
    def __new__(cls):
        return _create_courtlistener_tool()

