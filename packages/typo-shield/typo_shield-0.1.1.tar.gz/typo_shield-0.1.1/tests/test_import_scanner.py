"""Tests for Python import scanner."""

from __future__ import annotations

from pathlib import Path

from typo_shield.diff import DiffFileChange
from typo_shield.scanners.python_imports import (
    PythonImportFinding,
    deduplicate_imports,
    filter_new_imports,
    scan_python_imports,
)


class TestScanPythonImportsAST:
    """Tests for AST-based import scanning."""

    def test_simple_import(self, tmp_path: Path) -> None:
        """Test scanning simple import statement."""
        # Create test file
        test_file = tmp_path / "test.py"
        test_file.write_text("import requests\n")

        change = DiffFileChange(
            path="test.py",
            added_lines=[(1, "import requests")],
        )

        findings = scan_python_imports(change, tmp_path)

        assert len(findings) >= 1
        assert any(f.module == "requests" and f.kind == "import" for f in findings)

    def test_from_import(self, tmp_path: Path) -> None:
        """Test scanning from...import statement."""
        test_file = tmp_path / "test.py"
        test_file.write_text("from PIL import Image\n")

        change = DiffFileChange(
            path="test.py",
            added_lines=[(1, "from PIL import Image")],
        )

        findings = scan_python_imports(change, tmp_path)

        assert len(findings) >= 1
        assert any(f.module == "PIL" and f.kind == "from" for f in findings)

    def test_multiple_imports(self, tmp_path: Path) -> None:
        """Test scanning multiple imports in one line."""
        test_file = tmp_path / "test.py"
        test_file.write_text("import os, sys, json\n")

        change = DiffFileChange(
            path="test.py",
            added_lines=[(1, "import os, sys, json")],
        )

        findings = scan_python_imports(change, tmp_path)

        modules = {f.module for f in findings}
        assert "os" in modules
        assert "sys" in modules
        assert "json" in modules

    def test_import_with_alias(self, tmp_path: Path) -> None:
        """Test scanning import with alias."""
        test_file = tmp_path / "test.py"
        test_file.write_text("import numpy as np\n")

        change = DiffFileChange(
            path="test.py",
            added_lines=[(1, "import numpy as np")],
        )

        findings = scan_python_imports(change, tmp_path)

        assert len(findings) >= 1
        assert any(f.module == "numpy" for f in findings)

    def test_dotted_import(self, tmp_path: Path) -> None:
        """Test that only top-level module is extracted from dotted imports."""
        test_file = tmp_path / "test.py"
        test_file.write_text("import requests.auth.oauth\n")

        change = DiffFileChange(
            path="test.py",
            added_lines=[(1, "import requests.auth.oauth")],
        )

        findings = scan_python_imports(change, tmp_path)

        assert len(findings) >= 1
        # Should extract only 'requests', not 'requests.auth.oauth'
        assert any(f.module == "requests" for f in findings)

    def test_from_dotted_import(self, tmp_path: Path) -> None:
        """Test from statement with dotted module."""
        test_file = tmp_path / "test.py"
        test_file.write_text("from requests.auth import OAuth2\n")

        change = DiffFileChange(
            path="test.py",
            added_lines=[(1, "from requests.auth import OAuth2")],
        )

        findings = scan_python_imports(change, tmp_path)

        assert len(findings) >= 1
        # Should extract only 'requests'
        assert any(f.module == "requests" for f in findings)

    def test_relative_import_skipped(self, tmp_path: Path) -> None:
        """Test that relative imports are marked as relative."""
        test_file = tmp_path / "test.py"
        test_file.write_text("from . import utils\nfrom .. import config\n")

        change = DiffFileChange(
            path="test.py",
            added_lines=[(1, "from . import utils"), (2, "from .. import config")],
        )

        findings = scan_python_imports(change, tmp_path)

        # Relative imports should be marked
        [f for f in findings if f.is_relative]
        # Should have minimal or no findings, as relative imports are internal
        assert all(f.is_relative for f in findings) or len(findings) == 0

    def test_future_import_skipped(self, tmp_path: Path) -> None:
        """Test that __future__ imports are skipped."""
        test_file = tmp_path / "test.py"
        test_file.write_text(
            "from __future__ import annotations\nimport requests\n"
        )

        change = DiffFileChange(
            path="test.py",
            added_lines=[
                (1, "from __future__ import annotations"),
                (2, "import requests"),
            ],
        )

        findings = scan_python_imports(change, tmp_path)

        # __future__ should be skipped
        assert all(f.module != "__future__" for f in findings)
        # But requests should be found
        assert any(f.module == "requests" for f in findings)

    def test_complex_file(self, tmp_path: Path) -> None:
        """Test scanning file with multiple types of imports."""
        test_file = tmp_path / "app.py"
        test_file.write_text("""
from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Optional
import requests
from PIL import Image
import numpy as np
""")

        change = DiffFileChange(
            path="app.py",
            added_lines=[
                (3, "import os"),
                (4, "import sys"),
                (5, "from pathlib import Path"),
                (7, "import requests"),
                (8, "from PIL import Image"),
                (9, "import numpy as np"),
            ],
        )

        findings = scan_python_imports(change, tmp_path)

        modules = {f.module for f in findings}
        # Standard library
        assert "os" in modules
        assert "sys" in modules
        assert "pathlib" in modules
        assert "typing" in modules
        # Third-party
        assert "requests" in modules
        assert "PIL" in modules
        assert "numpy" in modules
        # __future__ should be skipped
        assert "__future__" not in modules


class TestScanPythonImportsRegex:
    """Tests for regex fallback scanning."""

    def test_regex_fallback_nonexistent_file(self, tmp_path: Path) -> None:
        """Test regex fallback when file doesn't exist."""
        change = DiffFileChange(
            path="nonexistent.py",
            added_lines=[
                (1, "import requests"),
                (2, "from PIL import Image"),
            ],
        )

        findings = scan_python_imports(change, tmp_path)

        assert len(findings) == 2
        modules = {f.module for f in findings}
        assert "requests" in modules
        assert "PIL" in modules

    def test_regex_simple_import(self, tmp_path: Path) -> None:
        """Test regex parsing of simple import."""
        change = DiffFileChange(
            path="test.py",
            added_lines=[(1, "import requests")],
        )

        findings = scan_python_imports(change, tmp_path)

        assert len(findings) == 1
        assert findings[0].module == "requests"
        assert findings[0].kind == "import"

    def test_regex_from_import(self, tmp_path: Path) -> None:
        """Test regex parsing of from import."""
        change = DiffFileChange(
            path="test.py",
            added_lines=[(1, "from PIL import Image")],
        )

        findings = scan_python_imports(change, tmp_path)

        assert len(findings) == 1
        assert findings[0].module == "PIL"
        assert findings[0].kind == "from"

    def test_regex_with_indentation(self, tmp_path: Path) -> None:
        """Test regex handles indented imports."""
        change = DiffFileChange(
            path="test.py",
            added_lines=[
                (1, "    import requests"),
                (2, "        from PIL import Image"),
            ],
        )

        findings = scan_python_imports(change, tmp_path)

        assert len(findings) == 2
        modules = {f.module for f in findings}
        assert "requests" in modules
        assert "PIL" in modules

    def test_regex_skips_relative_imports(self, tmp_path: Path) -> None:
        """Test regex skips relative imports."""
        change = DiffFileChange(
            path="test.py",
            added_lines=[
                (1, "from . import utils"),
                (2, "from .. import config"),
                (3, "import requests"),
            ],
        )

        findings = scan_python_imports(change, tmp_path)

        # Should only find non-relative import
        assert len(findings) == 1
        assert findings[0].module == "requests"

    def test_regex_skips_future(self, tmp_path: Path) -> None:
        """Test regex skips __future__ imports."""
        change = DiffFileChange(
            path="test.py",
            added_lines=[
                (1, "from __future__ import annotations"),
                (2, "import requests"),
            ],
        )

        findings = scan_python_imports(change, tmp_path)

        # Should skip __future__
        assert len(findings) == 1
        assert findings[0].module == "requests"


class TestFilterNewImports:
    """Tests for filter_new_imports()."""

    def test_filter_to_added_lines(self) -> None:
        """Test filtering imports to only added lines."""
        findings = [
            PythonImportFinding(file="test.py", module="os", kind="import", lineno=1),
            PythonImportFinding(file="test.py", module="sys", kind="import", lineno=2),
            PythonImportFinding(file="test.py", module="requests", kind="import", lineno=5),
        ]

        change = DiffFileChange(
            path="test.py",
            added_lines=[(2, "import sys"), (5, "import requests")],
        )

        filtered = filter_new_imports(findings, change)

        assert len(filtered) == 2
        modules = {f.module for f in filtered}
        assert "sys" in modules
        assert "requests" in modules
        assert "os" not in modules  # Line 1 not in added lines

    def test_filter_none_lineno(self) -> None:
        """Test that imports with None lineno are kept."""
        findings = [
            PythonImportFinding(file="test.py", module="requests", kind="import", lineno=None),
        ]

        change = DiffFileChange(
            path="test.py",
            added_lines=[(1, "import os")],
        )

        filtered = filter_new_imports(findings, change)

        # None lineno should be kept (can't filter)
        assert len(filtered) == 1


class TestDeduplicateImports:
    """Tests for deduplicate_imports()."""

    def test_deduplicate_same_module(self) -> None:
        """Test deduplication of same module imported multiple times."""
        findings = [
            PythonImportFinding(file="test.py", module="requests", kind="import", lineno=1),
            PythonImportFinding(file="test.py", module="requests", kind="from", lineno=5),
            PythonImportFinding(file="test.py", module="numpy", kind="import", lineno=10),
        ]

        dedup = deduplicate_imports(findings)

        assert len(dedup) == 2
        modules = [f.module for f in dedup]
        assert modules.count("requests") == 1
        assert modules.count("numpy") == 1

    def test_deduplicate_different_files(self) -> None:
        """Test that same module in different files is NOT deduplicated."""
        findings = [
            PythonImportFinding(file="file1.py", module="requests", kind="import", lineno=1),
            PythonImportFinding(file="file2.py", module="requests", kind="import", lineno=1),
        ]

        dedup = deduplicate_imports(findings)

        # Different files, both should be kept
        assert len(dedup) == 2

    def test_deduplicate_empty(self) -> None:
        """Test deduplication of empty list."""
        dedup = deduplicate_imports([])
        assert len(dedup) == 0

