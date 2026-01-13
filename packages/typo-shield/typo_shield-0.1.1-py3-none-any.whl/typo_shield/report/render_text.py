"""
Text report rendering.

Generates human-readable terminal reports with colors and formatting.
"""

from __future__ import annotations

from typing import Iterable

from typo_shield.risk.models import RiskFinding
from typo_shield.risk.score import aggregate_findings, filter_by_level


def render_text_report(
    findings: Iterable[RiskFinding],
    show_info: bool = True,
    use_colors: bool = True,
) -> str:
    """
    Render findings as a formatted text report.

    Args:
        findings: Iterable of RiskFinding objects
        show_info: Whether to show INFO-level findings (default: True)
        use_colors: Whether to use ANSI colors (default: True)

    Returns:
        Formatted text report

    Example:
        >>> findings = [
        ...     RiskFinding(kind="typosquat", subject="dep", name="reqeusts",
        ...                 target="requests", level="FAIL", code="TS001",
        ...                 message="Suspected typosquat", file="requirements.txt", lineno=1),
        ... ]
        >>> report = render_text_report(findings, use_colors=False)
        >>> "FAIL" in report
        True
    """
    findings_list = list(findings)
    counts = aggregate_findings(findings_list)

    lines = []

    # Header
    lines.append(_render_header(use_colors))
    lines.append("")

    # Summary
    lines.append(_render_summary(counts, use_colors))
    lines.append("")

    # Failures
    fail_findings = filter_by_level(findings_list, "FAIL")
    if fail_findings:
        lines.append(_render_section_header("FAILURES", len(fail_findings), "❌", use_colors, "red"))
        lines.append(_render_separator())
        for finding in fail_findings:
            lines.append(_render_finding(finding, use_colors))
            lines.append("")

    # Warnings
    warn_findings = filter_by_level(findings_list, "WARN")
    if warn_findings:
        lines.append(_render_section_header("WARNINGS", len(warn_findings), "⚠️ ", use_colors, "yellow"))
        lines.append(_render_separator())
        for finding in warn_findings:
            lines.append(_render_finding(finding, use_colors))
            lines.append("")

    # Info (optional)
    if show_info:
        info_findings = filter_by_level(findings_list, "INFO")
        if info_findings:
            lines.append(_render_section_header("INFO", len(info_findings), "ℹ️ ", use_colors, "blue"))
            lines.append(_render_separator())
            lines.append(_render_info_summary(info_findings, use_colors))
            lines.append("")

    # Footer separator
    lines.append(_render_separator())

    return "\n".join(lines)


def render_result_line(
    findings: Iterable[RiskFinding],
    fail_on: str = "fail",
    use_colors: bool = True,
) -> str:
    """
    Render a single-line result summary.

    Args:
        findings: Iterable of RiskFinding objects
        fail_on: Failure threshold ("fail" or "warn")
        use_colors: Whether to use ANSI colors

    Returns:
        Single-line result string

    Example:
        >>> findings = []
        >>> result = render_result_line(findings, use_colors=False)
        >>> "PASSED" in result
        True
    """
    from typo_shield.risk.rules import get_exit_code

    counts = aggregate_findings(findings)
    exit_code = get_exit_code(findings, fail_on)

    if exit_code == 0:
        status = _colorize("✓ PASSED", "green", use_colors)
        result = f"Result: {status} (exit code 0)"
    else:
        status = _colorize("✗ FAILED", "red", use_colors)
        result = f"Result: {status} (exit code 1)"

    # Add counts summary
    parts = []
    if counts["FAIL"] > 0:
        parts.append(_colorize(f"{counts['FAIL']} FAIL", "red", use_colors))
    if counts["WARN"] > 0:
        parts.append(_colorize(f"{counts['WARN']} WARN", "yellow", use_colors))
    if counts["INFO"] > 0:
        parts.append(_colorize(f"{counts['INFO']} INFO", "blue", use_colors))

    if parts:
        result += f" — {', '.join(parts)}"

    return result


def _render_header(use_colors: bool) -> str:
    """Render report header."""
    title = "typo-shield Security Report"
    border = "═" * 56

    if use_colors:
        title = _colorize(title, "cyan", True, bold=True)

    return f"╔{border}╗\n║{title.center(66)}║\n╚{border}╝"


def _render_summary(counts: dict[str, int], use_colors: bool) -> str:
    """Render summary line."""
    parts = []

    if counts["FAIL"] > 0:
        parts.append(_colorize(f"{counts['FAIL']} FAIL", "red", use_colors, bold=True))
    else:
        parts.append(f"{counts['FAIL']} FAIL")

    if counts["WARN"] > 0:
        parts.append(_colorize(f"{counts['WARN']} WARN", "yellow", use_colors, bold=True))
    else:
        parts.append(f"{counts['WARN']} WARN")

    if counts["INFO"] > 0:
        parts.append(_colorize(f"{counts['INFO']} INFO", "blue", use_colors))
    else:
        parts.append(f"{counts['INFO']} INFO")

    return f"Summary: {', '.join(parts)}"


def _render_section_header(
    title: str,
    count: int,
    icon: str,
    use_colors: bool,
    color: str,
) -> str:
    """Render section header."""
    header = f"{icon} {title} ({count})"

    if use_colors:
        header = _colorize(header, color, True, bold=True)

    return header


def _render_separator() -> str:
    """Render separator line."""
    return "─" * 56


def _render_finding(finding: RiskFinding, use_colors: bool) -> str:
    """Render a single finding with details."""
    lines = []

    # Code and message
    code = f"[{finding.code}]"
    if use_colors:
        if finding.level == "FAIL":
            code = _colorize(code, "red", True, bold=True)
        elif finding.level == "WARN":
            code = _colorize(code, "yellow", True, bold=True)

    lines.append(f"{code} {finding.message}")

    # File location
    if finding.file:
        location = f"  File: {finding.file}"
        if finding.lineno:
            location += f":{finding.lineno}"
        lines.append(location)

    # Additional details based on kind
    if finding.kind == "typosquat" and finding.target:
        lines.append(f"  Package: {finding.name}")
        lines.append(f"  Similar to: {finding.target}")
        lines.append(f"  💡 Suggestion: Did you mean \"{finding.target}\"?")
    elif finding.kind == "missing_dep":
        lines.append(f"  Module: {finding.name}")
        if finding.target:
            lines.append(f"  Expected package: {finding.target}")
        lines.append(f"  💡 Suggestion: Add \"{finding.target or finding.name}\" to your dependencies")
    elif finding.kind == "suspicious_chars" or finding.kind == "suspicious_pattern":
        lines.append(f"  Package: {finding.name}")
        lines.append("  💡 Suggestion: Verify this is the correct package name")

    return "\n".join(lines)


def _render_info_summary(findings: list[RiskFinding], use_colors: bool) -> str:
    """Render INFO findings as a compact summary."""
    # Group by kind
    by_kind: dict[str, list[str]] = {}

    for finding in findings:
        if finding.kind not in by_kind:
            by_kind[finding.kind] = []
        by_kind[finding.kind].append(finding.name)

    lines = []

    # Stdlib imports
    if "stdlib_import" in by_kind:
        modules = ", ".join(sorted(set(by_kind["stdlib_import"]))[:5])
        count = len(by_kind["stdlib_import"])
        if count > 5:
            modules += f", ... (+{count - 5} more)"
        lines.append(f"  ✓ Standard library imports: {modules}")

    # Local imports
    if "local_import" in by_kind:
        modules = ", ".join(sorted(set(by_kind["local_import"]))[:5])
        count = len(by_kind["local_import"])
        if count > 5:
            modules += f", ... (+{count - 5} more)"
        lines.append(f"  ✓ Local project modules: {modules}")

    # Relative imports
    if "relative_import" in by_kind:
        count = len(by_kind["relative_import"])
        lines.append(f"  ✓ Relative imports: {count}")

    # New dependencies
    if "new_dep" in by_kind:
        count = len(by_kind["new_dep"])
        lines.append(f"  ✓ New dependencies added: {count}")

    if not lines:
        lines.append("  ✓ No informational findings")

    return "\n".join(lines)


def _colorize(
    text: str,
    color: str,
    use_colors: bool,
    bold: bool = False,
) -> str:
    """Apply ANSI color codes to text."""
    if not use_colors:
        return text

    colors = {
        "red": "\033[91m",
        "green": "\033[92m",
        "yellow": "\033[93m",
        "blue": "\033[94m",
        "cyan": "\033[96m",
    }

    bold_code = "\033[1m" if bold else ""
    reset = "\033[0m"
    color_code = colors.get(color, "")

    return f"{bold_code}{color_code}{text}{reset}"

