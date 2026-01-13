"""Risk analysis and typosquat detection."""

from __future__ import annotations

from typo_shield.risk.models import RiskFinding
from typo_shield.risk.rules import get_exit_code, should_fail
from typo_shield.risk.score import aggregate_findings, compute_stats

__all__ = [
    "RiskFinding",
    "aggregate_findings",
    "compute_stats",
    "should_fail",
    "get_exit_code",
]

