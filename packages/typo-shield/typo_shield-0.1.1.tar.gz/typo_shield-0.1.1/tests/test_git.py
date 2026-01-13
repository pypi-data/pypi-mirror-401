"""Tests for git operations."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from typo_shield.git import (
    GitError,
    get_range_diff,
    get_repo_root,
    get_staged_diff,
    list_changed_files_from_diff,
)


class TestGetRepoRoot:
    """Tests for get_repo_root()."""

    @patch("subprocess.run")
    def test_get_repo_root_success(self, mock_run: MagicMock) -> None:
        """Test successful repo root detection."""
        mock_run.return_value = MagicMock(
            stdout="/home/user/project\n",
            returncode=0,
        )

        result = get_repo_root()

        assert result == Path("/home/user/project")
        mock_run.assert_called_once()

    @patch("subprocess.run")
    def test_get_repo_root_not_a_repo(self, mock_run: MagicMock) -> None:
        """Test error when not in a git repository."""
        from subprocess import CalledProcessError

        mock_run.side_effect = CalledProcessError(
            128,
            ["git"],
            stderr="fatal: not a git repository",
        )

        with pytest.raises(GitError, match="Not a git repository"):
            get_repo_root()

    @patch("subprocess.run")
    def test_get_repo_root_git_not_found(self, mock_run: MagicMock) -> None:
        """Test error when git is not installed."""
        mock_run.side_effect = FileNotFoundError()

        with pytest.raises(GitError, match="git command not found"):
            get_repo_root()


class TestGetStagedDiff:
    """Tests for get_staged_diff()."""

    @patch("subprocess.run")
    def test_get_staged_diff_success(self, mock_run: MagicMock) -> None:
        """Test successful staged diff retrieval."""
        mock_diff = """diff --git a/test.py b/test.py
index abc123..def456 100644
--- a/test.py
+++ b/test.py
@@ -1 +1,2 @@
+import requests
"""
        mock_run.return_value = MagicMock(
            stdout=mock_diff,
            returncode=0,
        )

        result = get_staged_diff()

        assert result == mock_diff
        mock_run.assert_called_once_with(
            ["git", "diff", "--staged", "--unified=0"],
            cwd=None,
            capture_output=True,
            text=True,
            check=True,
        )

    @patch("subprocess.run")
    def test_get_staged_diff_empty(self, mock_run: MagicMock) -> None:
        """Test with no staged changes."""
        mock_run.return_value = MagicMock(
            stdout="",
            returncode=0,
        )

        result = get_staged_diff()

        assert result == ""


class TestGetRangeDiff:
    """Tests for get_range_diff()."""

    @patch("subprocess.run")
    def test_get_range_diff_success(self, mock_run: MagicMock) -> None:
        """Test successful range diff."""
        mock_diff = "diff --git a/file.py b/file.py\n..."
        mock_run.return_value = MagicMock(
            stdout=mock_diff,
            returncode=0,
        )

        result = get_range_diff(Path("/tmp"), "main", "feature")

        assert result == mock_diff
        assert mock_run.called

    @patch("subprocess.run")
    def test_get_range_diff_invalid_ref(self, mock_run: MagicMock) -> None:
        """Test with invalid git reference."""
        from subprocess import CalledProcessError

        mock_run.side_effect = CalledProcessError(
            128,
            ["git"],
            stderr="fatal: bad revision",
        )

        with pytest.raises(GitError, match="Failed to get diff"):
            get_range_diff(Path("/tmp"), "invalid", "refs")


class TestListChangedFilesFromDiff:
    """Tests for list_changed_files_from_diff()."""

    def test_simple_addition(self) -> None:
        """Test parsing simple file addition."""
        diff = """diff --git a/test.py b/test.py
new file mode 100644
index 0000000..abc123
--- /dev/null
+++ b/test.py
@@ -0,0 +1 @@
+import requests
"""
        files = list_changed_files_from_diff(diff)

        assert files == ["test.py"]

    def test_multiple_files(self) -> None:
        """Test parsing multiple changed files."""
        diff = """diff --git a/file1.py b/file1.py
--- a/file1.py
+++ b/file1.py
@@ -1 +1,2 @@
+import os
diff --git a/file2.py b/file2.py
--- a/file2.py
+++ b/file2.py
@@ -1 +1,2 @@
+import sys
"""
        files = list_changed_files_from_diff(diff)

        assert files == ["file1.py", "file2.py"]

    def test_skip_dev_null(self) -> None:
        """Test skipping deleted files (/dev/null)."""
        diff = """diff --git a/deleted.py b/deleted.py
deleted file mode 100644
index abc123..0000000
--- a/deleted.py
+++ /dev/null
@@ -1 +0,0 @@
-import requests
diff --git a/added.py b/added.py
new file mode 100644
--- /dev/null
+++ b/added.py
@@ -0,0 +1 @@
+import os
"""
        files = list_changed_files_from_diff(diff)

        assert files == ["added.py"]
        assert "deleted.py" not in files

    def test_windows_paths(self) -> None:
        """Test normalization of Windows paths."""
        diff = r"""--- a/path\to\file.py
+++ b/path\to\file.py
"""
        files = list_changed_files_from_diff(diff)

        assert files == ["path/to/file.py"]

    def test_empty_diff(self) -> None:
        """Test with empty diff."""
        files = list_changed_files_from_diff("")

        assert files == []

