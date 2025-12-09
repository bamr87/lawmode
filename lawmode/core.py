"""Core LawMode agent orchestrator."""

import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional
from uuid import uuid4

from lawmode.chains import build_lawmode_chains
from lawmode.config import LawModeConfig
from lawmode.llm import create_llm_backend
from lawmode.models import ReviewResult, Risk, Severity


class LawModeAgent:
    """Main LawMode agent that orchestrates legal review."""

    def __init__(self, config: Optional[LawModeConfig] = None):
        """Initialize LawMode agent."""
        self.config = config or LawModeConfig.from_file()
        self.llm_backend = create_llm_backend(self.config.llm)
        self.chains = build_lawmode_chains(self.llm_backend)
        
        # Ensure artifact directories exist
        self.config.artifact_dir.mkdir(parents=True, exist_ok=True)
        self.config.history_dir.mkdir(parents=True, exist_ok=True)
        self.config.reviews_dir.mkdir(parents=True, exist_ok=True)

    def review_code(
        self,
        code: str,
        file_path: Optional[str] = None,
        commit_sha: Optional[str] = None,
    ) -> ReviewResult:
        """Review code and return legal analysis."""
        
        # Prepare initial state
        initial_state = {
            "code": code,
            "file_path": file_path,
            "commit_sha": commit_sha,
            "timestamp": datetime.utcnow().isoformat(),
        }
        
        # Execute chains
        try:
            final_state = self.chains.invoke(initial_state)
        except Exception as e:
            # If chain execution fails, return minimal result
            return ReviewResult(
                commit_sha=commit_sha,
                risks=[
                    Risk(
                        severity=Severity.HIGH,
                        title="Chain execution error",
                        law="Internal Error",
                        description=f"Failed to execute legal review chains: {str(e)}",
                        mitigation="Check LLM configuration and API keys",
                    )
                ],
            )
        
        # Parse chain outputs and extract risks
        risks = self._extract_risks(final_state, file_path)
        
        # Extract jurisdictions and domain
        jurisdictions = self._extract_jurisdictions(final_state)
        domain = self._extract_domain(final_state)
        
        # Create review result
        review = ReviewResult(
            commit_sha=commit_sha,
            jurisdictions=jurisdictions,
            domain=domain,
            risks=risks,
            history=[f"chain_{i}.json" for i in range(1, 9)],
            metadata={"file_path": file_path, "state": final_state},
        )
        
        # Save chain history
        self._save_chain_history(review.review_id, final_state)
        
        return review

    def _extract_risks(self, state: Dict[str, Any], file_path: Optional[str]) -> List[Risk]:
        """Extract risks from chain state."""
        risks = []
        
        # Handle None state
        if state is None:
            return risks
        
        # Parse each chain's output
        risk_sources = [
            ("privacy_risks", "Privacy Compliance"),
            ("license_risks", "License Compliance"),
            ("security_risks", "Security Compliance"),
            ("accessibility_risks", "Accessibility Compliance"),
            ("copyright_risks", "Copyright & IP"),
            ("regulatory_risks", "Regulatory Compliance"),
        ]
        
        for key, category in risk_sources:
            if state and key in state:
                parsed = self._parse_risk_output(state[key], category, file_path)
                risks.extend(parsed)
        
        return risks

    def _parse_risk_output(
        self, output: str, category: str, file_path: Optional[str]
    ) -> List[Risk]:
        """Parse LLM output into structured Risk objects."""
        risks = []
        
        # Try to extract JSON from output
        json_match = re.search(r'\{[^{}]*"risks"[^{}]*\}', output, re.DOTALL)
        if json_match:
            try:
                data = json.loads(json_match.group())
                if "risks" in data:
                    for risk_data in data["risks"]:
                        risk = Risk(
                            severity=Severity(risk_data.get("severity", "Medium")),
                            title=risk_data.get("title", "Unknown Risk"),
                            law=risk_data.get("law", "Unknown Law"),
                            citation=risk_data.get("citation"),
                            description=risk_data.get("description", ""),
                            mitigation=risk_data.get("mitigation", ""),
                            file_path=file_path,
                            line_start=risk_data.get("line_start"),
                            line_end=risk_data.get("line_end"),
                        )
                        risks.append(risk)
            except (json.JSONDecodeError, ValueError):
                pass
        
        # Fallback: parse text output
        if not risks:
            # Look for severity indicators
            severity_patterns = {
                Severity.CRITICAL: r"(?i)(critical|severe|blocking)",
                Severity.HIGH: r"(?i)(high|important|significant)",
                Severity.MEDIUM: r"(?i)(medium|moderate)",
                Severity.LOW: r"(?i)(low|minor|informational)",
            }
            
            # Simple heuristic: if output mentions risks, create one
            if any(word in output.lower() for word in ["risk", "violation", "issue", "problem"]):
                severity = Severity.MEDIUM
                for sev, pattern in severity_patterns.items():
                    if re.search(pattern, output):
                        severity = sev
                        break
                
                risk = Risk(
                    severity=severity,
                    title=f"{category} Issue",
                    law="Analysis Required",
                    description=output[:500],  # Truncate long outputs
                    mitigation="Review code and consult legal counsel",
                    file_path=file_path,
                )
                risks.append(risk)
        
        return risks

    def _extract_jurisdictions(self, state: Dict[str, Any]) -> List[str]:
        """Extract jurisdictions from state."""
        jurisdictions = []
        
        if state and "jurisdiction_analysis" in state:
            analysis = state["jurisdiction_analysis"]
            # Try to parse JSON
            json_match = re.search(r'\{[^{}]*"jurisdictions"[^{}]*\}', analysis)
            if json_match:
                try:
                    data = json.loads(json_match.group())
                    jurisdictions = data.get("jurisdictions", [])
                except json.JSONDecodeError:
                    pass
        
        # Fallback: use config defaults
        if not jurisdictions:
            jurisdictions = self.config.policy.jurisdictions
        
        return jurisdictions

    def _extract_domain(self, state: Dict[str, Any]) -> Optional[str]:
        """Extract domain from state."""
        if state and "domain_analysis" in state:
            analysis = state["domain_analysis"]
            json_match = re.search(r'\{[^{}]*"domain"[^{}]*\}', analysis)
            if json_match:
                try:
                    data = json.loads(json_match.group())
                    return data.get("domain")
                except json.JSONDecodeError:
                    pass
        
        return None

    def _save_chain_history(self, review_id: str, state: Dict[str, Any]) -> None:
        """Save chain execution history."""
        history_file = self.config.history_dir / f"{review_id}_history.json"
        with open(history_file, "w") as f:
            json.dump(state, f, indent=2, default=str)

    def generate_artifacts(self, review: ReviewResult) -> Dict[str, Path]:
        """Generate legal review artifacts."""
        artifacts = {}
        
        # Generate review.json
        review_json = self.config.artifact_dir / "review.json"
        with open(review_json, "w") as f:
            json.dump(review.model_dump(mode="json"), f, indent=2, default=str)
        artifacts["review.json"] = review_json
        
        # Generate risks.yaml
        risks_yaml = self.config.artifact_dir / "risks.yaml"
        risks_data = {
            "review_id": str(review.review_id),
            "timestamp": review.timestamp.isoformat(),
            "risks": [
                {
                    "id": risk.id,
                    "severity": risk.severity.value,
                    "title": risk.title,
                    "law": risk.law,
                    "citation": str(risk.citation) if risk.citation else None,
                    "description": risk.description,
                    "mitigation": risk.mitigation,
                    "file_path": risk.file_path,
                    "line_start": risk.line_start,
                    "line_end": risk.line_end,
                }
                for risk in review.risks
            ],
        }
        import yaml
        with open(risks_yaml, "w") as f:
            yaml.dump(risks_data, f, default_flow_style=False)
        artifacts["risks.yaml"] = risks_yaml
        
        # Generate mitigations.md
        mitigations_md = self.config.artifact_dir / "mitigations.md"
        with open(mitigations_md, "w") as f:
            f.write("# Legal Risk Mitigations\n\n")
            f.write(f"**Review ID:** {review.review_id}\n")
            f.write(f"**Timestamp:** {review.timestamp.isoformat()}\n\n")
            
            if review.risks:
                for risk in review.risks:
                    f.write(f"## {risk.id}: {risk.title}\n\n")
                    f.write(f"**Severity:** {risk.severity.value}\n\n")
                    f.write(f"**Law:** {risk.law}\n\n")
                    if risk.citation:
                        f.write(f"**Citation:** {risk.citation}\n\n")
                    f.write(f"**Description:** {risk.description}\n\n")
                    f.write(f"**Mitigation:** {risk.mitigation}\n\n")
                    if risk.file_path:
                        f.write(f"**File:** {risk.file_path}\n")
                        if risk.line_start:
                            f.write(f"**Lines:** {risk.line_start}-{risk.line_end or risk.line_start}\n")
                    f.write("\n---\n\n")
            else:
                f.write("No risks identified.\n")
        
        artifacts["mitigations.md"] = mitigations_md
        
        # Copy DISCLAIMER.md if it doesn't exist
        disclaimer = self.config.artifact_dir / "DISCLAIMER.md"
        if not disclaimer.exists():
            source_disclaimer = Path(__file__).parent.parent / "DISCLAIMER.md"
            if source_disclaimer.exists():
                import shutil
                shutil.copy(source_disclaimer, disclaimer)
                artifacts["DISCLAIMER.md"] = disclaimer
        
        return artifacts

