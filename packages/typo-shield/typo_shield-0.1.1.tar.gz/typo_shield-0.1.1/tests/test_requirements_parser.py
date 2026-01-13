"""Tests for requirements.txt parser."""

from __future__ import annotations

from typo_shield.diff import DiffFileChange
from typo_shield.scanners.deps_requirements import (
    DependencyFinding,
    deduplicate_dependencies,
    normalize_package_name,
    scan_requirements,
)


class TestScanRequirements:
    """Tests for scan_requirements()."""

    def test_simple_package(self) -> None:
        """Test parsing simple package name."""
        change = DiffFileChange(
            path="requirements.txt",
            added_lines=[(1, "requests")],
        )

        findings = scan_requirements(change)

        assert len(findings) == 1
        assert findings[0].name == "requests"
        assert findings[0].specifier == ""
        assert findings[0].source == "requirements"

    def test_versioned_package(self) -> None:
        """Test parsing package with version."""
        change = DiffFileChange(
            path="requirements.txt",
            added_lines=[(1, "requests==2.28.0")],
        )

        findings = scan_requirements(change)

        assert len(findings) == 1
        assert findings[0].name == "requests"
        assert findings[0].specifier == "==2.28.0"

    def test_version_specifiers(self) -> None:
        """Test parsing various version specifiers."""
        change = DiffFileChange(
            path="requirements.txt",
            added_lines=[
                (1, "requests>=2.0"),
                (2, "numpy>=1.20,<2.0"),
                (3, "flask~=2.0.0"),
                (4, "django!=3.0.*"),
            ],
        )

        findings = scan_requirements(change)

        assert len(findings) == 4
        assert findings[0].name == "requests"
        assert ">=2.0" in findings[0].specifier
        assert findings[1].name == "numpy"
        assert ">=1.20" in findings[1].specifier and "<2.0" in findings[1].specifier

    def test_package_with_extras(self) -> None:
        """Test parsing package with extras."""
        change = DiffFileChange(
            path="requirements.txt",
            added_lines=[(1, "requests[security]>=2.0")],
        )

        findings = scan_requirements(change)

        assert len(findings) == 1
        assert findings[0].name == "requests"
        assert ">=2.0" in findings[0].specifier

    def test_skip_comments(self) -> None:
        """Test that comments are skipped."""
        change = DiffFileChange(
            path="requirements.txt",
            added_lines=[
                (1, "# This is a comment"),
                (2, "requests"),
                (3, "# Another comment"),
            ],
        )

        findings = scan_requirements(change)

        assert len(findings) == 1
        assert findings[0].name == "requests"

    def test_inline_comments(self) -> None:
        """Test handling inline comments."""
        change = DiffFileChange(
            path="requirements.txt",
            added_lines=[
                (1, "requests  # HTTP library"),
                (2, "numpy>=1.20  # Scientific computing"),
            ],
        )

        findings = scan_requirements(change)

        assert len(findings) == 2
        assert findings[0].name == "requests"
        assert findings[1].name == "numpy"

    def test_skip_empty_lines(self) -> None:
        """Test that empty lines are skipped."""
        change = DiffFileChange(
            path="requirements.txt",
            added_lines=[
                (1, ""),
                (2, "requests"),
                (3, "   "),
                (4, "numpy"),
            ],
        )

        findings = scan_requirements(change)

        assert len(findings) == 2
        assert findings[0].name == "requests"
        assert findings[1].name == "numpy"

    def test_skip_option_lines(self) -> None:
        """Test that option lines (-r, --index-url) are skipped."""
        change = DiffFileChange(
            path="requirements.txt",
            added_lines=[
                (1, "-r other.txt"),
                (2, "--index-url https://pypi.org/simple"),
                (3, "--extra-index-url https://private.pypi.org"),
                (4, "requests"),
                (5, "-c constraints.txt"),
            ],
        )

        findings = scan_requirements(change)

        # Only 'requests' should be found
        assert len(findings) == 1
        assert findings[0].name == "requests"

    def test_git_url(self) -> None:
        """Test parsing git URL dependencies."""
        change = DiffFileChange(
            path="requirements.txt",
            added_lines=[
                (1, "git+https://github.com/user/repo.git"),
                (2, "git+https://github.com/user/package.git#egg=mypackage"),
            ],
        )

        findings = scan_requirements(change)

        assert len(findings) == 2
        assert findings[0].is_git is True
        assert findings[1].is_git is True
        assert findings[1].name == "mypackage"  # Extracted from #egg=

    def test_local_path(self) -> None:
        """Test parsing local file/directory dependencies."""
        change = DiffFileChange(
            path="requirements.txt",
            added_lines=[
                (1, "./local-package"),
                (2, "../sibling-package"),
                (3, "file:///absolute/path/to/package"),
            ],
        )

        findings = scan_requirements(change)

        assert len(findings) == 3
        assert all(f.is_local for f in findings)
        assert findings[0].name == "local-package"
        assert findings[1].name == "sibling-package"

    def test_whitespace_handling(self) -> None:
        """Test handling of whitespace."""
        change = DiffFileChange(
            path="requirements.txt",
            added_lines=[
                (1, "  requests  "),
                (2, "\tnumpy\t"),
                (3, "   flask   >=2.0   "),
            ],
        )

        findings = scan_requirements(change)

        assert len(findings) == 3
        assert findings[0].name == "requests"
        assert findings[1].name == "numpy"
        assert findings[2].name == "flask"

    def test_case_sensitivity(self) -> None:
        """Test that package names are normalized to lowercase."""
        change = DiffFileChange(
            path="requirements.txt",
            added_lines=[
                (1, "Flask"),
                (2, "REQUESTS"),
                (3, "NumPy"),
            ],
        )

        findings = scan_requirements(change)

        assert len(findings) == 3
        assert findings[0].name == "flask"
        assert findings[1].name == "requests"
        assert findings[2].name == "numpy"

    def test_underscore_to_dash(self) -> None:
        """Test that underscores are converted to dashes."""
        change = DiffFileChange(
            path="requirements.txt",
            added_lines=[
                (1, "Flask_RESTful"),
                (2, "some_package"),
            ],
        )

        findings = scan_requirements(change)

        assert len(findings) == 2
        assert findings[0].name == "flask-restful"
        assert findings[1].name == "some-package"

    def test_invalid_requirement(self) -> None:
        """Test that invalid requirements are skipped."""
        change = DiffFileChange(
            path="requirements.txt",
            added_lines=[
                (1, "requests"),
                (2, "this is not valid"),
                (3, "numpy"),
            ],
        )

        findings = scan_requirements(change)

        # Invalid line should be skipped
        assert len(findings) == 2
        assert findings[0].name == "requests"
        assert findings[1].name == "numpy"

    def test_complex_file(self) -> None:
        """Test parsing complex requirements file."""
        change = DiffFileChange(
            path="requirements.txt",
            added_lines=[
                (1, "# Core dependencies"),
                (2, "requests>=2.28.0"),
                (3, ""),
                (4, "# Data processing"),
                (5, "numpy>=1.20,<2.0"),
                (6, "pandas[performance]>=1.3.0  # DataFrame library"),
                (7, ""),
                (8, "# Web framework"),
                (9, "Flask==2.3.0"),
                (10, "Flask-RESTful>=0.3.9"),
            ],
        )

        findings = scan_requirements(change)

        assert len(findings) == 5
        names = [f.name for f in findings]
        assert "requests" in names
        assert "numpy" in names
        assert "pandas" in names
        assert "flask" in names
        assert "flask-restful" in names


class TestNormalizePackageName:
    """Tests for normalize_package_name()."""

    def test_lowercase(self) -> None:
        """Test conversion to lowercase."""
        assert normalize_package_name("Flask") == "flask"
        assert normalize_package_name("REQUESTS") == "requests"

    def test_underscore_to_dash(self) -> None:
        """Test underscore to dash conversion."""
        assert normalize_package_name("Flask_RESTful") == "flask-restful"
        assert normalize_package_name("some_package") == "some-package"

    def test_dot_to_dash(self) -> None:
        """Test dot to dash conversion."""
        assert normalize_package_name("some.package") == "some-package"
        assert normalize_package_name("name.with.dots") == "name-with-dots"

    def test_combined(self) -> None:
        """Test combined transformations."""
        assert normalize_package_name("My_Package.Name") == "my-package-name"

    def test_already_normalized(self) -> None:
        """Test already normalized names."""
        assert normalize_package_name("requests") == "requests"
        assert normalize_package_name("some-package") == "some-package"


class TestDeduplicateDependencies:
    """Tests for deduplicate_dependencies()."""

    def test_deduplicate_same_package(self) -> None:
        """Test deduplication of same package."""
        findings = [
            DependencyFinding(
                file="requirements.txt",
                name="requests",
                specifier=">=2.0",
                source="requirements",
            ),
            DependencyFinding(
                file="requirements.txt",
                name="requests",
                specifier=">=2.28.0",
                source="requirements",
            ),
            DependencyFinding(
                file="requirements.txt",
                name="numpy",
                specifier="",
                source="requirements",
            ),
        ]

        dedup = deduplicate_dependencies(findings)

        assert len(dedup) == 2
        names = [f.name for f in dedup]
        assert names.count("requests") == 1
        assert names.count("numpy") == 1
        # First occurrence should be kept
        assert dedup[0].specifier == ">=2.0"

    def test_deduplicate_different_files(self) -> None:
        """Test that same package in different files is NOT deduplicated."""
        findings = [
            DependencyFinding(
                file="requirements.txt",
                name="requests",
                specifier="",
                source="requirements",
            ),
            DependencyFinding(
                file="requirements-dev.txt",
                name="requests",
                specifier="",
                source="requirements",
            ),
        ]

        dedup = deduplicate_dependencies(findings)

        # Different files, both should be kept
        assert len(dedup) == 2

    def test_deduplicate_empty(self) -> None:
        """Test deduplication of empty list."""
        dedup = deduplicate_dependencies([])
        assert len(dedup) == 0

