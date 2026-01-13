"""
JSON report rendering.

Generates machine-readable JSON reports for CI/CD integration.
"""

from __future__ import annotations

import json
from typing import Any, Iterable

from typo_shield.risk.models import RiskFinding
from typo_shield.risk.score import aggregate_findings

# JSON schema version
SCHEMA_VERSION = "1.0"


def render_json_report(
    findings: Iterable[RiskFinding],
    indent: int | None = 2,
) -> str:
    """
    Render findings as a JSON report.

    Args:
        findings: Iterable of RiskFinding objects
        indent: JSON indentation level (None for compact, 2 for readable)

    Returns:
        JSON string

    Example:
        >>> findings = [
        ...     RiskFinding(kind="typosquat", subject="dep", name="reqeusts",
        ...                 target="requests", level="FAIL", code="TS001",
        ...                 message="Suspected typosquat", file="requirements.txt", lineno=1),
        ... ]
        >>> report = render_json_report(findings)
        >>> "reqeusts" in report
        True
    """
    findings_list = list(findings)
    counts = aggregate_findings(findings_list)

    report_data = {
        "version": SCHEMA_VERSION,
        "summary": {
            "fail": counts["FAIL"],
            "warn": counts["WARN"],
            "info": counts["INFO"],
            "total": sum(counts.values()),
        },
        "findings": [_finding_to_dict(f) for f in findings_list],
    }

    return json.dumps(report_data, indent=indent)


def render_json_summary(
    findings: Iterable[RiskFinding],
    fail_on: str = "fail",
    indent: int | None = 2,
) -> str:
    """
    Render a summary-only JSON report with result status.

    Args:
        findings: Iterable of RiskFinding objects
        fail_on: Failure threshold ("fail" or "warn")
        indent: JSON indentation level (None for compact, 2 for readable)

    Returns:
        JSON string with summary and result

    Example:
        >>> findings = []
        >>> summary = render_json_summary(findings)
        >>> "passed" in summary
        True
    """
    from typo_shield.risk.rules import get_exit_code

    findings_list = list(findings)
    counts = aggregate_findings(findings_list)
    exit_code = get_exit_code(findings_list, fail_on)

    summary_data = {
        "version": SCHEMA_VERSION,
        "result": {
            "passed": exit_code == 0,
            "exit_code": exit_code,
            "fail_on": fail_on,
        },
        "summary": {
            "fail": counts["FAIL"],
            "warn": counts["WARN"],
            "info": counts["INFO"],
            "total": sum(counts.values()),
            "actionable": counts["FAIL"] + counts["WARN"],
        },
    }

    return json.dumps(summary_data, indent=indent)


def _finding_to_dict(finding: RiskFinding) -> dict[str, Any]:
    """
    Convert a RiskFinding to a dictionary for JSON serialization.

    Args:
        finding: RiskFinding object

    Returns:
        Dictionary representation
    """
    return {
        "level": finding.level,
        "code": finding.code,
        "kind": finding.kind,
        "subject": finding.subject,
        "name": finding.name,
        "target": finding.target,
        "message": finding.message,
        "file": finding.file,
        "lineno": finding.lineno,
        "context": finding.context,
    }


def parse_json_report(json_str: str) -> dict[str, Any]:
    """
    Parse a JSON report back to a dictionary.

    Useful for testing and processing reports.

    Args:
        json_str: JSON report string

    Returns:
        Parsed dictionary

    Example:
        >>> findings = []
        >>> report = render_json_report(findings)
        >>> parsed = parse_json_report(report)
        >>> parsed["version"]
        '1.0'
    """
    return json.loads(json_str)


def validate_json_report(json_str: str) -> tuple[bool, str | None]:
    """
    Validate that a string is a valid JSON report.

    Args:
        json_str: String to validate

    Returns:
        Tuple of (is_valid, error_message)

    Example:
        >>> report = render_json_report([])
        >>> is_valid, error = validate_json_report(report)
        >>> is_valid
        True
        >>> error is None
        True
    """
    try:
        data = json.loads(json_str)
    except json.JSONDecodeError as e:
        return False, f"Invalid JSON: {e}"

    # Check required fields
    if not isinstance(data, dict):
        return False, "Report must be a JSON object"

    if "version" not in data:
        return False, "Missing 'version' field"

    if "summary" not in data:
        return False, "Missing 'summary' field"

    if not isinstance(data["summary"], dict):
        return False, "'summary' must be an object"

    required_summary_fields = ["fail", "warn", "info", "total"]
    for field in required_summary_fields:
        if field not in data["summary"]:
            return False, f"Missing 'summary.{field}' field"

    if "findings" not in data:
        return False, "Missing 'findings' field"

    if not isinstance(data["findings"], list):
        return False, "'findings' must be an array"

    return True, None

