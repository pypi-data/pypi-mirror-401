"""Tests for diff parser."""

from __future__ import annotations

from typo_shield.diff import (
    DiffFileChange,
    filter_files_by_extension,
    filter_files_by_pattern,
    parse_unified_diff,
)


class TestParseUnifiedDiff:
    """Tests for parse_unified_diff()."""

    def test_simple_addition(self) -> None:
        """Test parsing simple line addition."""
        diff = """diff --git a/test.py b/test.py
index abc123..def456 100644
--- a/test.py
+++ b/test.py
@@ -1,0 +2,2 @@
+import requests
+import numpy
"""
        changes = parse_unified_diff(diff)

        assert len(changes) == 1
        assert changes[0].path == "test.py"
        assert changes[0].is_new is False
        assert len(changes[0].added_lines) == 2
        assert changes[0].added_lines[0] == (2, "import requests")
        assert changes[0].added_lines[1] == (3, "import numpy")

    def test_new_file(self) -> None:
        """Test parsing new file creation."""
        diff = """diff --git a/new_file.py b/new_file.py
new file mode 100644
index 0000000..abc123
--- /dev/null
+++ b/new_file.py
@@ -0,0 +1,3 @@
+import os
+import sys
+print("hello")
"""
        changes = parse_unified_diff(diff)

        assert len(changes) == 1
        assert changes[0].path == "new_file.py"
        assert changes[0].is_new is True
        assert len(changes[0].added_lines) == 3
        assert changes[0].added_lines[0] == (1, "import os")
        assert changes[0].added_lines[1] == (2, "import sys")
        assert changes[0].added_lines[2] == (3, 'print("hello")')

    def test_multiple_files(self) -> None:
        """Test parsing diff with multiple files."""
        diff = """diff --git a/file1.py b/file1.py
--- a/file1.py
+++ b/file1.py
@@ -1,0 +2,1 @@
+import requests
diff --git a/file2.py b/file2.py
--- a/file2.py
+++ b/file2.py
@@ -5,0 +6,1 @@
+import numpy
"""
        changes = parse_unified_diff(diff)

        assert len(changes) == 2
        assert changes[0].path == "file1.py"
        assert changes[1].path == "file2.py"
        assert len(changes[0].added_lines) == 1
        assert len(changes[1].added_lines) == 1

    def test_multiple_hunks(self) -> None:
        """Test parsing multiple hunks in one file."""
        diff = """diff --git a/app.py b/app.py
--- a/app.py
+++ b/app.py
@@ -1,0 +2,1 @@
+import os
@@ -10,0 +12,2 @@
+import sys
+import json
"""
        changes = parse_unified_diff(diff)

        assert len(changes) == 1
        assert changes[0].path == "app.py"
        assert len(changes[0].added_lines) == 3
        assert changes[0].added_lines[0] == (2, "import os")
        assert changes[0].added_lines[1] == (12, "import sys")
        assert changes[0].added_lines[2] == (13, "import json")

    def test_deleted_file(self) -> None:
        """Test that deleted files are skipped."""
        diff = """diff --git a/deleted.py b/deleted.py
deleted file mode 100644
index abc123..0000000
--- a/deleted.py
+++ /dev/null
@@ -1,2 +0,0 @@
-import old_module
-print("deleted")
diff --git a/kept.py b/kept.py
--- a/kept.py
+++ b/kept.py
@@ -1,0 +2,1 @@
+import new_module
"""
        changes = parse_unified_diff(diff)

        # Only kept.py should be in results
        assert len(changes) == 1
        assert changes[0].path == "kept.py"

    def test_windows_paths(self) -> None:
        """Test normalization of Windows-style paths."""
        diff = r"""diff --git a/path\to\file.py b/path\to\file.py
--- a/path\to\file.py
+++ b/path\to\file.py
@@ -1,0 +2,1 @@
+import requests
"""
        changes = parse_unified_diff(diff)

        assert len(changes) == 1
        # Path should be normalized to forward slashes
        assert changes[0].path == "path/to/file.py"

    def test_empty_diff(self) -> None:
        """Test parsing empty diff."""
        changes = parse_unified_diff("")

        assert len(changes) == 0

    def test_no_additions(self) -> None:
        """Test diff with only deletions (no additions)."""
        diff = """diff --git a/test.py b/test.py
--- a/test.py
+++ b/test.py
@@ -2,1 +1,0 @@
-import old_module
"""
        changes = parse_unified_diff(diff)

        # File should be in results but with no added lines
        assert len(changes) == 1
        assert changes[0].path == "test.py"
        assert len(changes[0].added_lines) == 0

    def test_mixed_additions_and_deletions(self) -> None:
        """Test diff with both additions and deletions."""
        diff = """diff --git a/test.py b/test.py
--- a/test.py
+++ b/test.py
@@ -1,1 +1,2 @@
-import old_module
+import new_module
+import another_module
"""
        changes = parse_unified_diff(diff)

        assert len(changes) == 1
        # Only added lines should be captured
        assert len(changes[0].added_lines) == 2
        assert changes[0].added_lines[0] == (1, "import new_module")
        assert changes[0].added_lines[1] == (2, "import another_module")

    def test_hunk_without_line_count(self) -> None:
        """Test hunk header with implicit line count (single line)."""
        diff = """diff --git a/test.py b/test.py
--- a/test.py
+++ b/test.py
@@ -1 +2 @@
+import requests
"""
        changes = parse_unified_diff(diff)

        assert len(changes) == 1
        assert len(changes[0].added_lines) == 1
        assert changes[0].added_lines[0] == (2, "import requests")


class TestFilterFilesByExtension:
    """Tests for filter_files_by_extension()."""

    def test_filter_python_files(self) -> None:
        """Test filtering for Python files only."""
        changes = [
            DiffFileChange(path="app.py", added_lines=[(1, "import os")]),
            DiffFileChange(path="README.md", added_lines=[(1, "# Title")]),
            DiffFileChange(path="requirements.txt", added_lines=[(1, "requests")]),
        ]

        filtered = filter_files_by_extension(changes, {".py"})

        assert len(filtered) == 1
        assert filtered[0].path == "app.py"

    def test_filter_multiple_extensions(self) -> None:
        """Test filtering for multiple extensions."""
        changes = [
            DiffFileChange(path="app.py"),
            DiffFileChange(path="config.toml"),
            DiffFileChange(path="requirements.txt"),
            DiffFileChange(path="README.md"),
        ]

        filtered = filter_files_by_extension(changes, {".py", ".toml", ".txt"})

        assert len(filtered) == 3
        paths = {c.path for c in filtered}
        assert paths == {"app.py", "config.toml", "requirements.txt"}

    def test_filter_empty_list(self) -> None:
        """Test filtering empty list."""
        filtered = filter_files_by_extension([], {".py"})

        assert len(filtered) == 0

    def test_no_matches(self) -> None:
        """Test when no files match extensions."""
        changes = [
            DiffFileChange(path="README.md"),
            DiffFileChange(path="LICENSE"),
        ]

        filtered = filter_files_by_extension(changes, {".py"})

        assert len(filtered) == 0


class TestFilterFilesByPattern:
    """Tests for filter_files_by_pattern()."""

    def test_exclude_tests(self) -> None:
        """Test excluding test directory."""
        changes = [
            DiffFileChange(path="src/app.py"),
            DiffFileChange(path="tests/test_app.py"),
            DiffFileChange(path="tests/fixtures/data.json"),
        ]

        filtered = filter_files_by_pattern(changes, ["tests/**"])

        assert len(filtered) == 1
        assert filtered[0].path == "src/app.py"

    def test_exclude_multiple_patterns(self) -> None:
        """Test excluding multiple patterns."""
        changes = [
            DiffFileChange(path="src/app.py"),
            DiffFileChange(path="tests/test_app.py"),
            DiffFileChange(path="docs/README.md"),
            DiffFileChange(path="build/output.txt"),
        ]

        filtered = filter_files_by_pattern(changes, ["tests/**", "docs/**", "build/**"])

        assert len(filtered) == 1
        assert filtered[0].path == "src/app.py"

    def test_no_exclusions(self) -> None:
        """Test with no exclude patterns."""
        changes = [
            DiffFileChange(path="src/app.py"),
            DiffFileChange(path="tests/test_app.py"),
        ]

        filtered = filter_files_by_pattern(changes, [])

        assert len(filtered) == 2

    def test_exclude_pyc_files(self) -> None:
        """Test excluding .pyc files."""
        changes = [
            DiffFileChange(path="src/app.py"),
            DiffFileChange(path="src/__pycache__/app.pyc"),
        ]

        filtered = filter_files_by_pattern(changes, ["**/*.pyc", "**/__pycache__/**"])

        assert len(filtered) == 1
        assert filtered[0].path == "src/app.py"

    def test_pattern_without_prefix(self) -> None:
        """Test that patterns work without **/ prefix."""
        changes = [
            DiffFileChange(path="tests/test_app.py"),
            DiffFileChange(path="app.py"),
        ]

        # Pattern without **/ should still match
        filtered = filter_files_by_pattern(changes, ["tests/**"])

        assert len(filtered) == 1
        assert filtered[0].path == "app.py"

