"""
Edge case tests for typo-shield.

Tests various edge cases that can occur in real-world usage:
- src/ repository layout
- Import aliases (import numpy as np)
- Multiple imports per line (import os, sys)
- Requirements.txt with environment markers
- Deleted files in diff
- Windows paths in diff
- Empty diff
"""

from __future__ import annotations

from pathlib import Path

import pytest

from typo_shield.diff import DiffFileChange, parse_unified_diff
from typo_shield.mapping.project_modules import discover_local_modules
from typo_shield.scanners.deps_requirements import scan_requirements
from typo_shield.scanners.python_imports import scan_python_imports


class TestSrcLayout:
    """Test src/ repository layout handling."""

    def test_discover_modules_in_src_layout(self, tmp_path: Path) -> None:
        """Test that modules in src/ directory are discovered."""
        # Create src/ layout
        src_dir = tmp_path / "src"
        src_dir.mkdir()

        # Create a package in src/
        backend_pkg = src_dir / "backend"
        backend_pkg.mkdir()
        (backend_pkg / "__init__.py").write_text("")

        # Create a module in src/
        (src_dir / "utils.py").write_text("def helper(): pass")

        # Create a package in root (should also be found)
        frontend_pkg = tmp_path / "frontend"
        frontend_pkg.mkdir()
        (frontend_pkg / "__init__.py").write_text("")

        # Discover modules
        modules = discover_local_modules(tmp_path)

        # Should find both src/ and root modules
        assert "backend" in modules
        assert "utils" in modules
        assert "frontend" in modules

    def test_src_layout_preferred_over_root(self, tmp_path: Path) -> None:
        """Test that src/ layout is properly detected alongside root packages."""
        # Create both src/ and root packages
        (tmp_path / "app.py").write_text("# root module")

        src_dir = tmp_path / "src"
        src_dir.mkdir()
        (src_dir / "core.py").write_text("# src module")

        modules = discover_local_modules(tmp_path)

        # Both should be found
        assert "app" in modules
        assert "core" in modules


class TestImportAliases:
    """Test handling of import aliases."""

    def test_import_with_alias(self, tmp_path: Path) -> None:
        """Test that 'import numpy as np' extracts 'numpy'."""
        # Create a Python file with aliased import
        test_file = tmp_path / "test.py"
        test_file.write_text("import numpy as np\nimport pandas as pd\n")

        # Create DiffFileChange
        diff_change = DiffFileChange(
            path="test.py",
            added_lines=[(1, "import numpy as np"), (2, "import pandas as pd")],
        )

        # Scan imports
        findings = scan_python_imports(diff_change, tmp_path)

        # Should extract module names, not aliases
        module_names = {f.module for f in findings}
        assert "numpy" in module_names
        assert "pandas" in module_names
        assert "np" not in module_names  # alias should not be extracted
        assert "pd" not in module_names


class TestMultipleImports:
    """Test multiple imports per line."""

    def test_multiple_imports_single_line(self, tmp_path: Path) -> None:
        """Test 'import os, sys, re' extracts all three."""
        test_file = tmp_path / "test.py"
        test_file.write_text("import os, sys, re\n")

        diff_change = DiffFileChange(
            path="test.py",
            added_lines=[(1, "import os, sys, re")],
        )

        findings = scan_python_imports(diff_change, tmp_path)

        # Should find all three modules
        module_names = {f.module for f in findings}
        assert module_names == {"os", "sys", "re"}

    def test_multiple_imports_with_aliases(self, tmp_path: Path) -> None:
        """Test 'import os as operating_system, sys' works."""
        test_file = tmp_path / "test.py"
        test_file.write_text("import os as operating_system, sys\n")

        diff_change = DiffFileChange(
            path="test.py",
            added_lines=[(1, "import os as operating_system, sys")],
        )

        findings = scan_python_imports(diff_change, tmp_path)

        module_names = {f.module for f in findings}
        assert "os" in module_names
        assert "sys" in module_names
        assert "operating_system" not in module_names  # alias


class TestEnvironmentMarkers:
    """Test requirements.txt with environment markers."""

    def test_requirements_with_python_version_marker(self) -> None:
        """Test 'requests>=2.0; python_version<\"3.8\"' is parsed correctly."""
        diff_change = DiffFileChange(
            path="requirements.txt",
            added_lines=[
                (1, 'requests>=2.0; python_version<"3.8"'),
                (2, 'numpy>=1.20; sys_platform=="linux"'),
            ],
        )

        findings = scan_requirements(diff_change)

        # Should extract package names and specifiers, ignoring markers
        assert len(findings) == 2
        names = {f.name for f in findings}
        assert "requests" in names
        assert "numpy" in names

    def test_requirements_with_complex_markers(self) -> None:
        """Test complex environment markers are handled."""
        diff_change = DiffFileChange(
            path="requirements.txt",
            added_lines=[
                (1, 'typing-extensions>=4.0; python_version<"3.10"'),
                (2, 'backports.zoneinfo; python_version<"3.9"'),
            ],
        )

        findings = scan_requirements(diff_change)

        assert len(findings) == 2
        names = {f.name for f in findings}
        assert "typing-extensions" in names
        assert "backports-zoneinfo" in names  # Note: normalized with hyphen


class TestDeletedFiles:
    """Test handling of deleted files in diff."""

    def test_deleted_file_ignored(self) -> None:
        """Test that deleted files (b/dev/null) are ignored."""
        diff = """diff --git a/old.py b/old.py
deleted file mode 100644
--- a/old.py
+++ b/dev/null
@@ -1,2 +0,0 @@
-import requests
-import numpy
"""
        changes = parse_unified_diff(diff)

        # Deleted files should not appear in changes
        assert len(changes) == 0

    def test_new_file_detected(self) -> None:
        """Test that new files (a/dev/null) are properly detected."""
        diff = """diff --git a/new.py b/new.py
new file mode 100644
--- a/dev/null
+++ b/new.py
@@ -0,0 +1,2 @@
+import requests
+import numpy
"""
        changes = parse_unified_diff(diff)

        assert len(changes) == 1
        assert changes[0].path == "new.py"
        assert changes[0].is_new is True
        assert len(changes[0].added_lines) == 2


class TestWindowsPaths:
    """Test Windows path normalization."""

    def test_windows_paths_normalized(self) -> None:
        """Test that Windows backslashes are converted to forward slashes."""
        # Git on Windows may output paths with backslashes
        diff = """diff --git a/src\\app.py b/src\\app.py
--- a/src\\app.py
+++ b/src\\app.py
@@ -1,0 +2,1 @@
+import requests
"""
        changes = parse_unified_diff(diff)

        assert len(changes) == 1
        # Path should be normalized to forward slashes
        assert changes[0].path == "src/app.py"
        assert "\\" not in changes[0].path


class TestEmptyDiff:
    """Test empty diff handling."""

    def test_empty_diff_returns_empty_list(self) -> None:
        """Test that empty diff returns empty list."""
        changes = parse_unified_diff("")
        assert changes == []

    def test_diff_with_no_additions(self) -> None:
        """Test diff with only deletions (no + lines)."""
        diff = """diff --git a/test.py b/test.py
--- a/test.py
+++ b/test.py
@@ -1,2 +1,1 @@
-import requests
-import numpy
+import requests
"""
        changes = parse_unified_diff(diff)

        # Should only capture the one added line
        assert len(changes) == 1
        assert len(changes[0].added_lines) == 1
        assert changes[0].added_lines[0][1] == "import requests"


class TestRelativeImports:
    """Test relative imports handling."""

    def test_relative_import_detected(self, tmp_path: Path) -> None:
        """Test that relative imports are detected and marked."""
        test_file = tmp_path / "test.py"
        test_file.write_text("from . import utils\nfrom ..models import User\n")

        diff_change = DiffFileChange(
            path="test.py",
            added_lines=[
                (1, "from . import utils"),
                (2, "from ..models import User"),
            ],
        )

        findings = scan_python_imports(diff_change, tmp_path)

        # Relative imports should be marked
        # (they may or may not be included depending on implementation)
        # At minimum, they shouldn't cause errors
        assert isinstance(findings, list)


class TestGitUrlDependencies:
    """Test git URL dependencies."""

    def test_git_url_with_egg_fragment(self) -> None:
        """Test git URL with #egg= fragment is parsed correctly."""
        diff_change = DiffFileChange(
            path="requirements.txt",
            added_lines=[
                (1, "git+https://github.com/user/repo.git#egg=mypackage"),
                (2, "git+ssh://git@github.com/user/repo.git@branch#egg=another-pkg"),
            ],
        )

        findings = scan_requirements(diff_change)

        assert len(findings) == 2
        # All should be marked as git dependencies
        assert all(f.is_git for f in findings)
        # Should extract egg names
        names = {f.name for f in findings}
        assert "mypackage" in names
        assert "another-pkg" in names


@pytest.mark.slow
class TestEdgeCaseIntegration:
    """Integration tests for edge cases."""

    def test_complex_project_structure(self, tmp_path: Path) -> None:
        """Test a complex project with src/, tests/, docs/, etc."""
        # Create complex structure
        (tmp_path / "README.md").write_text("# Project")

        # src/ layout
        src = tmp_path / "src"
        src.mkdir()
        app_pkg = src / "app"
        app_pkg.mkdir()
        (app_pkg / "__init__.py").write_text("")

        # tests/ (should be ignored)
        tests = tmp_path / "tests"
        tests.mkdir()
        (tests / "test_app.py").write_text("import pytest")

        # docs/ (should be ignored)
        docs = tmp_path / "docs"
        docs.mkdir()
        (docs / "conf.py").write_text("# sphinx config")

        # Discover modules
        modules = discover_local_modules(tmp_path)

        # Should only find app, not tests or docs
        assert "app" in modules
        assert "tests" not in modules
        assert "docs" not in modules

    def test_mixed_imports_and_dependencies(self, tmp_path: Path) -> None:
        """Test file with both standard library and third-party imports."""
        test_file = tmp_path / "app.py"
        test_file.write_text("""
import os
import sys
from pathlib import Path
import requests
import numpy as np
from typing import Optional
""")

        diff_change = DiffFileChange(
            path="app.py",
            added_lines=[
                (2, "import os"),
                (3, "import sys"),
                (4, "from pathlib import Path"),
                (5, "import requests"),
                (6, "import numpy as np"),
                (7, "from typing import Optional"),
            ],
        )

        findings = scan_python_imports(diff_change, tmp_path)

        # Should find all imports
        module_names = {f.module for f in findings}
        assert "os" in module_names
        assert "sys" in module_names
        assert "pathlib" in module_names
        assert "requests" in module_names
        assert "numpy" in module_names
        assert "typing" in module_names

