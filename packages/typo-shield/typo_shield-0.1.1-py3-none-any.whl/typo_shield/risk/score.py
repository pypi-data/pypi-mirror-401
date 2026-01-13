"""
Risk scoring and aggregation.

Aggregates risk findings and computes statistics for reporting.
"""

from __future__ import annotations

from collections import Counter
from typing import Iterable

from typo_shield.risk.models import RiskFinding


def aggregate_findings(findings: Iterable[RiskFinding]) -> dict[str, int]:
    """
    Aggregate findings by severity level.

    Counts the number of findings at each severity level (INFO, WARN, FAIL).

    Args:
        findings: Iterable of RiskFinding objects

    Returns:
        Dictionary with counts for each level: {"INFO": n, "WARN": m, "FAIL": k}

    Examples:
        >>> findings = [
        ...     RiskFinding(kind="typosquat", subject="dep", name="reqeusts", target="requests",
        ...                 level="FAIL", code="TS001", message="..."),
        ...     RiskFinding(kind="missing_dep", subject="import", name="numpy", target=None,
        ...                 level="WARN", code="TS101", message="..."),
        ...     RiskFinding(kind="stdlib_import", subject="import", name="os", target=None,
        ...                 level="INFO", code="TS900", message="..."),
        ... ]
        >>> aggregate_findings(findings)
        {'INFO': 1, 'WARN': 1, 'FAIL': 1}
    """
    # Count findings by level
    counter = Counter(finding.level for finding in findings)

    # Ensure all levels are present (even if zero)
    return {
        "INFO": counter.get("INFO", 0),
        "WARN": counter.get("WARN", 0),
        "FAIL": counter.get("FAIL", 0),
    }


def aggregate_by_kind(findings: Iterable[RiskFinding]) -> dict[str, int]:
    """
    Aggregate findings by kind.

    Counts the number of findings for each finding kind.

    Args:
        findings: Iterable of RiskFinding objects

    Returns:
        Dictionary with counts for each kind

    Examples:
        >>> findings = [
        ...     RiskFinding(kind="typosquat", subject="dep", name="reqeusts", target="requests",
        ...                 level="FAIL", code="TS001", message="..."),
        ...     RiskFinding(kind="typosquat", subject="dep", name="flsk", target="flask",
        ...                 level="FAIL", code="TS001", message="..."),
        ...     RiskFinding(kind="missing_dep", subject="import", name="numpy", target=None,
        ...                 level="WARN", code="TS101", message="..."),
        ... ]
        >>> aggregate_by_kind(findings)
        {'typosquat': 2, 'missing_dep': 1}
    """
    counter = Counter(finding.kind for finding in findings)
    return dict(counter)


def aggregate_by_code(findings: Iterable[RiskFinding]) -> dict[str, int]:
    """
    Aggregate findings by error code.

    Counts the number of findings for each error code.

    Args:
        findings: Iterable of RiskFinding objects

    Returns:
        Dictionary with counts for each code

    Examples:
        >>> findings = [
        ...     RiskFinding(kind="typosquat", subject="dep", name="reqeusts", target="requests",
        ...                 level="FAIL", code="TS001", message="..."),
        ...     RiskFinding(kind="typosquat", subject="dep", name="flsk", target="flask",
        ...                 level="FAIL", code="TS001", message="..."),
        ...     RiskFinding(kind="missing_dep", subject="import", name="numpy", target=None,
        ...                 level="WARN", code="TS101", message="..."),
        ... ]
        >>> aggregate_by_code(findings)
        {'TS001': 2, 'TS101': 1}
    """
    counter = Counter(finding.code for finding in findings)
    return dict(counter)


def get_highest_severity(findings: Iterable[RiskFinding]) -> str | None:
    """
    Get the highest severity level among findings.

    Severity order: FAIL > WARN > INFO

    Args:
        findings: Iterable of RiskFinding objects

    Returns:
        Highest severity level ("FAIL", "WARN", or "INFO"), or None if no findings

    Examples:
        >>> findings = [
        ...     RiskFinding(kind="stdlib_import", subject="import", name="os", target=None,
        ...                 level="INFO", code="TS900", message="..."),
        ...     RiskFinding(kind="missing_dep", subject="import", name="numpy", target=None,
        ...                 level="WARN", code="TS101", message="..."),
        ... ]
        >>> get_highest_severity(findings)
        'WARN'
    """
    findings_list = list(findings)

    if not findings_list:
        return None

    # Check in order of severity
    if any(f.level == "FAIL" for f in findings_list):
        return "FAIL"
    if any(f.level == "WARN" for f in findings_list):
        return "WARN"
    if any(f.level == "INFO" for f in findings_list):
        return "INFO"

    return None


def filter_by_level(
    findings: Iterable[RiskFinding],
    level: str,
) -> list[RiskFinding]:
    """
    Filter findings by severity level.

    Args:
        findings: Iterable of RiskFinding objects
        level: Severity level to filter by ("INFO", "WARN", or "FAIL")

    Returns:
        List of findings matching the specified level

    Examples:
        >>> findings = [
        ...     RiskFinding(kind="typosquat", subject="dep", name="reqeusts", target="requests",
        ...                 level="FAIL", code="TS001", message="..."),
        ...     RiskFinding(kind="missing_dep", subject="import", name="numpy", target=None,
        ...                 level="WARN", code="TS101", message="..."),
        ... ]
        >>> fail_findings = filter_by_level(findings, "FAIL")
        >>> len(fail_findings)
        1
        >>> fail_findings[0].name
        'reqeusts'
    """
    return [f for f in findings if f.level == level]


def filter_by_kind(
    findings: Iterable[RiskFinding],
    kind: str,
) -> list[RiskFinding]:
    """
    Filter findings by kind.

    Args:
        findings: Iterable of RiskFinding objects
        kind: Finding kind to filter by

    Returns:
        List of findings matching the specified kind

    Examples:
        >>> findings = [
        ...     RiskFinding(kind="typosquat", subject="dep", name="reqeusts", target="requests",
        ...                 level="FAIL", code="TS001", message="..."),
        ...     RiskFinding(kind="missing_dep", subject="import", name="numpy", target=None,
        ...                 level="WARN", code="TS101", message="..."),
        ... ]
        >>> typosquat_findings = filter_by_kind(findings, "typosquat")
        >>> len(typosquat_findings)
        1
    """
    return [f for f in findings if f.kind == kind]


def compute_stats(findings: Iterable[RiskFinding]) -> dict[str, any]:
    """
    Compute comprehensive statistics for findings.

    Args:
        findings: Iterable of RiskFinding objects

    Returns:
        Dictionary with various statistics

    Examples:
        >>> findings = [
        ...     RiskFinding(kind="typosquat", subject="dep", name="reqeusts", target="requests",
        ...                 level="FAIL", code="TS001", message="..."),
        ...     RiskFinding(kind="missing_dep", subject="import", name="numpy", target=None,
        ...                 level="WARN", code="TS101", message="..."),
        ... ]
        >>> stats = compute_stats(findings)
        >>> stats['total']
        2
        >>> stats['by_level']['FAIL']
        1
    """
    findings_list = list(findings)

    return {
        "total": len(findings_list),
        "by_level": aggregate_findings(findings_list),
        "by_kind": aggregate_by_kind(findings_list),
        "by_code": aggregate_by_code(findings_list),
        "highest_severity": get_highest_severity(findings_list),
    }

