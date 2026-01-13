"""Tests for risk scoring."""

from __future__ import annotations

from typo_shield.risk.models import RiskFinding
from typo_shield.risk.score import (
    aggregate_by_code,
    aggregate_by_kind,
    aggregate_findings,
    compute_stats,
    filter_by_kind,
    filter_by_level,
    get_highest_severity,
)


class TestAggregateFindings:
    """Tests for aggregate_findings()."""

    def test_aggregate_mixed_levels(self) -> None:
        """Test aggregating findings with mixed severity levels."""
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

        result = aggregate_findings(findings)

        assert result == {"INFO": 1, "WARN": 1, "FAIL": 1}

    def test_aggregate_multiple_same_level(self) -> None:
        """Test aggregating multiple findings at same level."""
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
                kind="typosquat",
                subject="dep",
                name="flsk",
                target="flask",
                level="FAIL",
                code="TS001",
                message="...",
            ),
        ]

        result = aggregate_findings(findings)

        assert result == {"INFO": 0, "WARN": 0, "FAIL": 2}

    def test_aggregate_empty(self) -> None:
        """Test aggregating empty list."""
        result = aggregate_findings([])

        assert result == {"INFO": 0, "WARN": 0, "FAIL": 0}

    def test_aggregate_info_only(self) -> None:
        """Test aggregating only INFO findings."""
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
            RiskFinding(
                kind="local_import",
                subject="import",
                name="mymodule",
                target=None,
                level="INFO",
                code="TS900",
                message="...",
            ),
        ]

        result = aggregate_findings(findings)

        assert result == {"INFO": 2, "WARN": 0, "FAIL": 0}


class TestAggregateByKind:
    """Tests for aggregate_by_kind()."""

    def test_aggregate_by_kind_multiple_types(self) -> None:
        """Test aggregating by kind with multiple types."""
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
                kind="typosquat",
                subject="dep",
                name="flsk",
                target="flask",
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

        result = aggregate_by_kind(findings)

        assert result == {"typosquat": 2, "missing_dep": 1}

    def test_aggregate_by_kind_empty(self) -> None:
        """Test aggregating by kind with empty list."""
        result = aggregate_by_kind([])

        assert result == {}


class TestAggregateByCode:
    """Tests for aggregate_by_code()."""

    def test_aggregate_by_code_multiple_codes(self) -> None:
        """Test aggregating by code with multiple codes."""
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
                kind="typosquat",
                subject="dep",
                name="flsk",
                target="flask",
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

        result = aggregate_by_code(findings)

        assert result == {"TS001": 2, "TS101": 1}

    def test_aggregate_by_code_empty(self) -> None:
        """Test aggregating by code with empty list."""
        result = aggregate_by_code([])

        assert result == {}


class TestGetHighestSeverity:
    """Tests for get_highest_severity()."""

    def test_highest_severity_fail(self) -> None:
        """Test that FAIL is highest severity."""
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
                kind="typosquat",
                subject="dep",
                name="reqeusts",
                target="requests",
                level="FAIL",
                code="TS001",
                message="...",
            ),
        ]

        result = get_highest_severity(findings)

        assert result == "FAIL"

    def test_highest_severity_warn(self) -> None:
        """Test that WARN is returned when no FAIL."""
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

        result = get_highest_severity(findings)

        assert result == "WARN"

    def test_highest_severity_info(self) -> None:
        """Test that INFO is returned when only INFO findings."""
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

        result = get_highest_severity(findings)

        assert result == "INFO"

    def test_highest_severity_empty(self) -> None:
        """Test that None is returned for empty findings."""
        result = get_highest_severity([])

        assert result is None


class TestFilterByLevel:
    """Tests for filter_by_level()."""

    def test_filter_by_level_fail(self) -> None:
        """Test filtering by FAIL level."""
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

        result = filter_by_level(findings, "FAIL")

        assert len(result) == 1
        assert result[0].level == "FAIL"
        assert result[0].name == "reqeusts"

    def test_filter_by_level_no_matches(self) -> None:
        """Test filtering when no matches."""
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

        result = filter_by_level(findings, "FAIL")

        assert len(result) == 0


class TestFilterByKind:
    """Tests for filter_by_kind()."""

    def test_filter_by_kind_typosquat(self) -> None:
        """Test filtering by typosquat kind."""
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

        result = filter_by_kind(findings, "typosquat")

        assert len(result) == 1
        assert result[0].kind == "typosquat"

    def test_filter_by_kind_no_matches(self) -> None:
        """Test filtering when no matches."""
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

        result = filter_by_kind(findings, "missing_dep")

        assert len(result) == 0


class TestComputeStats:
    """Tests for compute_stats()."""

    def test_compute_stats_comprehensive(self) -> None:
        """Test computing comprehensive statistics."""
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

        stats = compute_stats(findings)

        assert stats["total"] == 3
        assert stats["by_level"] == {"INFO": 1, "WARN": 1, "FAIL": 1}
        assert stats["by_kind"] == {"typosquat": 1, "missing_dep": 1, "stdlib_import": 1}
        assert stats["by_code"] == {"TS001": 1, "TS101": 1, "TS900": 1}
        assert stats["highest_severity"] == "FAIL"

    def test_compute_stats_empty(self) -> None:
        """Test computing stats for empty findings."""
        stats = compute_stats([])

        assert stats["total"] == 0
        assert stats["by_level"] == {"INFO": 0, "WARN": 0, "FAIL": 0}
        assert stats["by_kind"] == {}
        assert stats["by_code"] == {}
        assert stats["highest_severity"] is None

