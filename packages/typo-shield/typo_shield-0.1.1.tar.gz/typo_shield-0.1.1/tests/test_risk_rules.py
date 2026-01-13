"""Tests for risk rules."""

from __future__ import annotations

from typo_shield.risk.models import RiskFinding
from typo_shield.risk.rules import (
    filter_actionable_findings,
    get_exit_code,
    get_result_summary,
    should_fail,
    validate_fail_on_value,
)


class TestShouldFail:
    """Tests for should_fail()."""

    def test_should_fail_on_fail_with_fail_finding(self) -> None:
        """Test that fail_on='fail' fails when there are FAIL findings."""
        findings = [
            RiskFinding(
                kind="typosquat",
                subject="dep",
                name="reqeusts",
                target="requests",
                level="FAIL",
                code="TS001",
                message="...",
            ),
        ]

        assert should_fail(findings, "fail") is True

    def test_should_fail_on_fail_with_warn_finding(self) -> None:
        """Test that fail_on='fail' passes when only WARN findings."""
        findings = [
            RiskFinding(
                kind="missing_dep",
                subject="import",
                name="numpy",
                target=None,
                level="WARN",
                code="TS101",
                message="...",
            ),
        ]

        assert should_fail(findings, "fail") is False

    def test_should_fail_on_fail_with_info_finding(self) -> None:
        """Test that fail_on='fail' passes when only INFO findings."""
        findings = [
            RiskFinding(
                kind="stdlib_import",
                subject="import",
                name="os",
                target=None,
                level="INFO",
                code="TS900",
                message="...",
            ),
        ]

        assert should_fail(findings, "fail") is False

    def test_should_fail_on_warn_with_fail_finding(self) -> None:
        """Test that fail_on='warn' fails when there are FAIL findings."""
        findings = [
            RiskFinding(
                kind="typosquat",
                subject="dep",
                name="reqeusts",
                target="requests",
                level="FAIL",
                code="TS001",
                message="...",
            ),
        ]

        assert should_fail(findings, "warn") is True

    def test_should_fail_on_warn_with_warn_finding(self) -> None:
        """Test that fail_on='warn' fails when there are WARN findings."""
        findings = [
            RiskFinding(
                kind="missing_dep",
                subject="import",
                name="numpy",
                target=None,
                level="WARN",
                code="TS101",
                message="...",
            ),
        ]

        assert should_fail(findings, "warn") is True

    def test_should_fail_on_warn_with_info_finding(self) -> None:
        """Test that fail_on='warn' passes when only INFO findings."""
        findings = [
            RiskFinding(
                kind="stdlib_import",
                subject="import",
                name="os",
                target=None,
                level="INFO",
                code="TS900",
                message="...",
            ),
        ]

        assert should_fail(findings, "warn") is False

    def test_should_fail_empty_findings(self) -> None:
        """Test that empty findings don't cause failure."""
        assert should_fail([], "fail") is False
        assert should_fail([], "warn") is False

    def test_should_fail_mixed_findings_fail_on_fail(self) -> None:
        """Test mixed findings with fail_on='fail'."""
        findings = [
            RiskFinding(
                kind="typosquat",
                subject="dep",
                name="reqeusts",
                target="requests",
                level="FAIL",
                code="TS001",
                message="...",
            ),
            RiskFinding(
                kind="missing_dep",
                subject="import",
                name="numpy",
                target=None,
                level="WARN",
                code="TS101",
                message="...",
            ),
            RiskFinding(
                kind="stdlib_import",
                subject="import",
                name="os",
                target=None,
                level="INFO",
                code="TS900",
                message="...",
            ),
        ]

        assert should_fail(findings, "fail") is True

    def test_should_fail_mixed_findings_fail_on_warn(self) -> None:
        """Test mixed findings with fail_on='warn'."""
        findings = [
            RiskFinding(
                kind="missing_dep",
                subject="import",
                name="numpy",
                target=None,
                level="WARN",
                code="TS101",
                message="...",
            ),
            RiskFinding(
                kind="stdlib_import",
                subject="import",
                name="os",
                target=None,
                level="INFO",
                code="TS900",
                message="...",
            ),
        ]

        assert should_fail(findings, "warn") is True


class TestGetExitCode:
    """Tests for get_exit_code()."""

    def test_exit_code_success(self) -> None:
        """Test that success returns exit code 0."""
        findings = [
            RiskFinding(
                kind="stdlib_import",
                subject="import",
                name="os",
                target=None,
                level="INFO",
                code="TS900",
                message="...",
            ),
        ]

        assert get_exit_code(findings, "fail") == 0

    def test_exit_code_failure(self) -> None:
        """Test that failure returns exit code 1."""
        findings = [
            RiskFinding(
                kind="typosquat",
                subject="dep",
                name="reqeusts",
                target="requests",
                level="FAIL",
                code="TS001",
                message="...",
            ),
        ]

        assert get_exit_code(findings, "fail") == 1

    def test_exit_code_warn_with_fail_on_fail(self) -> None:
        """Test that WARN findings pass with fail_on='fail'."""
        findings = [
            RiskFinding(
                kind="missing_dep",
                subject="import",
                name="numpy",
                target=None,
                level="WARN",
                code="TS101",
                message="...",
            ),
        ]

        assert get_exit_code(findings, "fail") == 0

    def test_exit_code_warn_with_fail_on_warn(self) -> None:
        """Test that WARN findings fail with fail_on='warn'."""
        findings = [
            RiskFinding(
                kind="missing_dep",
                subject="import",
                name="numpy",
                target=None,
                level="WARN",
                code="TS101",
                message="...",
            ),
        ]

        assert get_exit_code(findings, "warn") == 1


class TestFilterActionableFindings:
    """Tests for filter_actionable_findings()."""

    def test_filter_actionable_mixed(self) -> None:
        """Test filtering actionable findings from mixed levels."""
        findings = [
            RiskFinding(
                kind="typosquat",
                subject="dep",
                name="reqeusts",
                target="requests",
                level="FAIL",
                code="TS001",
                message="...",
            ),
            RiskFinding(
                kind="missing_dep",
                subject="import",
                name="numpy",
                target=None,
                level="WARN",
                code="TS101",
                message="...",
            ),
            RiskFinding(
                kind="stdlib_import",
                subject="import",
                name="os",
                target=None,
                level="INFO",
                code="TS900",
                message="...",
            ),
        ]

        result = filter_actionable_findings(findings)

        assert len(result) == 2
        assert all(f.level in ["WARN", "FAIL"] for f in result)

    def test_filter_actionable_info_only(self) -> None:
        """Test that INFO-only findings return empty list."""
        findings = [
            RiskFinding(
                kind="stdlib_import",
                subject="import",
                name="os",
                target=None,
                level="INFO",
                code="TS900",
                message="...",
            ),
        ]

        result = filter_actionable_findings(findings)

        assert len(result) == 0

    def test_filter_actionable_empty(self) -> None:
        """Test that empty findings return empty list."""
        result = filter_actionable_findings([])

        assert len(result) == 0


class TestValidateFailOnValue:
    """Tests for validate_fail_on_value()."""

    def test_validate_fail(self) -> None:
        """Test that 'fail' is valid."""
        assert validate_fail_on_value("fail") is True

    def test_validate_warn(self) -> None:
        """Test that 'warn' is valid."""
        assert validate_fail_on_value("warn") is True

    def test_validate_invalid(self) -> None:
        """Test that invalid values are rejected."""
        assert validate_fail_on_value("invalid") is False
        assert validate_fail_on_value("error") is False
        assert validate_fail_on_value("") is False


class TestGetResultSummary:
    """Tests for get_result_summary()."""

    def test_result_summary_passed(self) -> None:
        """Test result summary when passed."""
        findings = [
            RiskFinding(
                kind="stdlib_import",
                subject="import",
                name="os",
                target=None,
                level="INFO",
                code="TS900",
                message="...",
            ),
        ]

        summary = get_result_summary(findings, "fail")

        assert summary["passed"] is True
        assert summary["exit_code"] == 0
        assert summary["fail_on"] == "fail"
        assert summary["counts"] == {"INFO": 1, "WARN": 0, "FAIL": 0}
        assert summary["total_findings"] == 1
        assert summary["actionable_findings"] == 0

    def test_result_summary_failed(self) -> None:
        """Test result summary when failed."""
        findings = [
            RiskFinding(
                kind="typosquat",
                subject="dep",
                name="reqeusts",
                target="requests",
                level="FAIL",
                code="TS001",
                message="...",
            ),
            RiskFinding(
                kind="missing_dep",
                subject="import",
                name="numpy",
                target=None,
                level="WARN",
                code="TS101",
                message="...",
            ),
        ]

        summary = get_result_summary(findings, "fail")

        assert summary["passed"] is False
        assert summary["exit_code"] == 1
        assert summary["fail_on"] == "fail"
        assert summary["counts"] == {"INFO": 0, "WARN": 1, "FAIL": 1}
        assert summary["total_findings"] == 2
        assert summary["actionable_findings"] == 2

    def test_result_summary_warn_with_fail_on_warn(self) -> None:
        """Test result summary with WARN findings and fail_on='warn'."""
        findings = [
            RiskFinding(
                kind="missing_dep",
                subject="import",
                name="numpy",
                target=None,
                level="WARN",
                code="TS101",
                message="...",
            ),
        ]

        summary = get_result_summary(findings, "warn")

        assert summary["passed"] is False
        assert summary["exit_code"] == 1
        assert summary["fail_on"] == "warn"

    def test_result_summary_empty(self) -> None:
        """Test result summary with no findings."""
        summary = get_result_summary([], "fail")

        assert summary["passed"] is True
        assert summary["exit_code"] == 0
        assert summary["total_findings"] == 0
        assert summary["actionable_findings"] == 0

