"""Integration tests for CLI."""

from __future__ import annotations

import os
import re
import subprocess
from pathlib import Path

import pytest


class TestCLIVersion:
    """Tests for CLI version command."""

    def test_version_flag(self) -> None:
        """Test --version flag."""
        result = subprocess.run(
            ["typo-shield", "--version"],
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0
        assert "typo-shield version" in result.stdout
        assert "0.1.0" in result.stdout

    def test_version_short_flag(self) -> None:
        """Test -v flag."""
        result = subprocess.run(
            ["typo-shield", "-v"],
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0
        assert "typo-shield version" in result.stdout


class TestCLIHelp:
    """Tests for CLI help."""

    def test_help_flag(self) -> None:
        """Test --help flag."""
        result = subprocess.run(
            ["typo-shield", "--help"],
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0
        assert "typo-shield" in result.stdout
        assert "scan" in result.stdout

    def test_scan_help(self) -> None:
        """Test scan --help."""
        result = subprocess.run(
            ["typo-shield", "scan", "--help"],
            capture_output=True,
            text=True,
            env={**os.environ, "NO_COLOR": "1"},  # Disable colors for testing
        )

        assert result.returncode == 0
        assert "scan" in result.stdout
        assert "staged" in result.stdout  # Check without -- to avoid ANSI code issues
        # Strip ANSI codes for reliable checking
        clean_output = re.sub(r'\x1b\[[0-9;]*m', '', result.stdout)
        assert "diff-range" in clean_output or "diff" in clean_output


class TestCLIValidation:
    """Tests for CLI argument validation."""

    def test_invalid_format(self, tmp_path: Path) -> None:
        """Test invalid output format."""
        # Create a minimal git repo
        repo = tmp_path / "test_repo"
        repo.mkdir()
        subprocess.run(["git", "init"], cwd=repo, capture_output=True)

        result = subprocess.run(
            ["typo-shield", "scan", "--format", "invalid"],
            cwd=repo,
            capture_output=True,
            text=True,
        )

        assert result.returncode == 2
        assert "Invalid format" in result.stderr

    def test_invalid_fail_on(self, tmp_path: Path) -> None:
        """Test invalid --fail-on value."""
        # Create a minimal git repo
        repo = tmp_path / "test_repo"
        repo.mkdir()
        subprocess.run(["git", "init"], cwd=repo, capture_output=True)

        result = subprocess.run(
            ["typo-shield", "scan", "--fail-on", "invalid"],
            cwd=repo,
            capture_output=True,
            text=True,
        )

        assert result.returncode == 2
        assert "Invalid --fail-on value" in result.stderr

    def test_mutually_exclusive_args(self, tmp_path: Path) -> None:
        """Test that --staged and --diff-range are mutually exclusive."""
        # Create a minimal git repo
        repo = tmp_path / "test_repo"
        repo.mkdir()
        subprocess.run(["git", "init"], cwd=repo, capture_output=True)

        result = subprocess.run(
            ["typo-shield", "scan", "--staged", "--diff-range", "main...feature"],
            cwd=repo,
            capture_output=True,
            text=True,
        )

        assert result.returncode == 2
        assert "mutually exclusive" in result.stderr


class TestCLIScanBasic:
    """Basic scan tests."""

    def test_scan_empty_repo(self, tmp_path: Path) -> None:
        """Test scanning empty repository with no changes."""
        # Create a minimal git repo
        repo = tmp_path / "test_repo"
        repo.mkdir()
        subprocess.run(["git", "init"], cwd=repo, capture_output=True)
        subprocess.run(["git", "config", "user.email", "test@test.com"], cwd=repo, capture_output=True)
        subprocess.run(["git", "config", "user.name", "Test User"], cwd=repo, capture_output=True)

        # Create initial commit
        (repo / "README.md").write_text("# Test")
        subprocess.run(["git", "add", "."], cwd=repo, capture_output=True)
        subprocess.run(["git", "commit", "-m", "Initial commit"], cwd=repo, capture_output=True)

        # Run scan with no staged changes
        result = subprocess.run(
            ["typo-shield", "scan"],
            cwd=repo,
            capture_output=True,
            text=True,
        )

        # Should succeed with no findings
        assert result.returncode == 0
        assert "typo-shield Security Report" in result.stdout or "Summary" in result.stdout

    def test_scan_json_output(self, tmp_path: Path) -> None:
        """Test JSON output format."""
        # Create a minimal git repo
        repo = tmp_path / "test_repo"
        repo.mkdir()
        subprocess.run(["git", "init"], cwd=repo, capture_output=True)
        subprocess.run(["git", "config", "user.email", "test@test.com"], cwd=repo, capture_output=True)
        subprocess.run(["git", "config", "user.name", "Test User"], cwd=repo, capture_output=True)

        # Create initial commit
        (repo / "README.md").write_text("# Test")
        subprocess.run(["git", "add", "."], cwd=repo, capture_output=True)
        subprocess.run(["git", "commit", "-m", "Initial commit"], cwd=repo, capture_output=True)

        # Run scan with JSON output
        result = subprocess.run(
            ["typo-shield", "scan", "--format", "json"],
            cwd=repo,
            capture_output=True,
            text=True,
        )

        # Should succeed
        assert result.returncode == 0

        # Should be valid JSON
        import json
        data = json.loads(result.stdout)
        assert "version" in data
        assert "summary" in data
        assert "findings" in data


@pytest.mark.slow
class TestCLIScanWithFindings:
    """Tests that generate findings."""

    def test_scan_with_typosquat(self, tmp_path: Path) -> None:
        """Test scanning with a typosquat finding."""
        # Create a git repo
        repo = tmp_path / "test_repo"
        repo.mkdir()
        subprocess.run(["git", "init"], cwd=repo, capture_output=True)
        subprocess.run(["git", "config", "user.email", "test@test.com"], cwd=repo, capture_output=True)
        subprocess.run(["git", "config", "user.name", "Test User"], cwd=repo, capture_output=True)

        # Create initial commit
        (repo / "README.md").write_text("# Test")
        subprocess.run(["git", "add", "."], cwd=repo, capture_output=True)
        subprocess.run(["git", "commit", "-m", "Initial commit"], cwd=repo, capture_output=True)

        # Add requirements.txt with a typosquat
        (repo / "requirements.txt").write_text("requets==2.28.0\n")  # Typo: requets instead of requests
        subprocess.run(["git", "add", "requirements.txt"], cwd=repo, capture_output=True)

        # Run scan on staged changes
        result = subprocess.run(
            ["typo-shield", "scan"],
            cwd=repo,
            capture_output=True,
            text=True,
        )

        # Should fail due to typosquat
        assert result.returncode == 1
        assert "FAIL" in result.stdout or "fail" in result.stdout.lower()


class TestCLIScanNotGitRepo:
    """Tests for non-git directories."""

    def test_scan_non_git_directory(self, tmp_path: Path) -> None:
        """Test scanning non-git directory."""
        # Create a directory without git
        non_git_dir = tmp_path / "not_git"
        non_git_dir.mkdir()

        result = subprocess.run(
            ["typo-shield", "scan"],
            cwd=non_git_dir,
            capture_output=True,
            text=True,
        )

        # Should fail with error
        assert result.returncode == 2
        assert "not a Git repository" in result.stderr or "Error" in result.stderr

