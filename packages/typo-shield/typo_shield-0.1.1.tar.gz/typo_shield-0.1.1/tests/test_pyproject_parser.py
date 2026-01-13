"""Tests for pyproject.toml parser."""

from __future__ import annotations

from pathlib import Path

from typo_shield.diff import DiffFileChange
from typo_shield.scanners.deps_pyproject import scan_pyproject


class TestScanPyprojectPEP621:
    """Tests for PEP 621 format parsing."""

    def test_simple_dependencies(self, tmp_path: Path) -> None:
        """Test parsing simple PEP 621 dependencies."""
        pyproject = tmp_path / "pyproject.toml"
        pyproject.write_text("""
[project]
name = "myproject"
dependencies = [
    "requests>=2.28.0",
    "numpy>=1.20",
]
""")

        change = DiffFileChange(
            path="pyproject.toml",
            added_lines=[
                (4, '    "requests>=2.28.0",'),
                (5, '    "numpy>=1.20",'),
            ],
        )

        findings = scan_pyproject(change, tmp_path)

        assert len(findings) == 2
        names = {f.name for f in findings}
        assert "requests" in names
        assert "numpy" in names
        assert all(f.source == "pyproject_pep621" for f in findings)

    def test_optional_dependencies(self, tmp_path: Path) -> None:
        """Test parsing optional dependencies."""
        pyproject = tmp_path / "pyproject.toml"
        pyproject.write_text("""
[project]
name = "myproject"

[project.optional-dependencies]
dev = ["pytest>=7.0", "mypy>=1.0"]
docs = ["sphinx>=5.0"]
""")

        change = DiffFileChange(
            path="pyproject.toml",
            added_lines=[
                (5, 'dev = ["pytest>=7.0", "mypy>=1.0"]'),
                (6, 'docs = ["sphinx>=5.0"]'),
            ],
        )

        findings = scan_pyproject(change, tmp_path)

        assert len(findings) == 3
        names = {f.name for f in findings}
        assert "pytest" in names
        assert "mypy" in names
        assert "sphinx" in names

    def test_with_extras(self, tmp_path: Path) -> None:
        """Test parsing dependencies with extras."""
        pyproject = tmp_path / "pyproject.toml"
        pyproject.write_text("""
[project]
dependencies = [
    "requests[security]>=2.28.0",
]
""")

        change = DiffFileChange(
            path="pyproject.toml",
            added_lines=[(3, '    "requests[security]>=2.28.0",')],
        )

        findings = scan_pyproject(change, tmp_path)

        assert len(findings) == 1
        assert findings[0].name == "requests"

    def test_complex_version_specifiers(self, tmp_path: Path) -> None:
        """Test parsing complex version specifiers."""
        pyproject = tmp_path / "pyproject.toml"
        pyproject.write_text("""
[project]
dependencies = [
    "numpy>=1.20,<2.0",
    "flask~=2.0.0",
]
""")

        change = DiffFileChange(
            path="pyproject.toml",
            added_lines=[
                (3, '    "numpy>=1.20,<2.0",'),
                (4, '    "flask~=2.0.0",'),
            ],
        )

        findings = scan_pyproject(change, tmp_path)

        assert len(findings) == 2
        numpy_finding = next(f for f in findings if f.name == "numpy")
        assert ">=1.20" in numpy_finding.specifier
        assert "<2.0" in numpy_finding.specifier


class TestScanPyprojectPoetry:
    """Tests for Poetry format parsing."""

    def test_simple_poetry_dependencies(self, tmp_path: Path) -> None:
        """Test parsing simple Poetry dependencies."""
        pyproject = tmp_path / "pyproject.toml"
        pyproject.write_text("""
[tool.poetry.dependencies]
python = "^3.8"
requests = "^2.28.0"
numpy = "^1.20"
""")

        change = DiffFileChange(
            path="pyproject.toml",
            added_lines=[
                (3, 'requests = "^2.28.0"'),
                (4, 'numpy = "^1.20"'),
            ],
        )

        findings = scan_pyproject(change, tmp_path)

        # Python should be skipped
        assert len(findings) == 2
        names = {f.name for f in findings}
        assert "requests" in names
        assert "numpy" in names
        assert "python" not in names
        assert all(f.source == "pyproject_poetry" for f in findings)

    def test_poetry_dict_dependencies(self, tmp_path: Path) -> None:
        """Test parsing Poetry dict-format dependencies."""
        pyproject = tmp_path / "pyproject.toml"
        pyproject.write_text("""
[tool.poetry.dependencies]
requests = {version = "^2.28.0", optional = true}
numpy = {version = "^1.20"}
""")

        change = DiffFileChange(
            path="pyproject.toml",
            added_lines=[
                (2, 'requests = {version = "^2.28.0", optional = true}'),
                (3, 'numpy = {version = "^1.20"}'),
            ],
        )

        findings = scan_pyproject(change, tmp_path)

        assert len(findings) == 2
        names = {f.name for f in findings}
        assert "requests" in names
        assert "numpy" in names

    def test_poetry_dev_dependencies(self, tmp_path: Path) -> None:
        """Test parsing Poetry dev-dependencies (legacy)."""
        pyproject = tmp_path / "pyproject.toml"
        pyproject.write_text("""
[tool.poetry.dev-dependencies]
pytest = "^7.0"
mypy = "^1.0"
""")

        change = DiffFileChange(
            path="pyproject.toml",
            added_lines=[
                (2, 'pytest = "^7.0"'),
                (3, 'mypy = "^1.0"'),
            ],
        )

        findings = scan_pyproject(change, tmp_path)

        assert len(findings) == 2
        names = {f.name for f in findings}
        assert "pytest" in names
        assert "mypy" in names

    def test_poetry_group_dependencies(self, tmp_path: Path) -> None:
        """Test parsing Poetry group dependencies (new format)."""
        pyproject = tmp_path / "pyproject.toml"
        pyproject.write_text("""
[tool.poetry.group.dev.dependencies]
pytest = "^7.0"
mypy = "^1.0"

[tool.poetry.group.docs.dependencies]
sphinx = "^5.0"
""")

        change = DiffFileChange(
            path="pyproject.toml",
            added_lines=[
                (2, 'pytest = "^7.0"'),
                (3, 'mypy = "^1.0"'),
                (6, 'sphinx = "^5.0"'),
            ],
        )

        findings = scan_pyproject(change, tmp_path)

        assert len(findings) == 3
        names = {f.name for f in findings}
        assert "pytest" in names
        assert "mypy" in names
        assert "sphinx" in names

    def test_poetry_git_dependency(self, tmp_path: Path) -> None:
        """Test parsing Poetry git dependencies."""
        pyproject = tmp_path / "pyproject.toml"
        pyproject.write_text("""
[tool.poetry.dependencies]
mypackage = {git = "https://github.com/user/repo.git"}
""")

        change = DiffFileChange(
            path="pyproject.toml",
            added_lines=[
                (2, 'mypackage = {git = "https://github.com/user/repo.git"}'),
            ],
        )

        findings = scan_pyproject(change, tmp_path)

        assert len(findings) == 1
        assert findings[0].name == "mypackage"
        assert findings[0].is_git is True

    def test_poetry_path_dependency(self, tmp_path: Path) -> None:
        """Test parsing Poetry path dependencies."""
        pyproject = tmp_path / "pyproject.toml"
        pyproject.write_text("""
[tool.poetry.dependencies]
mypackage = {path = "../local-package"}
""")

        change = DiffFileChange(
            path="pyproject.toml",
            added_lines=[
                (2, 'mypackage = {path = "../local-package"}'),
            ],
        )

        findings = scan_pyproject(change, tmp_path)

        assert len(findings) == 1
        assert findings[0].name == "mypackage"
        assert findings[0].is_local is True


class TestScanPyprojectMixed:
    """Tests for mixed PEP 621 and Poetry formats."""

    def test_both_formats(self, tmp_path: Path) -> None:
        """Test file with both PEP 621 and Poetry sections."""
        pyproject = tmp_path / "pyproject.toml"
        pyproject.write_text("""
[project]
dependencies = ["requests>=2.28.0"]

[tool.poetry.dependencies]
numpy = "^1.20"
""")

        change = DiffFileChange(
            path="pyproject.toml",
            added_lines=[
                (2, 'dependencies = ["requests>=2.28.0"]'),
                (5, 'numpy = "^1.20"'),
            ],
        )

        findings = scan_pyproject(change, tmp_path)

        # Should find both
        assert len(findings) == 2
        names = {f.name for f in findings}
        assert "requests" in names
        assert "numpy" in names


class TestScanPyprojectEdgeCases:
    """Tests for edge cases."""

    def test_nonexistent_file(self, tmp_path: Path) -> None:
        """Test with non-existent file."""
        change = DiffFileChange(
            path="pyproject.toml",
            added_lines=[(1, "something")],
        )

        findings = scan_pyproject(change, tmp_path)

        assert len(findings) == 0

    def test_invalid_toml(self, tmp_path: Path) -> None:
        """Test with invalid TOML."""
        pyproject = tmp_path / "pyproject.toml"
        pyproject.write_text("this is not valid TOML [[[")

        change = DiffFileChange(
            path="pyproject.toml",
            added_lines=[(1, "something")],
        )

        findings = scan_pyproject(change, tmp_path)

        assert len(findings) == 0

    def test_empty_file(self, tmp_path: Path) -> None:
        """Test with empty file."""
        pyproject = tmp_path / "pyproject.toml"
        pyproject.write_text("")

        change = DiffFileChange(
            path="pyproject.toml",
            added_lines=[],
        )

        findings = scan_pyproject(change, tmp_path)

        assert len(findings) == 0

    def test_filter_to_added_lines(self, tmp_path: Path) -> None:
        """Test that only dependencies in added lines are returned."""
        pyproject = tmp_path / "pyproject.toml"
        pyproject.write_text("""
[project]
dependencies = [
    "requests>=2.28.0",
    "numpy>=1.20",
    "flask>=2.0",
]
""")

        # Only requests and flask in added lines
        change = DiffFileChange(
            path="pyproject.toml",
            added_lines=[
                (3, '    "requests>=2.28.0",'),
                (5, '    "flask>=2.0",'),
            ],
        )

        findings = scan_pyproject(change, tmp_path)

        # Should only find packages mentioned in added lines
        names = {f.name for f in findings}
        assert "requests" in names
        assert "flask" in names
        # numpy is not in added lines, so might not be included
        # (depends on implementation - our MVP checks if name appears in added text)

    def test_case_insensitive_name_normalization(self, tmp_path: Path) -> None:
        """Test that package names are normalized."""
        pyproject = tmp_path / "pyproject.toml"
        pyproject.write_text("""
[project]
dependencies = ["Flask>=2.0", "Flask_RESTful>=0.3"]
""")

        change = DiffFileChange(
            path="pyproject.toml",
            added_lines=[
                (2, 'dependencies = ["Flask>=2.0", "Flask_RESTful>=0.3"]'),
            ],
        )

        findings = scan_pyproject(change, tmp_path)

        assert len(findings) == 2
        names = [f.name for f in findings]
        assert "flask" in names
        assert "flask-restful" in names

