"""
Requirements.txt dependency scanner.

Scans requirements files for package dependencies.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Literal

from packaging.requirements import InvalidRequirement, Requirement

from typo_shield.diff import DiffFileChange


@dataclass
class DependencyFinding:
    """
    Represents a dependency found in a requirements file or pyproject.toml.

    Attributes:
        file: Path to the file containing the dependency
        name: Package name (normalized: lowercase, _ → -)
        specifier: Version specifier (e.g., ">=1.2.3", "==2.0.0")
        source: Source of the dependency ('requirements', 'pyproject_pep621', 'pyproject_poetry')
        lineno: Line number in the file (1-indexed), or None
        raw: Original line text
        is_git: True if this is a git URL dependency
        is_local: True if this is a local file/directory dependency
    """
    file: str
    name: str
    specifier: str
    source: Literal["requirements", "pyproject_pep621", "pyproject_poetry"]
    lineno: int | None = None
    raw: str | None = None
    is_git: bool = False
    is_local: bool = False


def scan_requirements(
    file_change: DiffFileChange,
) -> list[DependencyFinding]:
    """
    Scan requirements.txt file for dependencies.

    Only processes added lines from diff.

    Handles:
    - Simple package names: requests
    - Versioned packages: requests==2.28.0
    - Version specifiers: requests>=2.0,<3.0
    - Extras: requests[security]>=2.0
    - Comments: # comment (ignored)
    - Options: -r, --index-url, etc. (noted but skipped)
    - Git URLs: git+https://... (marked as non-PyPI)
    - Local paths: ./local or file:// (marked as local)

    Args:
        file_change: DiffFileChange object with added lines

    Returns:
        List of DependencyFinding objects

    Example:
        >>> change = DiffFileChange(
        ...     path="requirements.txt",
        ...     added_lines=[(1, "requests==2.28.0"), (2, "numpy>=1.20")]
        ... )
        >>> findings = scan_requirements(change)
        >>> len(findings)
        2
    """
    findings: list[DependencyFinding] = []

    for lineno, line in file_change.added_lines:
        # Strip whitespace
        line = line.strip()

        # Skip empty lines
        if not line:
            continue

        # Skip comments
        if line.startswith('#'):
            continue

        # Skip option lines (-r, -c, --index-url, etc.)
        if line.startswith('-'):
            # Could log these as INFO
            continue

        # Check for git URLs (before removing inline comments, as # can be part of URL)
        if line.startswith(('git+', 'hg+', 'svn+', 'bzr+')) or 'git@' in line:
            # Extract package name if possible from git URL
            name = _extract_name_from_git_url(line)
            findings.append(DependencyFinding(
                file=file_change.path,
                name=name or "unknown-git-package",
                specifier="",
                source="requirements",
                lineno=lineno,
                raw=line,
                is_git=True,
            ))
            continue

        # Check for local file paths
        if line.startswith(('file://', './', '../', '/')) or '\\' in line:
            name = _extract_name_from_local_path(line)
            findings.append(DependencyFinding(
                file=file_change.path,
                name=name or "unknown-local-package",
                specifier="",
                source="requirements",
                lineno=lineno,
                raw=line,
                is_local=True,
            ))
            continue

        # Handle inline comments for standard requirements
        # (do this AFTER checking git/local paths, as # can be part of URL)
        if '#' in line:
            line = line.split('#')[0].strip()
            if not line:
                continue

        # Try parsing as standard requirement
        try:
            req = Requirement(line)

            # Normalize name: lowercase, _ → -
            normalized_name = normalize_package_name(req.name)

            # Get specifier string
            specifier_str = str(req.specifier) if req.specifier else ""

            findings.append(DependencyFinding(
                file=file_change.path,
                name=normalized_name,
                specifier=specifier_str,
                source="requirements",
                lineno=lineno,
                raw=line,
            ))
        except InvalidRequirement:
            # Skip lines we can't parse
            # Could log these as warnings
            continue

    return findings


def normalize_package_name(name: str) -> str:
    """
    Normalize package name according to PyPI rules.

    - Convert to lowercase
    - Replace underscores with hyphens
    - Replace dots with hyphens

    Args:
        name: Original package name

    Returns:
        Normalized name

    Example:
        >>> normalize_package_name("Flask_RESTful")
        'flask-restful'
        >>> normalize_package_name("some.package")
        'some-package'
    """
    normalized = name.lower()
    normalized = normalized.replace('_', '-')
    normalized = normalized.replace('.', '-')
    return normalized


def _extract_name_from_git_url(url: str) -> str | None:
    """
    Try to extract package name from git URL.

    Examples:
        git+https://github.com/user/repo.git
        git+https://github.com/user/repo.git@branch
        git+https://github.com/user/repo.git#egg=package-name

    Args:
        url: Git URL

    Returns:
        Package name if found, None otherwise
    """
    # Try to extract from #egg= parameter (highest priority)
    egg_match = re.search(r'[#&]egg=([a-zA-Z0-9_-]+)', url)
    if egg_match:
        return normalize_package_name(egg_match.group(1))

    # Try to extract from repository name (fallback)
    # Match the last component before .git or @
    repo_match = re.search(r'/([a-zA-Z0-9_-]+?)(?:\.git)?(?:[@#]|$)', url)
    if repo_match:
        return normalize_package_name(repo_match.group(1))

    return None


def _extract_name_from_local_path(path: str) -> str | None:
    """
    Try to extract package name from local file path.

    Examples:
        ./local-package
        ../my_package
        file:///path/to/package

    Args:
        path: Local file path

    Returns:
        Package name if found, None otherwise
    """
    # Remove file:// prefix
    if path.startswith('file://'):
        path = path[7:]

    # Get last component of path
    components = path.rstrip('/\\').split('/')[-1].split('\\')[-1]

    # Remove common suffixes
    for suffix in ['.tar.gz', '.zip', '.whl', '.egg']:
        if components.endswith(suffix):
            components = components[:-len(suffix)]
            break

    if components:
        return normalize_package_name(components)

    return None


def deduplicate_dependencies(
    findings: list[DependencyFinding],
) -> list[DependencyFinding]:
    """
    Remove duplicate dependencies (same package in same file).

    Keeps first occurrence.

    Args:
        findings: List of dependency findings

    Returns:
        Deduplicated list
    """
    seen: set[tuple[str, str]] = set()
    deduplicated = []

    for finding in findings:
        key = (finding.file, finding.name)
        if key not in seen:
            seen.add(key)
            deduplicated.append(finding)

    return deduplicated

