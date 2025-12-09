"""Tests for configuration management."""

import os
import tempfile
from pathlib import Path

import pytest
from lawmode.config import LawModeConfig, LLMConfig, PolicyConfig


def test_default_config():
    """Test default configuration."""
    config = LawModeConfig()
    
    assert config.llm.provider == "openai"
    assert len(config.policy.jurisdictions) > 0


def test_config_from_file(tmp_path):
    """Test loading configuration from file."""
    config_file = tmp_path / "policy.yaml"
    config_file.write_text("""
policy:
  jurisdictions:
    - US-CA
    - EU
  severity_gating:
    critical: block
    high: comment
""")
    
    config = LawModeConfig.from_file(config_file)
    
    assert "US-CA" in config.policy.jurisdictions
    assert config.policy.severity_gating["critical"] == "block"


def test_config_env_override():
    """Test environment variable overrides."""
    os.environ["LAWMODE_LLM_PROVIDER"] = "grok"
    os.environ["LAWMODE_LLM_MODEL"] = "grok-2-1212"
    
    config = LawModeConfig.from_file()
    
    assert config.llm.provider == "grok"
    assert config.llm.model == "grok-2-1212"
    
    # Cleanup
    del os.environ["LAWMODE_LLM_PROVIDER"]
    del os.environ["LAWMODE_LLM_MODEL"]

