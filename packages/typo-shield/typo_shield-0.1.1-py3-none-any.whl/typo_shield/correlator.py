"""
Import-to-dependency correlator.

Correlates imported modules with declared dependencies to find:
- Missing dependencies (imports without declarations)
- Standard library usage
- Local module usage
"""

from __future__ import annotations

from pathlib import Path

from typo_shield.mapping.module_to_dist import (
    get_dist_name,
    normalize_dist_name,
)
from typo_shield.mapping.project_modules import is_local_module
from typo_shield.mapping.stdlib import is_stdlib
from typo_shield.risk.models import RiskFinding
from typo_shield.scanners.deps_requirements import DependencyFinding
from typo_shield.scanners.python_imports import PythonImportFinding


def correlate_imports_and_deps(
    new_imports: list[PythonImportFinding],
    declared_deps: set[str],
    repo_root: Path,
) -> list[RiskFinding]:
    """
    Correlate imported modules with declared dependencies.

    Analyzes imports to determine if they are:
    1. Standard library → INFO
    2. Local modules → INFO
    3. Third-party without declaration → WARN
    4. Third-party with declaration → (no finding)

    Args:
        new_imports: List of imports found in added/changed lines
        declared_deps: Set of all declared dependency names (normalized)
        repo_root: Repository root path for local module detection

    Returns:
        List of RiskFinding objects

    Example:
        >>> imports = [
        ...     PythonImportFinding(file="main.py", module="requests", kind="import", lineno=1),
        ...     PythonImportFinding(file="main.py", module="os", kind="import", lineno=2),
        ... ]
        >>> deps = {"requests"}
        >>> findings = correlate_imports_and_deps(imports, deps, Path("."))
        >>> len(findings)
        1
        >>> findings[0].kind
        'stdlib_import'
    """
    findings: list[RiskFinding] = []

    # Normalize declared deps for comparison
    normalized_deps = {normalize_dist_name(dep) for dep in declared_deps}

    for imp in new_imports:
        # Skip relative imports
        if imp.is_relative:
            findings.append(
                RiskFinding(
                    kind="relative_import",
                    subject="import",
                    name=imp.module or "(relative)",
                    target=None,
                    level="INFO",
                    code="TS900",
                    message=f"Relative import detected: {imp.raw or imp.module}",
                    file=imp.file,
                    lineno=imp.lineno,
                )
            )
            continue

        module = imp.module

        # Check if standard library
        if is_stdlib(module):
            findings.append(
                RiskFinding(
                    kind="stdlib_import",
                    subject="import",
                    name=module,
                    target=None,
                    level="INFO",
                    code="TS900",
                    message=f"Standard library import: {module}",
                    file=imp.file,
                    lineno=imp.lineno,
                )
            )
            continue

        # Check if local module
        if is_local_module(module, repo_root):
            findings.append(
                RiskFinding(
                    kind="local_import",
                    subject="import",
                    name=module,
                    target=None,
                    level="INFO",
                    code="TS900",
                    message=f"Local module import: {module}",
                    file=imp.file,
                    lineno=imp.lineno,
                )
            )
            continue

        # Third-party import: check if declared
        dist_name = get_dist_name(module)
        normalized_dist = normalize_dist_name(dist_name)

        if normalized_dist not in normalized_deps:
            # Not declared → WARN (missing dependency)
            findings.append(
                RiskFinding(
                    kind="missing_dep",
                    subject="import",
                    name=module,
                    target=dist_name if dist_name != module else None,
                    level="WARN",
                    code="TS101",
                    message=f"Import '{module}' (package: {dist_name}) not found in declared dependencies",
                    file=imp.file,
                    lineno=imp.lineno,
                    context={
                        "expected_package": dist_name,
                        "import_statement": imp.raw or f"import {module}",
                    },
                )
            )

    return findings


def collect_declared_deps(deps: list[DependencyFinding]) -> set[str]:
    """
    Collect and normalize all declared dependency names.

    Args:
        deps: List of DependencyFinding objects

    Returns:
        Set of normalized dependency names

    Example:
        >>> deps = [
        ...     DependencyFinding(file="requirements.txt", name="requests", specifier=">=2.28.0", source="requirements.txt", lineno=1),
        ...     DependencyFinding(file="requirements.txt", name="Flask", specifier="==2.0.0", source="requirements.txt", lineno=2),
        ... ]
        >>> collect_declared_deps(deps)
        {'requests', 'flask'}
    """
    return {normalize_dist_name(dep.name) for dep in deps}


def analyze_new_deps(
    new_deps: list[DependencyFinding],
) -> list[RiskFinding]:
    """
    Analyze newly added dependencies for informational purposes.

    In MVP, we just generate INFO findings for tracking.
    Future: could check for git/local deps, suspicious names, etc.

    Args:
        new_deps: List of newly added dependencies

    Returns:
        List of RiskFinding objects (INFO level)

    Example:
        >>> deps = [
        ...     DependencyFinding(file="requirements.txt", name="requests", specifier=">=2.28.0", source="requirements.txt", lineno=1),
        ... ]
        >>> findings = analyze_new_deps(deps)
        >>> len(findings)
        1
        >>> findings[0].level
        'INFO'
    """
    findings: list[RiskFinding] = []

    for dep in new_deps:
        # Generate INFO for new dependency
        msg = f"New dependency added: {dep.name}"
        if dep.specifier:
            msg += f" {dep.specifier}"

        if dep.is_git:
            msg += " (Git source)"
        elif dep.is_local:
            msg += " (local path)"

        findings.append(
            RiskFinding(
                kind="new_dep",
                subject="dep",
                name=dep.name,
                target=None,
                level="INFO",
                code="TS900",
                message=msg,
                file=dep.file,
                lineno=dep.lineno,
            )
        )

    return findings

