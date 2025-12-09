"""Tests for legal research tools."""

import pytest
from lawmode.tools import EurLexTool, SPDXLicenseTool


def test_eurlex_tool():
    """Test EUR-Lex tool."""
    tool = EurLexTool()
    result = tool._run("GDPR Art. 32")
    
    assert "GDPR" in result or "EUR-Lex" in result
    assert isinstance(result, str)


def test_spdx_tool():
    """Test SPDX license tool."""
    tool = SPDXLicenseTool()
    
    # Test GPL detection
    result = tool._run("GPL-3.0")
    assert "GPL" in result or "viral" in result or "copyleft" in result
    
    # Test permissive license
    result = tool._run("MIT")
    assert "MIT" in result or "permissive" in result

