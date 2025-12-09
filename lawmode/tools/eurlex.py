"""EUR-Lex tool for EU legal research."""

import requests
from typing import Any

from lawmode.tools.base import LegalTool
from pydantic import BaseModel, Field


class EurLexInput(BaseModel):
    """Input schema for EUR-Lex tool."""

    query: str = Field(description="Legal query or article reference (e.g., 'GDPR Art. 32')")
    language: str = Field(default="EN", description="Language code (EN, DE, FR, etc.)")


def _create_eurlex_tool() -> LegalTool:
    """Create EUR-Lex tool instance."""
    def _run(query: str, language: str = "EN") -> str:
        """Search EUR-Lex for legal documents."""
        try:
            # EUR-Lex API endpoint (using the public search API)
            base_url = "https://eur-lex.europa.eu/search.html"
            
            # For MVP, we'll return a formatted response with search instructions
            # In production, this would use the EUR-Lex API or web scraping
            if "GDPR" in query.upper() or "art" in query.lower():
                # Extract article number if present
                article_match = None
                if "art" in query.lower():
                    import re
                    art_match = re.search(r'art[\.\s]+(\d+)', query.lower())
                    if art_match:
                        article_match = art_match.group(1)
                
                result = f"EUR-Lex Search Results for: {query}\n\n"
                result += f"Primary Source: https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32016R0679\n"
                result += f"Document: Regulation (EU) 2016/679 (GDPR)\n"
                
                if article_match:
                    result += f"\nArticle {article_match}:\n"
                    result += f"https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32016R0679#art_{article_match}\n"
                
                result += "\nNote: Full text retrieval requires EUR-Lex API access or web scraping."
                return result
            else:
                return f"EUR-Lex search for '{query}': https://eur-lex.europa.eu/search.html?qid={query.replace(' ', '+')}&type=quick&lang={language}"
        
        except Exception as e:
            return f"Error searching EUR-Lex: {str(e)}"
    
    from langchain_core.tools import StructuredTool
    return StructuredTool(
        name="eurlex_search",
        description=(
            "Search EUR-Lex database for EU legal documents, regulations, directives, "
            "and case law. Use this for GDPR, EU directives, and European legal references."
        ),
        args_schema=EurLexInput,
        func=_run,
    )


class EurLexTool:
    """Tool for searching EUR-Lex (EU legal database)."""
    
    def __new__(cls):
        return _create_eurlex_tool()

