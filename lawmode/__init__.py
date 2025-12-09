"""LawMode.ai - Always-on AI lawyer for developers."""

__version__ = "0.1.0"
__author__ = "LawMode.ai"

from lawmode.core import LawModeAgent
from lawmode.models import ReviewResult, Risk, Severity

__all__ = ["LawModeAgent", "ReviewResult", "Risk", "Severity"]

