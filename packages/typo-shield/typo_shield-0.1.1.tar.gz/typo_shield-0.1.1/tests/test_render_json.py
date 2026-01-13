"""Tests for JSON report rendering."""

from __future__ import annotations

import json

import pytest

from typo_shield.report.render_json import (
    parse_json_report,
    render_json_report,
    render_json_summary,
    validate_json_report,
)
from typo_shield.risk.models import RiskFinding


class TestRenderJsonReport:
    """Tests for render_json_report()."""

    def test_render_json_with_findings(self) -> None:
        """Test rendering JSON report with findings."""
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
                lineno=12,
            ),
        ]

        report = render_json_report(findings)
        data = json.loads(report)

        # Check structure
        assert "version" in data
        assert "summary" in data
        assert "findings" in data

        # Check version
        assert data["version"] == "1.0"

        # Check summary
        assert data["summary"]["fail"] == 1
        assert data["summary"]["warn"] == 0
        assert data["summary"]["info"] == 0
        assert data["summary"]["total"] == 1

        # Check findings
        assert len(data["findings"]) == 1
        finding = data["findings"][0]
        assert finding["level"] == "FAIL"
        assert finding["code"] == "TS001"
        assert finding["kind"] == "typosquat"
        assert finding["name"] == "reqeusts"
        assert finding["target"] == "requests"
        assert finding["file"] == "requirements.txt"
        assert finding["lineno"] == 12

    def test_render_json_empty(self) -> None:
        """Test rendering JSON report with no findings."""
        report = render_json_report([])
        data = json.loads(report)

        assert data["summary"]["fail"] == 0
        assert data["summary"]["warn"] == 0
        assert data["summary"]["info"] == 0
        assert data["summary"]["total"] == 0
        assert len(data["findings"]) == 0

    def test_render_json_multiple_findings(self) -> None:
        """Test rendering JSON report with multiple findings."""
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

        report = render_json_report(findings)
        data = json.loads(report)

        assert data["summary"]["fail"] == 1
        assert data["summary"]["warn"] == 1
        assert data["summary"]["info"] == 1
        assert data["summary"]["total"] == 3
        assert len(data["findings"]) == 3

    def test_render_json_compact(self) -> None:
        """Test rendering compact JSON (no indentation)."""
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

        report = render_json_report(findings, indent=None)

        # Compact JSON should not have newlines
        assert "\n" not in report

        # But should still be valid
        data = json.loads(report)
        assert data["summary"]["fail"] == 1

    def test_render_json_with_context(self) -> None:
        """Test rendering finding with context field."""
        findings = [
            RiskFinding(
                kind="typosquat",
                subject="dep",
                name="reqeusts",
                target="requests",
                level="FAIL",
                code="TS001",
                message="Suspected typosquat",
                context={"distance": "1", "algorithm": "levenshtein"},
            ),
        ]

        report = render_json_report(findings)
        data = json.loads(report)

        finding = data["findings"][0]
        assert "context" in finding
        assert finding["context"]["distance"] == "1"
        assert finding["context"]["algorithm"] == "levenshtein"

    def test_render_json_without_file_location(self) -> None:
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

        report = render_json_report(findings)
        data = json.loads(report)

        finding = data["findings"][0]
        assert finding["file"] is None
        assert finding["lineno"] is None


class TestRenderJsonSummary:
    """Tests for render_json_summary()."""

    def test_render_summary_passed(self) -> None:
        """Test rendering summary when passed."""
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

        summary = render_json_summary(findings, fail_on="fail")
        data = json.loads(summary)

        assert data["result"]["passed"] is True
        assert data["result"]["exit_code"] == 0
        assert data["result"]["fail_on"] == "fail"
        assert data["summary"]["actionable"] == 0

    def test_render_summary_failed(self) -> None:
        """Test rendering summary when failed."""
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

        summary = render_json_summary(findings, fail_on="fail")
        data = json.loads(summary)

        assert data["result"]["passed"] is False
        assert data["result"]["exit_code"] == 1
        assert data["summary"]["actionable"] == 1

    def test_render_summary_warn_with_fail_on_warn(self) -> None:
        """Test rendering summary with WARN findings and fail_on='warn'."""
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

        summary = render_json_summary(findings, fail_on="warn")
        data = json.loads(summary)

        assert data["result"]["passed"] is False
        assert data["result"]["exit_code"] == 1
        assert data["summary"]["actionable"] == 1

    def test_render_summary_empty(self) -> None:
        """Test rendering summary with no findings."""
        summary = render_json_summary([])
        data = json.loads(summary)

        assert data["result"]["passed"] is True
        assert data["result"]["exit_code"] == 0
        assert data["summary"]["total"] == 0
        assert data["summary"]["actionable"] == 0


class TestParseJsonReport:
    """Tests for parse_json_report()."""

    def test_parse_valid_report(self) -> None:
        """Test parsing a valid JSON report."""
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

        report = render_json_report(findings)
        parsed = parse_json_report(report)

        assert parsed["version"] == "1.0"
        assert parsed["summary"]["fail"] == 1
        assert len(parsed["findings"]) == 1

    def test_parse_invalid_json(self) -> None:
        """Test parsing invalid JSON raises exception."""
        with pytest.raises(json.JSONDecodeError):
            parse_json_report("not valid json")


class TestValidateJsonReport:
    """Tests for validate_json_report()."""

    def test_validate_valid_report(self) -> None:
        """Test validating a valid JSON report."""
        report = render_json_report([])
        is_valid, error = validate_json_report(report)

        assert is_valid is True
        assert error is None

    def test_validate_invalid_json(self) -> None:
        """Test validating invalid JSON."""
        is_valid, error = validate_json_report("not valid json")

        assert is_valid is False
        assert "Invalid JSON" in error

    def test_validate_not_object(self) -> None:
        """Test validating JSON that is not an object."""
        is_valid, error = validate_json_report("[]")

        assert is_valid is False
        assert "must be a JSON object" in error

    def test_validate_missing_version(self) -> None:
        """Test validating report missing version field."""
        report = json.dumps({
            "summary": {"fail": 0, "warn": 0, "info": 0, "total": 0},
            "findings": [],
        })

        is_valid, error = validate_json_report(report)

        assert is_valid is False
        assert "version" in error

    def test_validate_missing_summary(self) -> None:
        """Test validating report missing summary field."""
        report = json.dumps({
            "version": "1.0",
            "findings": [],
        })

        is_valid, error = validate_json_report(report)

        assert is_valid is False
        assert "summary" in error

    def test_validate_missing_summary_field(self) -> None:
        """Test validating report missing summary sub-field."""
        report = json.dumps({
            "version": "1.0",
            "summary": {"fail": 0, "warn": 0},  # Missing "info" and "total"
            "findings": [],
        })

        is_valid, error = validate_json_report(report)

        assert is_valid is False
        assert "info" in error or "total" in error

    def test_validate_missing_findings(self) -> None:
        """Test validating report missing findings field."""
        report = json.dumps({
            "version": "1.0",
            "summary": {"fail": 0, "warn": 0, "info": 0, "total": 0},
        })

        is_valid, error = validate_json_report(report)

        assert is_valid is False
        assert "findings" in error

    def test_validate_findings_not_array(self) -> None:
        """Test validating report where findings is not an array."""
        report = json.dumps({
            "version": "1.0",
            "summary": {"fail": 0, "warn": 0, "info": 0, "total": 0},
            "findings": {},  # Should be array
        })

        is_valid, error = validate_json_report(report)

        assert is_valid is False
        assert "array" in error


class TestJsonReportIntegration:
    """Integration tests for JSON reporting."""

    def test_round_trip(self) -> None:
        """Test that reports can be serialized and deserialized."""
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
                lineno=12,
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
                lineno=5,
            ),
        ]

        # Render to JSON
        report_json = render_json_report(findings)

        # Validate
        is_valid, error = validate_json_report(report_json)
        assert is_valid is True

        # Parse back
        data = parse_json_report(report_json)

        # Verify data integrity
        assert data["summary"]["fail"] == 1
        assert data["summary"]["warn"] == 1
        assert len(data["findings"]) == 2

    def test_summary_consistency(self) -> None:
        """Test that summary counts match findings."""
        findings = [
            RiskFinding(kind="typosquat", subject="dep", name="a", target=None,
                       level="FAIL", code="TS001", message="..."),
            RiskFinding(kind="missing_dep", subject="import", name="b", target=None,
                       level="WARN", code="TS101", message="..."),
            RiskFinding(kind="stdlib_import", subject="import", name="c", target=None,
                       level="INFO", code="TS900", message="..."),
        ]

        report_json = render_json_report(findings)
        data = parse_json_report(report_json)

        # Count findings by level
        fail_count = sum(1 for f in data["findings"] if f["level"] == "FAIL")
        warn_count = sum(1 for f in data["findings"] if f["level"] == "WARN")
        info_count = sum(1 for f in data["findings"] if f["level"] == "INFO")

        # Should match summary
        assert data["summary"]["fail"] == fail_count
        assert data["summary"]["warn"] == warn_count
        assert data["summary"]["info"] == info_count
        assert data["summary"]["total"] == len(data["findings"])

