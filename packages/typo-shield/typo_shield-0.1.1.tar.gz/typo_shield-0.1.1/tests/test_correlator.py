"""Tests for import-dependency correlator."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

from typo_shield.correlator import (
    analyze_new_deps,
    collect_declared_deps,
    correlate_imports_and_deps,
)
from typo_shield.scanners.deps_requirements import DependencyFinding
from typo_shield.scanners.python_imports import PythonImportFinding


class TestCorrelateImportsAndDeps:
    """Tests for correlate_imports_and_deps()."""

    @patch("typo_shield.correlator.is_stdlib")
    @patch("typo_shield.correlator.is_local_module")
    def test_stdlib_import(
        self, mock_is_local: any, mock_is_stdlib: any, tmp_path: Path
    ) -> None:
        """Test that stdlib imports are marked as INFO."""
        mock_is_stdlib.return_value = True
        mock_is_local.return_value = False

        imports = [
            PythonImportFinding(
                file="main.py",
                module="os",
                kind="import",
                lineno=1,
            )
        ]

        findings = correlate_imports_and_deps(imports, set(), tmp_path)

        assert len(findings) == 1
        assert findings[0].kind == "stdlib_import"
        assert findings[0].level == "INFO"
        assert findings[0].name == "os"

    @patch("typo_shield.correlator.is_stdlib")
    @patch("typo_shield.correlator.is_local_module")
    def test_local_import(
        self, mock_is_local: any, mock_is_stdlib: any, tmp_path: Path
    ) -> None:
        """Test that local imports are marked as INFO."""
        mock_is_stdlib.return_value = False
        mock_is_local.return_value = True

        imports = [
            PythonImportFinding(
                file="main.py",
                module="mymodule",
                kind="import",
                lineno=1,
            )
        ]

        findings = correlate_imports_and_deps(imports, set(), tmp_path)

        assert len(findings) == 1
        assert findings[0].kind == "local_import"
        assert findings[0].level == "INFO"
        assert findings[0].name == "mymodule"

    @patch("typo_shield.correlator.is_stdlib")
    @patch("typo_shield.correlator.is_local_module")
    def test_declared_third_party_import(
        self, mock_is_local: any, mock_is_stdlib: any, tmp_path: Path
    ) -> None:
        """Test that declared third-party imports don't generate warnings."""
        mock_is_stdlib.return_value = False
        mock_is_local.return_value = False

        imports = [
            PythonImportFinding(
                file="main.py",
                module="requests",
                kind="import",
                lineno=1,
            )
        ]

        declared_deps = {"requests"}

        findings = correlate_imports_and_deps(imports, declared_deps, tmp_path)

        # Should have no findings (declared properly)
        assert len(findings) == 0

    @patch("typo_shield.correlator.is_stdlib")
    @patch("typo_shield.correlator.is_local_module")
    def test_missing_dependency(
        self, mock_is_local: any, mock_is_stdlib: any, tmp_path: Path
    ) -> None:
        """Test that undeclared third-party imports generate WARN."""
        mock_is_stdlib.return_value = False
        mock_is_local.return_value = False

        imports = [
            PythonImportFinding(
                file="main.py",
                module="requests",
                kind="import",
                lineno=1,
            )
        ]

        # Empty declared deps
        declared_deps = set()

        findings = correlate_imports_and_deps(imports, declared_deps, tmp_path)

        assert len(findings) == 1
        assert findings[0].kind == "missing_dep"
        assert findings[0].level == "WARN"
        assert findings[0].code == "TS101"
        assert findings[0].name == "requests"
        assert "not found in declared dependencies" in findings[0].message

    @patch("typo_shield.correlator.is_stdlib")
    @patch("typo_shield.correlator.is_local_module")
    def test_module_to_dist_mapping(
        self, mock_is_local: any, mock_is_stdlib: any, tmp_path: Path
    ) -> None:
        """Test that module names are mapped to distribution names."""
        mock_is_stdlib.return_value = False
        mock_is_local.return_value = False

        imports = [
            PythonImportFinding(
                file="main.py",
                module="PIL",  # Module name
                kind="import",
                lineno=1,
            )
        ]

        # Declared with distribution name
        declared_deps = {"Pillow"}

        findings = correlate_imports_and_deps(imports, declared_deps, tmp_path)

        # Should have no findings (PIL -> Pillow mapping works)
        assert len(findings) == 0

    @patch("typo_shield.correlator.is_stdlib")
    @patch("typo_shield.correlator.is_local_module")
    def test_case_insensitive_matching(
        self, mock_is_local: any, mock_is_stdlib: any, tmp_path: Path
    ) -> None:
        """Test that package name matching is case-insensitive."""
        mock_is_stdlib.return_value = False
        mock_is_local.return_value = False

        imports = [
            PythonImportFinding(
                file="main.py",
                module="flask",
                kind="import",
                lineno=1,
            )
        ]

        # Declared with different case
        declared_deps = {"Flask"}

        findings = correlate_imports_and_deps(imports, declared_deps, tmp_path)

        # Should have no findings (case-insensitive match)
        assert len(findings) == 0

    @patch("typo_shield.correlator.is_stdlib")
    @patch("typo_shield.correlator.is_local_module")
    def test_relative_import(
        self, mock_is_local: any, mock_is_stdlib: any, tmp_path: Path
    ) -> None:
        """Test that relative imports are marked as INFO."""
        imports = [
            PythonImportFinding(
                file="main.py",
                module="",
                kind="from",
                lineno=1,
                raw="from . import foo",
                is_relative=True,
            )
        ]

        findings = correlate_imports_and_deps(imports, set(), tmp_path)

        assert len(findings) == 1
        assert findings[0].kind == "relative_import"
        assert findings[0].level == "INFO"

    @patch("typo_shield.correlator.is_stdlib")
    @patch("typo_shield.correlator.is_local_module")
    def test_multiple_imports_mixed(
        self, mock_is_local: any, mock_is_stdlib: any, tmp_path: Path
    ) -> None:
        """Test multiple imports with mixed scenarios."""
        def stdlib_side_effect(module: str) -> bool:
            return module == "os"

        def local_side_effect(module: str, repo: Path) -> bool:
            return module == "mymodule"

        mock_is_stdlib.side_effect = stdlib_side_effect
        mock_is_local.side_effect = local_side_effect

        imports = [
            PythonImportFinding(file="main.py", module="os", kind="import", lineno=1),
            PythonImportFinding(file="main.py", module="mymodule", kind="import", lineno=2),
            PythonImportFinding(file="main.py", module="requests", kind="import", lineno=3),
            PythonImportFinding(file="main.py", module="numpy", kind="import", lineno=4),
        ]

        declared_deps = {"requests"}

        findings = correlate_imports_and_deps(imports, declared_deps, tmp_path)

        # Should have 3 findings: os (INFO), mymodule (INFO), numpy (WARN)
        assert len(findings) == 3

        # Check os (stdlib)
        os_finding = next(f for f in findings if f.name == "os")
        assert os_finding.kind == "stdlib_import"
        assert os_finding.level == "INFO"

        # Check mymodule (local)
        local_finding = next(f for f in findings if f.name == "mymodule")
        assert local_finding.kind == "local_import"
        assert local_finding.level == "INFO"

        # Check numpy (missing)
        numpy_finding = next(f for f in findings if f.name == "numpy")
        assert numpy_finding.kind == "missing_dep"
        assert numpy_finding.level == "WARN"

    @patch("typo_shield.correlator.is_stdlib")
    @patch("typo_shield.correlator.is_local_module")
    def test_empty_imports(
        self, mock_is_local: any, mock_is_stdlib: any, tmp_path: Path
    ) -> None:
        """Test with no imports."""
        findings = correlate_imports_and_deps([], set(), tmp_path)
        assert len(findings) == 0


class TestCollectDeclaredDeps:
    """Tests for collect_declared_deps()."""

    def test_collect_basic(self) -> None:
        """Test collecting basic dependencies."""
        deps = [
            DependencyFinding(
                file="requirements.txt",
                name="requests",
                specifier=">=2.28.0",
                source="requirements.txt",
                lineno=1,
            ),
            DependencyFinding(
                file="requirements.txt",
                name="numpy",
                specifier="==1.24.0",
                source="requirements.txt",
                lineno=2,
            ),
        ]

        result = collect_declared_deps(deps)

        assert result == {"requests", "numpy"}

    def test_collect_normalized(self) -> None:
        """Test that names are normalized."""
        deps = [
            DependencyFinding(
                file="requirements.txt",
                name="Flask",
                specifier=None,
                source="requirements.txt",
                lineno=1,
            ),
            DependencyFinding(
                file="requirements.txt",
                name="scikit_learn",
                specifier=None,
                source="requirements.txt",
                lineno=2,
            ),
        ]

        result = collect_declared_deps(deps)

        # Should be normalized (lowercase, _ -> -)
        assert "flask" in result
        assert "scikit-learn" in result

    def test_collect_empty(self) -> None:
        """Test with empty list."""
        result = collect_declared_deps([])
        assert result == set()

    def test_collect_duplicates(self) -> None:
        """Test that duplicates are handled."""
        deps = [
            DependencyFinding(
                file="requirements.txt",
                name="requests",
                specifier=">=2.28.0",
                source="requirements.txt",
                lineno=1,
            ),
            DependencyFinding(
                file="pyproject.toml",
                name="requests",
                specifier=">=2.28.0",
                source="pyproject.toml",
                lineno=None,
            ),
        ]

        result = collect_declared_deps(deps)

        # Should have only one entry
        assert result == {"requests"}


class TestAnalyzeNewDeps:
    """Tests for analyze_new_deps()."""

    def test_analyze_basic_dep(self) -> None:
        """Test analyzing a basic new dependency."""
        deps = [
            DependencyFinding(
                file="requirements.txt",
                name="requests",
                specifier=">=2.28.0",
                source="requirements.txt",
                lineno=1,
            )
        ]

        findings = analyze_new_deps(deps)

        assert len(findings) == 1
        assert findings[0].kind == "new_dep"
        assert findings[0].level == "INFO"
        assert findings[0].name == "requests"
        assert "New dependency added" in findings[0].message
        assert ">=2.28.0" in findings[0].message

    def test_analyze_git_dep(self) -> None:
        """Test analyzing a Git dependency."""
        deps = [
            DependencyFinding(
                file="requirements.txt",
                name="mypackage",
                specifier=None,
                source="requirements.txt",
                lineno=1,
                is_git=True,
            )
        ]

        findings = analyze_new_deps(deps)

        assert len(findings) == 1
        assert "(Git source)" in findings[0].message

    def test_analyze_local_dep(self) -> None:
        """Test analyzing a local path dependency."""
        deps = [
            DependencyFinding(
                file="requirements.txt",
                name="mylib",
                specifier=None,
                source="requirements.txt",
                lineno=1,
                is_local=True,
            )
        ]

        findings = analyze_new_deps(deps)

        assert len(findings) == 1
        assert "(local path)" in findings[0].message

    def test_analyze_empty(self) -> None:
        """Test with no new dependencies."""
        findings = analyze_new_deps([])
        assert len(findings) == 0

    def test_analyze_multiple_deps(self) -> None:
        """Test analyzing multiple dependencies."""
        deps = [
            DependencyFinding(
                file="requirements.txt",
                name="requests",
                specifier=">=2.28.0",
                source="requirements.txt",
                lineno=1,
            ),
            DependencyFinding(
                file="requirements.txt",
                name="numpy",
                specifier="==1.24.0",
                source="requirements.txt",
                lineno=2,
            ),
        ]

        findings = analyze_new_deps(deps)

        assert len(findings) == 2
        assert all(f.level == "INFO" for f in findings)

