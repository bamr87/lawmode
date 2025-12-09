"""Configuration management for LawMode."""

import os
from pathlib import Path
from typing import Dict, List, Optional

import yaml
from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv()


class LLMConfig(BaseModel):
    """LLM backend configuration."""

    provider: str = Field(default="openai")  # openai, grok
    model: str = Field(default="gpt-4o")
    api_key: Optional[str] = None
    temperature: float = Field(default=0.1, ge=0.0, le=1.0)
    max_tokens: int = Field(default=4000)


class PolicyConfig(BaseModel):
    """Policy configuration for risk gating."""

    jurisdictions: List[str] = Field(default_factory=lambda: ["US", "EU"])
    severity_gating: Dict[str, str] = Field(
        default_factory=lambda: {
            "critical": "block",
            "high": "require_approval",
            "medium": "comment",
            "low": "comment",
        }
    )
    domains: List[str] = Field(default_factory=list)
    auto_fix_enabled: bool = False


class LawModeConfig(BaseModel):
    """Main LawMode configuration."""

    llm: LLMConfig = Field(default_factory=LLMConfig)
    policy: PolicyConfig = Field(default_factory=PolicyConfig)
    artifact_dir: Path = Field(default=Path(".lawmode"))
    history_dir: Path = Field(default=Path(".lawmode/history"))
    reviews_dir: Path = Field(default=Path(".lawmode/reviews"))
    timeout_seconds: int = 30

    @classmethod
    def from_file(cls, path: Optional[Path] = None) -> "LawModeConfig":
        """Load configuration from YAML file."""
        if path is None:
            path = Path(".lawmode/policy.yaml")
        
        config = cls()
        
        if path.exists():
            with open(path, "r") as f:
                data = yaml.safe_load(f) or {}
            
            if "policy" in data:
                config.policy = PolicyConfig(**data["policy"])
            
            if "llm" in data:
                config.llm = LLMConfig(**data["llm"])
        
        # Override with environment variables
        if os.getenv("LAWMODE_LLM_PROVIDER"):
            config.llm.provider = os.getenv("LAWMODE_LLM_PROVIDER")
        if os.getenv("LAWMODE_LLM_MODEL"):
            config.llm.model = os.getenv("LAWMODE_LLM_MODEL")
        if os.getenv("LAWMODE_LLM_API_KEY"):
            config.llm.api_key = os.getenv("LAWMODE_LLM_API_KEY")
        
        # Special handling for Grok - check XAI_API_KEY if provider is grok
        if config.llm.provider.lower() == "grok" and not config.llm.api_key:
            config.llm.api_key = os.getenv("XAI_API_KEY") or os.getenv("GROK_API_KEY")
        
        return config

    def save(self, path: Optional[Path] = None) -> None:
        """Save configuration to YAML file."""
        if path is None:
            path = Path(".lawmode/policy.yaml")
        
        path.parent.mkdir(parents=True, exist_ok=True)
        
        data = {
            "policy": self.policy.model_dump(),
            "llm": self.llm.model_dump(exclude={"api_key"}),
        }
        
        with open(path, "w") as f:
            yaml.dump(data, f, default_flow_style=False)

