"""Data models for LawMode."""

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, HttpUrl


class Severity(str, Enum):
    """Risk severity levels."""

    CRITICAL = "Critical"
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"


class Risk(BaseModel):
    """A legal risk identified in code."""

    id: str = Field(default_factory=lambda: f"R{uuid4().hex[:3].upper()}")
    severity: Severity
    title: str
    law: str  # e.g., "GDPR Art. 32"
    citation: Optional[HttpUrl] = None
    description: str
    mitigation: str
    auto_fix_patch: Optional[str] = None  # Base64 encoded patch
    line_start: Optional[int] = None
    line_end: Optional[int] = None
    file_path: Optional[str] = None
    code_snippet: Optional[str] = None


class ReviewResult(BaseModel):
    """Complete legal review result."""

    review_id: UUID = Field(default_factory=uuid4)
    commit_sha: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    jurisdictions: List[str] = Field(default_factory=list)
    domain: Optional[str] = None
    risks: List[Risk] = Field(default_factory=list)
    history: List[str] = Field(default_factory=list)  # Chain execution history
    signature: Optional[str] = None  # Optional PGP signature
    metadata: Dict[str, Any] = Field(default_factory=dict)

    def has_critical_risks(self) -> bool:
        """Check if review contains critical risks."""
        return any(risk.severity == Severity.CRITICAL for risk in self.risks)

    def has_blocking_risks(self, policy: Optional[Dict[str, str]] = None) -> bool:
        """Check if review has risks that should block merge."""
        if policy is None:
            policy = {"critical": "block", "high": "require_approval"}
        
        blocking_severities = [
            severity for severity, action in policy.items()
            if action == "block"
        ]
        
        return any(
            risk.severity.value.lower() in blocking_severities
            for risk in self.risks
        )

