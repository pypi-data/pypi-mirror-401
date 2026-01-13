"""
Local project modules detection.

Detects whether a module is part of the local project.
"""

from __future__ import annotations

from pathlib import Path


def discover_local_modules(repo_root: Path) -> set[str]:
    """
    Discover top-level modules that are part of the local project.

    Searches for:
    1. Directories with __init__.py in the root
    2. Directories with __init__.py in src/ (src layout)
    3. Single .py files in the root

    Args:
        repo_root: Path to repository root

    Returns:
        Set of top-level module names

    Example:
        >>> # For a project with:
        >>> # myapp/__init__.py
        >>> # utils.py
        >>> # src/backend/__init__.py
        >>> discover_local_modules(Path("/repo"))
        {'myapp', 'utils', 'backend'}
    """
    modules: set[str] = set()

    if not repo_root.exists():
        return modules

    # Strategy 1: Scan root directory for packages and modules
    try:
        for item in repo_root.iterdir():
            # Skip hidden files/directories
            if item.name.startswith('.'):
                continue

            # Skip common non-package directories
            if item.name in {'tests', 'docs', 'build', 'dist', '__pycache__', 'venv', 'env'}:
                continue

            # Directory with __init__.py = package
            if item.is_dir():
                init_file = item / '__init__.py'
                if init_file.exists():
                    modules.add(item.name)
            # Single .py file = module
            elif item.is_file() and item.suffix == '.py':
                # Remove .py extension to get module name
                module_name = item.stem
                # Skip setup.py, conftest.py, etc.
                if module_name not in {'setup', 'conftest', '__pycache__'}:
                    modules.add(module_name)
    except (OSError, PermissionError):
        pass

    # Strategy 2: Check for src/ layout
    src_dir = repo_root / 'src'
    if src_dir.exists() and src_dir.is_dir():
        try:
            for item in src_dir.iterdir():
                # Skip hidden files/directories
                if item.name.startswith('.'):
                    continue

                # Directory with __init__.py = package
                if item.is_dir():
                    init_file = item / '__init__.py'
                    if init_file.exists():
                        modules.add(item.name)
                # Single .py file in src/
                elif item.is_file() and item.suffix == '.py':
                    module_name = item.stem
                    if module_name not in {'setup', 'conftest'}:
                        modules.add(module_name)
        except (OSError, PermissionError):
            pass

    return modules


def is_local_module(module: str, repo_root: Path) -> bool:
    """
    Check if a module is part of the local project.

    Args:
        module: Top-level module name
        repo_root: Path to repository root

    Returns:
        True if the module is local to the project, False otherwise

    Example:
        >>> is_local_module('myapp', Path("/repo"))
        True
        >>> is_local_module('requests', Path("/repo"))
        False
    """
    local_modules = discover_local_modules(repo_root)
    return module in local_modules


# Simple cache to avoid repeated filesystem scans
_cache: dict[Path, set[str]] = {}


def discover_local_modules_cached(repo_root: Path) -> set[str]:
    """
    Discover local modules with caching.

    Same as discover_local_modules() but caches results per repo_root.

    Args:
        repo_root: Path to repository root

    Returns:
        Set of top-level module names
    """
    # Resolve to absolute path for cache key
    repo_root = repo_root.resolve()

    if repo_root not in _cache:
        _cache[repo_root] = discover_local_modules(repo_root)

    return _cache[repo_root]


def is_local_module_cached(module: str, repo_root: Path) -> bool:
    """
    Check if a module is local with caching.

    Same as is_local_module() but uses cached discovery.

    Args:
        module: Top-level module name
        repo_root: Path to repository root

    Returns:
        True if the module is local to the project, False otherwise
    """
    local_modules = discover_local_modules_cached(repo_root)
    return module in local_modules


def clear_cache() -> None:
    """
    Clear the module discovery cache.

    Useful for testing or when the project structure changes.
    """
    _cache.clear()

