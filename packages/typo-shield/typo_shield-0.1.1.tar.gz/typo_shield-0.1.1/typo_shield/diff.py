"""
Parser for unified diff format.

Extracts added lines per file from git diff output.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field


@dataclass
class DiffFileChange:
    """
    Represents changes in a single file from diff.

    Attributes:
        path: File path relative to repo root
        added_lines: List of (line_number, content) tuples for added lines
        is_new: True if the file is newly created (was /dev/null)
    """
    path: str
    added_lines: list[tuple[int | None, str]] = field(default_factory=list)
    is_new: bool = False


def parse_unified_diff(diff_text: str) -> list[DiffFileChange]:
    """
    Parse unified diff into structured file changes.

    Parses git diff output (--unified=0 format) and extracts:
    - File paths
    - Added lines with line numbers
    - Whether files are new

    Args:
        diff_text: Output from git diff command

    Returns:
        List of DiffFileChange objects, one per modified file

    Example:
        >>> diff = '''diff --git a/test.py b/test.py
        ... index abc..def 100644
        ... --- a/test.py
        ... +++ b/test.py
        ... @@ -1,0 +2,2 @@
        ... +import requests
        ... +import numpy
        ... '''
        >>> changes = parse_unified_diff(diff)
        >>> changes[0].path
        'test.py'
        >>> len(changes[0].added_lines)
        2
    """
    changes: dict[str, DiffFileChange] = {}
    current_file: str | None = None
    current_line_no: int | None = None

    # Regex patterns
    file_header_pattern = re.compile(r'^\+\+\+ b/(.+)$')
    dev_null_pattern = re.compile(r'^--- (?:a/)?/?dev/null$')  # Match "--- /dev/null", "--- a/dev/null", and "--- a//dev/null"
    deleted_file_pattern = re.compile(r'^\+\+\+ b/?dev/null$')  # Match "+++ b/dev/null" or "+++ b//dev/null"
    hunk_header_pattern = re.compile(r'^@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@')

    lines = diff_text.split('\n')

    for i, line in enumerate(lines):
        # File header: +++ b/path/to/file
        match = file_header_pattern.match(line)
        if match:
            filepath = match.group(1)

            # Skip /dev/null (deleted files) - check the full line
            if deleted_file_pattern.match(line):
                current_file = None
                continue

            # Normalize Windows paths
            filepath = filepath.replace('\\', '/')

            # Check if this is a new file (previous line was "--- /dev/null" or "--- a/dev/null")
            is_new_file = i > 0 and dev_null_pattern.match(lines[i - 1]) is not None

            current_file = filepath
            if current_file not in changes:
                changes[current_file] = DiffFileChange(
                    path=current_file,
                    is_new=is_new_file,
                )
            continue

        # Hunk header: @@ -a,b +c,d @@
        match = hunk_header_pattern.match(line)
        if match and current_file:
            # Extract start line number for new file (+c part)
            new_start = int(match.group(3))
            current_line_no = new_start
            continue

        # Added line: starts with + (but not +++ which is file header)
        if line.startswith('+') and not line.startswith('+++'):
            if current_file and current_file in changes:
                # Remove the leading '+'
                content = line[1:]

                # Add to changes
                changes[current_file].added_lines.append((current_line_no, content))

                # Increment line number for next line
                if current_line_no is not None:
                    current_line_no += 1

    return list(changes.values())


def filter_files_by_extension(
    changes: list[DiffFileChange],
    extensions: set[str],
) -> list[DiffFileChange]:
    """
    Filter file changes by file extension.

    Args:
        changes: List of file changes
        extensions: Set of extensions to keep (e.g., {'.py', '.txt', '.toml'})

    Returns:
        Filtered list of changes

    Example:
        >>> changes = [
        ...     DiffFileChange(path='test.py'),
        ...     DiffFileChange(path='README.md'),
        ... ]
        >>> filtered = filter_files_by_extension(changes, {'.py'})
        >>> len(filtered)
        1
        >>> filtered[0].path
        'test.py'
    """
    filtered = []
    for change in changes:
        for ext in extensions:
            if change.path.endswith(ext):
                filtered.append(change)
                break
    return filtered


def filter_files_by_pattern(
    changes: list[DiffFileChange],
    exclude_patterns: list[str],
) -> list[DiffFileChange]:
    """
    Filter out files matching exclude patterns (glob-style).

    Args:
        changes: List of file changes
        exclude_patterns: List of glob patterns to exclude

    Returns:
        Filtered list of changes

    Example:
        >>> changes = [
        ...     DiffFileChange(path='src/app.py'),
        ...     DiffFileChange(path='tests/test_app.py'),
        ... ]
        >>> filtered = filter_files_by_pattern(changes, ['tests/**'])
        >>> len(filtered)
        1
        >>> filtered[0].path
        'src/app.py'
    """
    from fnmatch import fnmatch

    filtered = []
    for change in changes:
        should_exclude = False
        for pattern in exclude_patterns:
            # Support both "tests/**" and "**/tests/**"
            if not pattern.startswith('**/'):
                pattern = '**/' + pattern

            if fnmatch(change.path, pattern) or fnmatch(change.path, pattern.removeprefix('**/')):
                should_exclude = True
                break

        if not should_exclude:
            filtered.append(change)

    return filtered

