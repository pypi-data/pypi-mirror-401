"""
Git operations for typo-shield.

Functions for getting repository root, diff, and changed files.
"""

from __future__ import annotations

import subprocess
from pathlib import Path


class GitError(Exception):
    """Raised when git command fails."""

    pass


def get_repo_root(path: Path | None = None) -> Path:
    """
    Get the root directory of the git repository.

    Args:
        path: Starting path (default: current directory)

    Returns:
        Path to repository root

    Raises:
        GitError: If not in a git repository or git is not available
    """
    try:
        cmd = ["git", "rev-parse", "--show-toplevel"]
        if path:
            result = subprocess.run(
                cmd,
                cwd=path,
                capture_output=True,
                text=True,
                check=True,
            )
        else:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True,
            )
        return Path(result.stdout.strip())
    except subprocess.CalledProcessError as e:
        raise GitError(f"Not a git repository or git not found: {e.stderr.strip()}") from e
    except FileNotFoundError as e:
        raise GitError("git command not found. Please install git.") from e


def get_staged_diff(repo_root: Path | None = None) -> str:
    """
    Get diff of staged changes.

    Args:
        repo_root: Repository root directory (optional, uses current directory if not provided)

    Returns:
        Unified diff text

    Raises:
        GitError: If git command fails
    """
    try:
        result = subprocess.run(
            ["git", "diff", "--staged", "--unified=0"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        raise GitError(f"Failed to get staged diff: {e.stderr.strip()}") from e
    except FileNotFoundError as e:
        raise GitError("git command not found. Please install git.") from e


def get_range_diff(repo_root: Path, base: str, head: str) -> str:
    """
    Get diff between two git references.

    Args:
        repo_root: Repository root directory
        base: Base reference (e.g., 'main', 'HEAD~1')
        head: Head reference (e.g., 'feature', 'HEAD')

    Returns:
        Unified diff text

    Raises:
        GitError: If git command fails or references are invalid
    """
    try:
        # Support both "base...head" and "base..head" formats
        if "..." in f"{base}{head}":
            # Already contains separator
            diff_spec = f"{base}..{head}" if ".." not in f"{base}{head}" else f"{base}{head}"
        else:
            diff_spec = f"{base}..{head}"

        result = subprocess.run(
            ["git", "diff", diff_spec, "--unified=0"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        raise GitError(
            f"Failed to get diff for {base}..{head}: {e.stderr.strip()}"
        ) from e
    except FileNotFoundError as e:
        raise GitError("git command not found. Please install git.") from e


def list_changed_files_from_diff(diff_text: str) -> list[str]:
    """
    Extract list of changed file paths from unified diff.

    Parses "+++ b/path/to/file" lines.
    Filters out:
    - Deleted files (/dev/null)
    - Binary files

    Args:
        diff_text: Unified diff output

    Returns:
        List of file paths (relative to repo root)
    """
    files: list[str] = []

    for line in diff_text.split("\n"):
        # Look for "+++ b/path/to/file" lines
        if line.startswith("+++ b/"):
            filepath = line[6:]  # Remove "+++ b/" prefix

            # Skip /dev/null (deleted files)
            if filepath == "/dev/null":
                continue

            # Normalize Windows paths to Unix
            filepath = filepath.replace("\\", "/")

            files.append(filepath)

    return files

