"""Tests for text report rendering."""

from __future__ import annotations

from typo_shield.report.render_text import (
    render_result_line,
    render_text_report,
)
from typo_shield.risk.models import RiskFinding


class TestRenderTextReport:
    """Tests for render_text_report()."""

    def test_render_with_failures(self) -> None:
        """Test rendering report with FAIL findings."""
        findings = [
            RiskFinding(
                kind="typosquat",
                subject="dep",
                name="reqeusts",
                target="requests",
                level="FAIL",
                code="TS001",
                message="Suspected typosquat: 'reqeusts' is very similar to 'requests'",
                file="requirements.txt",
                lineno=12,
            ),
        ]

        report = render_text_report(findings, use_colors=False)

        # Check header
        assert "typo-shield Security Report" in report

        # Check summary
        assert "1 FAIL" in report
        assert "0 WARN" in report

        # Check failure section
        assert "FAILURES (1)" in report
        assert "[TS001]" in report
        assert "reqeusts" in report
        assert "requests" in report
        assert "requirements.txt:12" in report
        assert "Did you mean" in report

    def test_render_with_warnings(self) -> None:
        """Test rendering report with WARN findings."""
        findings = [
            RiskFinding(
                kind="missing_dep",
                subject="import",
                name="numpy",
                target="numpy",
                level="WARN",
                code="TS101",
                message="Import 'numpy' not found in declared dependencies",
                file="app.py",
                lineno=5,
            ),
        ]

        report = render_text_report(findings, use_colors=False)

        # Check summary
        assert "0 FAIL" in report
        assert "1 WARN" in report

        # Check warning section
        assert "WARNINGS (1)" in report
        assert "[TS101]" in report
        assert "numpy" in report
        assert "app.py:5" in report
        assert "Add" in report and "dependencies" in report

    def test_render_with_info(self) -> None:
        """Test rendering report with INFO findings."""
        findings = [
            RiskFinding(
                kind="stdlib_import",
                subject="import",
                name="os",
                target=None,
                level="INFO",
                code="TS900",
                message="Standard library import",
                file="app.py",
                lineno=1,
            ),
            RiskFinding(
                kind="local_import",
                subject="import",
                name="mymodule",
                target=None,
                level="INFO",
                code="TS900",
                message="Local module import",
                file="app.py",
                lineno=2,
            ),
        ]

        report = render_text_report(findings, use_colors=False)

        # Check summary
        assert "2 INFO" in report

        # Check info section
        assert "INFO (2)" in report
        assert "Standard library imports" in report
        assert "os" in report
        assert "Local project modules" in report
        assert "mymodule" in report

    def test_render_without_info(self) -> None:
        """Test rendering report without INFO findings when show_info=False."""
        findings = [
            RiskFinding(
                kind="stdlib_import",
                subject="import",
                name="os",
                target=None,
                level="INFO",
                code="TS900",
                message="Standard library import",
            ),
        ]

        report = render_text_report(findings, show_info=False, use_colors=False)

        # Summary should still show count
        assert "1 INFO" in report

        # But INFO section should not be present
        assert "INFO (1)" not in report
        assert "Standard library imports" not in report

    def test_render_empty(self) -> None:
        """Test rendering empty report."""
        report = render_text_report([], use_colors=False)

        # Check header is present
        assert "typo-shield Security Report" in report

        # Check summary shows zeros
        assert "0 FAIL" in report
        assert "0 WARN" in report
        assert "0 INFO" in report

    def test_render_mixed_findings(self) -> None:
        """Test rendering report with mixed severity levels."""
        findings = [
            RiskFinding(
                kind="typosquat",
                subject="dep",
                name="reqeusts",
                target="requests",
                level="FAIL",
                code="TS001",
                message="Suspected typosquat",
                file="requirements.txt",
                lineno=1,
            ),
            RiskFinding(
                kind="missing_dep",
                subject="import",
                name="numpy",
                target="numpy",
                level="WARN",
                code="TS101",
                message="Missing dependency",
                file="app.py",
                lineno=1,
            ),
            RiskFinding(
                kind="stdlib_import",
                subject="import",
                name="os",
                target=None,
                level="INFO",
                code="TS900",
                message="Standard library import",
            ),
        ]

        report = render_text_report(findings, use_colors=False)

        # Check all sections are present
        assert "FAILURES (1)" in report
        assert "WARNINGS (1)" in report
        assert "INFO (1)" in report

        # Check summary
        assert "1 FAIL" in report
        assert "1 WARN" in report
        assert "1 INFO" in report

    def test_render_with_colors(self) -> None:
        """Test that color codes are added when use_colors=True."""
        findings = [
            RiskFinding(
                kind="typosquat",
                subject="dep",
                name="reqeusts",
                target="requests",
                level="FAIL",
                code="TS001",
                message="Suspected typosquat",
            ),
        ]

        report = render_text_report(findings, use_colors=True)

        # Check that ANSI codes are present
        assert "\033[" in report  # ANSI escape sequence

    def test_render_without_colors(self) -> None:
        """Test that no color codes are added when use_colors=False."""
        findings = [
            RiskFinding(
                kind="typosquat",
                subject="dep",
                name="reqeusts",
                target="requests",
                level="FAIL",
                code="TS001",
                message="Suspected typosquat",
            ),
        ]

        report = render_text_report(findings, use_colors=False)

        # Check that no ANSI codes are present
        assert "\033[" not in report

    def test_render_suspicious_chars_finding(self) -> None:
        """Test rendering suspicious characters finding."""
        findings = [
            RiskFinding(
                kind="suspicious_chars",
                subject="dep",
                name="req@uests",
                target=None,
                level="WARN",
                code="TS003",
                message="Package name contains suspicious characters",
                file="requirements.txt",
                lineno=5,
            ),
        ]

        report = render_text_report(findings, use_colors=False)

        assert "[TS003]" in report
        assert "req@uests" in report
        assert "Verify" in report

    def test_render_multiple_info_findings_truncated(self) -> None:
        """Test that many INFO findings are truncated in summary."""
        findings = [
            RiskFinding(
                kind="stdlib_import",
                subject="import",
                name=f"module{i}",
                target=None,
                level="INFO",
                code="TS900",
                message="Standard library import",
            )
            for i in range(10)
        ]

        report = render_text_report(findings, use_colors=False)

        # Should show "... (+N more)"
        assert "(+5 more)" in report or "more)" in report

    def test_render_finding_without_file(self) -> None:
        """Test rendering finding without file location."""
        findings = [
            RiskFinding(
                kind="typosquat",
                subject="dep",
                name="reqeusts",
                target="requests",
                level="FAIL",
                code="TS001",
                message="Suspected typosquat",
                file=None,
                lineno=None,
            ),
        ]

        report = render_text_report(findings, use_colors=False)

        # Should still render without crashing
        assert "[TS001]" in report
        assert "reqeusts" in report


class TestRenderResultLine:
    """Tests for render_result_line()."""

    def test_result_line_passed(self) -> None:
        """Test result line when passed."""
        findings = [
            RiskFinding(
                kind="stdlib_import",
                subject="import",
                name="os",
                target=None,
                level="INFO",
                code="TS900",
                message="Standard library import",
            ),
        ]

        result = render_result_line(findings, fail_on="fail", use_colors=False)

        assert "PASSED" in result
        assert "exit code 0" in result
        assert "1 INFO" in result

    def test_result_line_failed(self) -> None:
        """Test result line when failed."""
        findings = [
            RiskFinding(
                kind="typosquat",
                subject="dep",
                name="reqeusts",
                target="requests",
                level="FAIL",
                code="TS001",
                message="Suspected typosquat",
            ),
        ]

        result = render_result_line(findings, fail_on="fail", use_colors=False)

        assert "FAILED" in result
        assert "exit code 1" in result
        assert "1 FAIL" in result

    def test_result_line_warn_with_fail_on_fail(self) -> None:
        """Test result line with WARN findings and fail_on='fail'."""
        findings = [
            RiskFinding(
                kind="missing_dep",
                subject="import",
                name="numpy",
                target="numpy",
                level="WARN",
                code="TS101",
                message="Missing dependency",
            ),
        ]

        result = render_result_line(findings, fail_on="fail", use_colors=False)

        assert "PASSED" in result
        assert "1 WARN" in result

    def test_result_line_warn_with_fail_on_warn(self) -> None:
        """Test result line with WARN findings and fail_on='warn'."""
        findings = [
            RiskFinding(
                kind="missing_dep",
                subject="import",
                name="numpy",
                target="numpy",
                level="WARN",
                code="TS101",
                message="Missing dependency",
            ),
        ]

        result = render_result_line(findings, fail_on="warn", use_colors=False)

        assert "FAILED" in result
        assert "1 WARN" in result

    def test_result_line_empty(self) -> None:
        """Test result line with no findings."""
        result = render_result_line([], fail_on="fail", use_colors=False)

        assert "PASSED" in result
        assert "exit code 0" in result

    def test_result_line_with_colors(self) -> None:
        """Test that color codes are added when use_colors=True."""
        findings = [
            RiskFinding(
                kind="typosquat",
                subject="dep",
                name="reqeusts",
                target="requests",
                level="FAIL",
                code="TS001",
                message="Suspected typosquat",
            ),
        ]

        result = render_result_line(findings, use_colors=True)

        # Check that ANSI codes are present
        assert "\033[" in result

    def test_result_line_mixed_counts(self) -> None:
        """Test result line with mixed severity counts."""
        findings = [
            RiskFinding(
                kind="typosquat",
                subject="dep",
                name="reqeusts",
                target="requests",
                level="FAIL",
                code="TS001",
                message="Suspected typosquat",
            ),
            RiskFinding(
                kind="missing_dep",
                subject="import",
                name="numpy",
                target="numpy",
                level="WARN",
                code="TS101",
                message="Missing dependency",
            ),
            RiskFinding(
                kind="stdlib_import",
                subject="import",
                name="os",
                target=None,
                level="INFO",
                code="TS900",
                message="Standard library import",
            ),
        ]

        result = render_result_line(findings, fail_on="fail", use_colors=False)

        assert "1 FAIL" in result
        assert "1 WARN" in result
        assert "1 INFO" in result

