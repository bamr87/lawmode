"""Tests for LawMode models."""

import pytest
from lawmode.models import Risk, ReviewResult, Severity


def test_risk_creation():
    """Test Risk model creation."""
    risk = Risk(
        severity=Severity.CRITICAL,
        title="Test Risk",
        law="Test Law",
        description="Test description",
        mitigation="Test mitigation",
    )
    
    assert risk.severity == Severity.CRITICAL
    assert risk.title == "Test Risk"
    assert risk.id.startswith("R")


def test_review_result():
    """Test ReviewResult model creation."""
    review = ReviewResult(
        jurisdictions=["US", "EU"],
        domain="fintech",
    )
    
    assert len(review.jurisdictions) == 2
    assert review.domain == "fintech"
    assert not review.has_critical_risks()


def test_review_result_with_risks():
    """Test ReviewResult with risks."""
    risk = Risk(
        severity=Severity.CRITICAL,
        title="Critical Risk",
        law="Test Law",
        description="Test",
        mitigation="Fix it",
    )
    
    review = ReviewResult(risks=[risk])
    
    assert review.has_critical_risks()
    assert review.has_blocking_risks({"critical": "block"})


def test_review_result_blocking():
    """Test blocking risk detection."""
    risk = Risk(
        severity=Severity.HIGH,
        title="High Risk",
        law="Test Law",
        description="Test",
        mitigation="Fix it",
    )
    
    review = ReviewResult(risks=[risk])
    
    # Should not block if policy doesn't require it
    assert not review.has_blocking_risks({"critical": "block"})
    
    # Should block if policy requires it
    assert review.has_blocking_risks({"high": "block"})

