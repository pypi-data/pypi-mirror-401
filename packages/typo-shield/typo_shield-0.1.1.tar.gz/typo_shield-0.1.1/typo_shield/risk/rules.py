"""
Risk rules and failure policies.

Determines when the tool should exit with failure based on findings.
"""

from __future__ import annotations

from typing import Iterable, Literal

from typo_shield.risk.models import RiskFinding
from typo_shield.risk.score import aggregate_findings


def should_fail(
    findings: Iterable[RiskFinding],
    fail_on: Literal["fail", "warn"] = "fail",
) -> bool:
    """
    Determine if the tool should exit with failure.

    Policy:
    - fail_on="fail": Fail only if there are FAIL-level findings
    - fail_on="warn": Fail if there are WARN or FAIL-level findings

    Args:
        findings: Iterable of RiskFinding objects
        fail_on: Failure threshold ("fail" or "warn")

    Returns:
        True if the tool should fail, False otherwise

    Examples:
        >>> findings_with_fail = [
        ...     RiskFinding(kind="typosquat", subject="dep", name="reqeusts", target="requests",
        ...                 level="FAIL", code="TS001", message="..."),
        ... ]
        >>> should_fail(findings_with_fail, "fail")
        True
        >>> should_fail(findings_with_fail, "warn")
        True

        >>> findings_with_warn = [
        ...     RiskFinding(kind="missing_dep", subject="import", name="numpy", target=None,
        ...                 level="WARN", code="TS101", message="..."),
        ... ]
        >>> should_fail(findings_with_warn, "fail")
        False
        >>> should_fail(findings_with_warn, "warn")
        True

        >>> findings_with_info = [
        ...     RiskFinding(kind="stdlib_import", subject="import", name="os", target=None,
        ...                 level="INFO", code="TS900", message="..."),
        ... ]
        >>> should_fail(findings_with_info, "fail")
        False
        >>> should_fail(findings_with_info, "warn")
        False
    """
    counts = aggregate_findings(findings)

    if fail_on == "fail":
        # Fail only if there are FAIL-level findings
        return counts["FAIL"] > 0
    elif fail_on == "warn":
        # Fail if there are WARN or FAIL-level findings
        return counts["WARN"] > 0 or counts["FAIL"] > 0
    else:
        # Unknown policy, default to strict (fail on FAIL)
        return counts["FAIL"] > 0


def get_exit_code(
    findings: Iterable[RiskFinding],
    fail_on: Literal["fail", "warn"] = "fail",
) -> int:
    """
    Get the appropriate exit code based on findings.

    Exit codes:
    - 0: Success (no issues or only INFO findings)
    - 1: Failure (based on fail_on policy)

    Args:
        findings: Iterable of RiskFinding objects
        fail_on: Failure threshold ("fail" or "warn")

    Returns:
        Exit code (0 or 1)

    Examples:
        >>> findings_with_fail = [
        ...     RiskFinding(kind="typosquat", subject="dep", name="reqeusts", target="requests",
        ...                 level="FAIL", code="TS001", message="..."),
        ... ]
        >>> get_exit_code(findings_with_fail, "fail")
        1

        >>> findings_with_info = [
        ...     RiskFinding(kind="stdlib_import", subject="import", name="os", target=None,
        ...                 level="INFO", code="TS900", message="..."),
        ... ]
        >>> get_exit_code(findings_with_info, "fail")
        0
    """
    return 1 if should_fail(findings, fail_on) else 0


def filter_actionable_findings(
    findings: Iterable[RiskFinding],
) -> list[RiskFinding]:
    """
    Filter findings to only actionable ones (WARN and FAIL).

    INFO-level findings are informational and don't require action.

    Args:
        findings: Iterable of RiskFinding objects

    Returns:
        List of WARN and FAIL findings

    Examples:
        >>> findings = [
        ...     RiskFinding(kind="typosquat", subject="dep", name="reqeusts", target="requests",
        ...                 level="FAIL", code="TS001", message="..."),
        ...     RiskFinding(kind="missing_dep", subject="import", name="numpy", target=None,
        ...                 level="WARN", code="TS101", message="..."),
        ...     RiskFinding(kind="stdlib_import", subject="import", name="os", target=None,
        ...                 level="INFO", code="TS900", message="..."),
        ... ]
        >>> actionable = filter_actionable_findings(findings)
        >>> len(actionable)
        2
        >>> all(f.level in ["WARN", "FAIL"] for f in actionable)
        True
    """
    return [f for f in findings if f.level in ["WARN", "FAIL"]]


def validate_fail_on_value(fail_on: str) -> bool:
    """
    Validate that fail_on has a valid value.

    Args:
        fail_on: Failure threshold value to validate

    Returns:
        True if valid, False otherwise

    Examples:
        >>> validate_fail_on_value("fail")
        True
        >>> validate_fail_on_value("warn")
        True
        >>> validate_fail_on_value("invalid")
        False
    """
    return fail_on in ["fail", "warn"]


def get_result_summary(
    findings: Iterable[RiskFinding],
    fail_on: Literal["fail", "warn"] = "fail",
) -> dict[str, any]:
    """
    Get a summary of the scan result.

    Args:
        findings: Iterable of RiskFinding objects
        fail_on: Failure threshold ("fail" or "warn")

    Returns:
        Dictionary with result summary

    Examples:
        >>> findings = [
        ...     RiskFinding(kind="typosquat", subject="dep", name="reqeusts", target="requests",
        ...                 level="FAIL", code="TS001", message="..."),
        ... ]
        >>> summary = get_result_summary(findings, "fail")
        >>> summary['passed']
        False
        >>> summary['exit_code']
        1
    """
    counts = aggregate_findings(findings)
    exit_code = get_exit_code(findings, fail_on)

    return {
        "passed": exit_code == 0,
        "exit_code": exit_code,
        "fail_on": fail_on,
        "counts": counts,
        "total_findings": sum(counts.values()),
        "actionable_findings": counts["WARN"] + counts["FAIL"],
    }

