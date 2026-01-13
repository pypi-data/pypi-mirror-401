"""
Python import scanner using AST.

Scans Python files for import statements and extracts top-level module names.
"""

from __future__ import annotations

import ast
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

from typo_shield.diff import DiffFileChange


@dataclass
class PythonImportFinding:
    """
    Represents a single import statement found in Python code.

    Attributes:
        file: Path to the file containing the import
        module: Top-level module name (e.g., 'requests' from 'import requests.auth')
        kind: Type of import ('import' or 'from')
        lineno: Line number in the file (1-indexed), or None if unknown
        raw: Original import line text, or None
        is_relative: True if this is a relative import (from . import ...)
    """
    file: str
    module: str
    kind: Literal["import", "from"]
    lineno: int | None = None
    raw: str | None = None
    is_relative: bool = False


def scan_python_imports(
    file_change: DiffFileChange,
    repo_root: Path,
) -> list[PythonImportFinding]:
    """
    Scan a Python file for import statements.

    Strategy:
    1. Try to read full file from disk and parse with AST (preferred)
    2. If file doesn't exist or AST fails, use regex fallback on added lines

    Args:
        file_change: DiffFileChange object with file path and added lines
        repo_root: Repository root path

    Returns:
        List of PythonImportFinding objects

    Example:
        >>> change = DiffFileChange(
        ...     path="app.py",
        ...     added_lines=[(1, "import requests"), (2, "from PIL import Image")]
        ... )
        >>> findings = scan_python_imports(change, Path("/repo"))
        >>> len(findings)
        2
    """
    findings: list[PythonImportFinding] = []
    file_path = repo_root / file_change.path

    # Strategy A: Full file AST parsing (preferred)
    if file_path.exists() and file_path.is_file():
        try:
            with open(file_path, encoding='utf-8') as f:
                content = f.read()
            findings = _parse_imports_ast(content, file_change.path)
        except (SyntaxError, UnicodeDecodeError):
            # Fall back to regex if AST fails
            findings = _parse_imports_regex(file_change)
    else:
        # Strategy B: Regex on added lines (fallback)
        findings = _parse_imports_regex(file_change)

    return findings


def _parse_imports_ast(
    content: str,
    filepath: str,
) -> list[PythonImportFinding]:
    """
    Parse imports using AST (Abstract Syntax Tree).

    Handles:
    - import statement: import os, sys, requests
    - from statement: from package import module
    - Relative imports: from . import utils
    - Aliased imports: import numpy as np

    Args:
        content: Full Python file content
        filepath: File path for the finding

    Returns:
        List of import findings
    """
    findings: list[PythonImportFinding] = []

    try:
        tree = ast.parse(content)
    except SyntaxError:
        return findings

    for node in ast.walk(tree):
        # Handle: import module1, module2, ...
        if isinstance(node, ast.Import):
            for alias in node.names:
                # Extract top-level module name
                module_name = alias.name.split('.')[0]

                # Skip __future__ imports
                if module_name == '__future__':
                    continue

                findings.append(PythonImportFinding(
                    file=filepath,
                    module=module_name,
                    kind="import",
                    lineno=node.lineno,
                    is_relative=False,
                ))

        # Handle: from module import something
        elif isinstance(node, ast.ImportFrom):
            # Skip relative imports (from . import ...)
            if node.level > 0:
                # Mark as relative but still record
                if node.module:
                    module_name = node.module.split('.')[0]
                    findings.append(PythonImportFinding(
                        file=filepath,
                        module=module_name,
                        kind="from",
                        lineno=node.lineno,
                        is_relative=True,
                    ))
                continue

            # Skip if module is None (happens with: from . import x)
            if node.module is None:
                continue

            # Extract top-level module name
            module_name = node.module.split('.')[0]

            # Skip __future__ imports
            if module_name == '__future__':
                continue

            findings.append(PythonImportFinding(
                file=filepath,
                module=module_name,
                kind="from",
                lineno=node.lineno,
                is_relative=False,
            ))

    return findings


def _parse_imports_regex(
    file_change: DiffFileChange,
) -> list[PythonImportFinding]:
    """
    Parse imports using regex as fallback.

    Less reliable than AST but works when:
    - File doesn't exist yet (new file in staging)
    - File has syntax errors
    - Only have access to diff lines

    Args:
        file_change: DiffFileChange with added lines

    Returns:
        List of import findings
    """
    findings: list[PythonImportFinding] = []

    # Patterns for import statements
    import_pattern = re.compile(r'^\s*import\s+([a-zA-Z_][a-zA-Z0-9_]*)')
    from_pattern = re.compile(r'^\s*from\s+([a-zA-Z_][a-zA-Z0-9_]*)\s+import')
    relative_from_pattern = re.compile(r'^\s*from\s+\.+')

    for lineno, line in file_change.added_lines:
        # Skip relative imports
        if relative_from_pattern.match(line):
            continue

        # Try: import module
        match = import_pattern.match(line)
        if match:
            module_name = match.group(1)

            # Skip __future__
            if module_name == '__future__':
                continue

            findings.append(PythonImportFinding(
                file=file_change.path,
                module=module_name,
                kind="import",
                lineno=lineno,
                raw=line,
                is_relative=False,
            ))
            continue

        # Try: from module import ...
        match = from_pattern.match(line)
        if match:
            module_name = match.group(1)

            # Skip __future__
            if module_name == '__future__':
                continue

            findings.append(PythonImportFinding(
                file=file_change.path,
                module=module_name,
                kind="from",
                lineno=lineno,
                raw=line,
                is_relative=False,
            ))

    return findings


def filter_new_imports(
    findings: list[PythonImportFinding],
    file_change: DiffFileChange,
) -> list[PythonImportFinding]:
    """
    Filter imports to only those on added lines.

    When using AST on full file, we get ALL imports.
    This filters to only imports on newly added lines.

    Args:
        findings: All imports found in file
        file_change: DiffFileChange with added line numbers

    Returns:
        Filtered list of imports only on added lines
    """
    added_line_numbers = {lineno for lineno, _ in file_change.added_lines}

    filtered = []
    for finding in findings:
        if finding.lineno is None or finding.lineno in added_line_numbers:
            filtered.append(finding)

    return filtered


def deduplicate_imports(
    findings: list[PythonImportFinding],
) -> list[PythonImportFinding]:
    """
    Remove duplicate imports (same module in same file).

    Keeps first occurrence.

    Args:
        findings: List of import findings

    Returns:
        Deduplicated list
    """
    seen: set[tuple[str, str]] = set()
    deduplicated = []

    for finding in findings:
        key = (finding.file, finding.module)
        if key not in seen:
            seen.add(key)
            deduplicated.append(finding)

    return deduplicated

