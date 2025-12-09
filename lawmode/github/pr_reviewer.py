"""GitHub PR review and commenting functionality."""

import json
from typing import Dict, List, Optional

from lawmode.core import LawModeAgent
from lawmode.models import ReviewResult, Severity


class PRReviewer:
    """Review GitHub PRs and post comments."""

    def __init__(self, agent: LawModeAgent):
        """Initialize PR reviewer."""
        self.agent = agent

    def review_pr(
        self,
        diff_content: str,
        pr_number: int,
        commit_sha: str,
    ) -> Dict[str, any]:
        """Review a PR and return comment data."""
        # Run legal review
        review = self.agent.review_code(diff_content, commit_sha=commit_sha)
        
        # Generate artifacts
        artifacts = self.agent.generate_artifacts(review)
        
        # Create PR comment
        comment = self._create_pr_comment(review)
        
        # Determine if PR should be blocked
        should_block = review.has_blocking_risks(self.agent.config.policy.severity_gating)
        
        return {
            "comment": comment,
            "should_block": should_block,
            "review": review,
            "artifacts": artifacts,
        }

    def _create_pr_comment(self, review: ReviewResult) -> str:
        """Create a formatted PR comment."""
        lines = [
            "## 🔍 LawMode.ai Legal Review",
            "",
            f"**Review ID:** `{review.review_id}`",
            f"**Jurisdictions:** {', '.join(review.jurisdictions) if review.jurisdictions else 'Auto-detected'}",
            f"**Domain:** {review.domain or 'Not detected'}",
            "",
        ]
        
        if review.risks:
            # Risk summary table
            lines.append("### Risk Summary")
            lines.append("")
            lines.append("| Severity | Count |")
            lines.append("|----------|-------|")
            
            severity_counts = {
                Severity.CRITICAL: sum(1 for r in review.risks if r.severity == Severity.CRITICAL),
                Severity.HIGH: sum(1 for r in review.risks if r.severity == Severity.HIGH),
                Severity.MEDIUM: sum(1 for r in review.risks if r.severity == Severity.MEDIUM),
                Severity.LOW: sum(1 for r in review.risks if r.severity == Severity.LOW),
            }
            
            for severity, count in severity_counts.items():
                if count > 0:
                    emoji = "🔴" if severity == Severity.CRITICAL else "🟡" if severity == Severity.HIGH else "🔵"
                    lines.append(f"| {emoji} {severity.value} | {count} |")
            
            lines.append("")
            lines.append("### Identified Risks")
            lines.append("")
            
            for risk in review.risks:
                severity_emoji = {
                    Severity.CRITICAL: "🔴",
                    Severity.HIGH: "🟡",
                    Severity.MEDIUM: "🔵",
                    Severity.LOW: "🟢",
                }.get(risk.severity, "⚪")
                
                lines.append(f"#### {severity_emoji} {risk.id}: {risk.title}")
                lines.append("")
                lines.append(f"- **Severity:** {risk.severity.value}")
                lines.append(f"- **Law:** {risk.law}")
                if risk.citation:
                    lines.append(f"- **Citation:** {risk.citation}")
                if risk.file_path:
                    lines.append(f"- **File:** `{risk.file_path}`")
                    if risk.line_start:
                        lines.append(f"- **Lines:** {risk.line_start}-{risk.line_end or risk.line_start}")
                lines.append(f"- **Description:** {risk.description}")
                lines.append(f"- **Mitigation:** {risk.mitigation}")
                lines.append("")
        else:
            lines.append("✅ No legal risks identified.")
            lines.append("")
        
        # Artifacts
        lines.append("### Artifacts")
        lines.append("")
        lines.append("Legal review artifacts have been generated:")
        lines.append("- `lawmode/review.json` - Complete review data")
        lines.append("- `lawmode/risks.yaml` - Risk summary")
        lines.append("- `lawmode/mitigations.md` - Detailed mitigations")
        lines.append("")
        
        # Blocking status
        if review.has_blocking_risks(self.agent.config.policy.severity_gating):
            lines.append("---")
            lines.append("")
            lines.append("⚠️ **This PR contains blocking legal risks and cannot be merged.**")
            lines.append("")
            lines.append("Please address the critical/high risks before merging, or contact your legal team.")
        
        # Disclaimer
        lines.append("---")
        lines.append("")
        lines.append("⚠️ **NOT LEGAL ADVICE**: This is automated analysis for informational purposes only.")
        
        return "\n".join(lines)

    def create_status_check(self, review: ReviewResult) -> Dict[str, any]:
        """Create GitHub status check data."""
        state = "failure" if review.has_blocking_risks(self.agent.config.policy.severity_gating) else "success"
        
        description = f"Found {len(review.risks)} legal risk(s)"
        if review.has_critical_risks():
            description = f"Found {sum(1 for r in review.risks if r.severity == Severity.CRITICAL)} critical risk(s)"
        
        return {
            "state": state,
            "description": description,
            "context": "lawmode/legal-review",
            "target_url": f"https://github.com/.../lawmode/review.json",  # Would be actual URL
        }

