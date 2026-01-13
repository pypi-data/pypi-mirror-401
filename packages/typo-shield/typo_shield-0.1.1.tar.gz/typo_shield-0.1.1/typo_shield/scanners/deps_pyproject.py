"""
pyproject.toml dependency scanner.

Scans pyproject.toml for dependencies in both PEP 621 and Poetry formats.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

if sys.version_info >= (3, 11):
    import tomllib
else:
    try:
        import tomli as tomllib
    except ImportError:
        tomllib = None  # type: ignore

from typo_shield.diff import DiffFileChange
from typo_shield.scanners.deps_requirements import (
    DependencyFinding,
    normalize_package_name,
)


def scan_pyproject(
    file_change: DiffFileChange,
    repo_root: Path,
) -> list[DependencyFinding]:
    """
    Scan pyproject.toml for dependencies.

    Supports:
    - PEP 621: [project] dependencies and optional-dependencies
    - Poetry: [tool.poetry.dependencies] and [tool.poetry.group.*.dependencies]

    Args:
        file_change: DiffFileChange object
        repo_root: Repository root path

    Returns:
        List of DependencyFinding objects

    Example:
        >>> change = DiffFileChange(path="pyproject.toml", added_lines=[...])
        >>> findings = scan_pyproject(change, Path("/repo"))
    """
    if tomllib is None:
        # Can't parse TOML without tomllib/tomli
        return []

    findings: list[DependencyFinding] = []
    file_path = repo_root / file_change.path

    # Read and parse full TOML file
    if not file_path.exists():
        return []

    try:
        with open(file_path, 'rb') as f:
            data = tomllib.load(f)
    except (tomllib.TOMLDecodeError, OSError):  # type: ignore
        return []

    # Parse PEP 621 dependencies
    findings.extend(_parse_pep621_dependencies(data, file_change.path))

    # Parse Poetry dependencies
    findings.extend(_parse_poetry_dependencies(data, file_change.path))

    # Filter to only dependencies on added lines
    # (For MVP, we check if the dependency name appears in added lines)
    findings = _filter_to_added_lines(findings, file_change)

    return findings


def _parse_pep621_dependencies(
    data: dict[str, Any],
    filepath: str,
) -> list[DependencyFinding]:
    """
    Parse PEP 621 format dependencies.

    Format:
        [project]
        dependencies = [
            "requests>=2.28.0",
            "numpy>=1.20,<2.0",
        ]

        [project.optional-dependencies]
        dev = ["pytest>=7.0"]
        docs = ["sphinx"]

    Args:
        data: Parsed TOML data
        filepath: Path to pyproject.toml

    Returns:
        List of dependency findings
    """
    findings: list[DependencyFinding] = []

    project = data.get('project', {})
    if not isinstance(project, dict):
        return findings

    # Main dependencies
    dependencies = project.get('dependencies', [])
    if isinstance(dependencies, list):
        for dep_str in dependencies:
            if not isinstance(dep_str, str):
                continue
            finding = _parse_pep621_dependency_string(dep_str, filepath)
            if finding:
                findings.append(finding)

    # Optional dependencies
    optional_deps = project.get('optional-dependencies', {})
    if isinstance(optional_deps, dict):
        for _group_name, deps in optional_deps.items():
            if not isinstance(deps, list):
                continue
            for dep_str in deps:
                if not isinstance(dep_str, str):
                    continue
                finding = _parse_pep621_dependency_string(dep_str, filepath)
                if finding:
                    findings.append(finding)

    return findings


def _parse_pep621_dependency_string(
    dep_str: str,
    filepath: str,
) -> DependencyFinding | None:
    """
    Parse a single PEP 621 dependency string.

    Examples:
        "requests>=2.28.0"
        "numpy>=1.20,<2.0"
        "flask[async]>=2.0"

    Args:
        dep_str: Dependency string
        filepath: Source file path

    Returns:
        DependencyFinding or None if parsing fails
    """
    from packaging.requirements import InvalidRequirement, Requirement

    try:
        req = Requirement(dep_str)
        normalized_name = normalize_package_name(req.name)
        specifier_str = str(req.specifier) if req.specifier else ""

        return DependencyFinding(
            file=filepath,
            name=normalized_name,
            specifier=specifier_str,
            source="pyproject_pep621",
        )
    except InvalidRequirement:
        return None


def _parse_poetry_dependencies(
    data: dict[str, Any],
    filepath: str,
) -> list[DependencyFinding]:
    """
    Parse Poetry format dependencies.

    Format:
        [tool.poetry.dependencies]
        python = "^3.8"
        requests = "^2.28.0"
        numpy = {version = "^1.20", optional = true}

        [tool.poetry.group.dev.dependencies]
        pytest = "^7.0"

    Args:
        data: Parsed TOML data
        filepath: Path to pyproject.toml

    Returns:
        List of dependency findings
    """
    findings: list[DependencyFinding] = []

    tool = data.get('tool', {})
    if not isinstance(tool, dict):
        return findings

    poetry = tool.get('poetry', {})
    if not isinstance(poetry, dict):
        return findings

    # Main dependencies
    dependencies = poetry.get('dependencies', {})
    if isinstance(dependencies, dict):
        for name, spec in dependencies.items():
            # Skip python itself
            if name.lower() == 'python':
                continue

            finding = _parse_poetry_dependency(name, spec, filepath)
            if finding:
                findings.append(finding)

    # Development dependencies (legacy format)
    dev_dependencies = poetry.get('dev-dependencies', {})
    if isinstance(dev_dependencies, dict):
        for name, spec in dev_dependencies.items():
            finding = _parse_poetry_dependency(name, spec, filepath)
            if finding:
                findings.append(finding)

    # Group dependencies (new format)
    group = poetry.get('group', {})
    if isinstance(group, dict):
        for _group_name, group_data in group.items():
            if not isinstance(group_data, dict):
                continue
            group_deps = group_data.get('dependencies', {})
            if isinstance(group_deps, dict):
                for name, spec in group_deps.items():
                    finding = _parse_poetry_dependency(name, spec, filepath)
                    if finding:
                        findings.append(finding)

    return findings


def _parse_poetry_dependency(
    name: str,
    spec: Any,
    filepath: str,
) -> DependencyFinding | None:
    """
    Parse a single Poetry dependency.

    Poetry supports multiple formats:
    - Simple string: requests = "^2.28.0"
    - Dict: requests = {version = "^2.28.0", optional = true}
    - Git: requests = {git = "https://github.com/..."}

    Args:
        name: Package name
        spec: Version specification (string or dict)
        filepath: Source file path

    Returns:
        DependencyFinding or None
    """
    normalized_name = normalize_package_name(name)

    # Simple string version
    if isinstance(spec, str):
        return DependencyFinding(
            file=filepath,
            name=normalized_name,
            specifier=spec,
            source="pyproject_poetry",
        )

    # Dict format
    if isinstance(spec, dict):
        # Check for git dependency
        if 'git' in spec or 'url' in spec or 'path' in spec:
            return DependencyFinding(
                file=filepath,
                name=normalized_name,
                specifier="",
                source="pyproject_poetry",
                is_git='git' in spec or 'url' in spec,
                is_local='path' in spec,
            )

        # Regular version in dict
        version = spec.get('version', '')
        return DependencyFinding(
            file=filepath,
            name=normalized_name,
            specifier=str(version) if version else "",
            source="pyproject_poetry",
        )

    return None


def _filter_to_added_lines(
    findings: list[DependencyFinding],
    file_change: DiffFileChange,
) -> list[DependencyFinding]:
    """
    Filter dependencies to only those mentioned in added lines.

    This is a simple approach for MVP: check if package name appears
    in any of the added lines.

    Args:
        findings: All dependencies found in file
        file_change: DiffFileChange with added lines

    Returns:
        Filtered list of dependencies
    """
    # Collect all text from added lines
    added_text = '\n'.join(line for _, line in file_change.added_lines)
    added_text_lower = added_text.lower()

    filtered = []
    for finding in findings:
        # Check if package name appears in added lines
        # (both normalized and original forms)
        name_variants = [
            finding.name,
            finding.name.replace('-', '_'),
            finding.name.replace('-', '.'),
        ]

        if any(variant in added_text_lower for variant in name_variants):
            filtered.append(finding)

    return filtered

