"""
Module to distribution name mapping.

Maps Python module names to their PyPI distribution names.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Literal


@dataclass
class MappedImport:
    """
    Represents a module mapped to its distribution name.

    Attributes:
        module: Original module name (e.g., 'PIL')
        dist_name: PyPI distribution name (e.g., 'Pillow')
        confidence: High if from known aliases, low if assumed equal
        reason: Explanation of the mapping
    """
    module: str
    dist_name: str
    confidence: Literal["high", "low"]
    reason: str


# Cache for loaded aliases
_aliases_cache: dict[str, str] | None = None


def load_module_aliases() -> dict[str, str]:
    """
    Load module to distribution name aliases from JSON file.

    Returns:
        Dictionary mapping module names to distribution names

    Example:
        >>> aliases = load_module_aliases()
        >>> aliases['PIL']
        'Pillow'
    """
    global _aliases_cache

    if _aliases_cache is not None:
        return _aliases_cache

    # Get path to data file
    data_dir = Path(__file__).parent.parent / "data"
    aliases_file = data_dir / "module_dist_aliases.json"

    if not aliases_file.exists():
        # Return empty dict if file doesn't exist
        _aliases_cache = {}
        return _aliases_cache

    try:
        with open(aliases_file, encoding='utf-8') as f:
            _aliases_cache = json.load(f)
    except (json.JSONDecodeError, OSError):
        _aliases_cache = {}

    return _aliases_cache


def map_module_to_dist(module: str) -> MappedImport:
    """
    Map a module name to its PyPI distribution name.

    Strategy:
    1. Check known aliases (high confidence)
    2. Assume module == distribution name (low confidence)

    Args:
        module: Module name (e.g., 'PIL', 'requests')

    Returns:
        MappedImport with distribution name and confidence

    Examples:
        >>> mapped = map_module_to_dist('PIL')
        >>> mapped.dist_name
        'Pillow'
        >>> mapped.confidence
        'high'

        >>> mapped = map_module_to_dist('requests')
        >>> mapped.dist_name
        'requests'
        >>> mapped.confidence
        'low'
    """
    aliases = load_module_aliases()

    # Check if module is in known aliases
    if module in aliases:
        return MappedImport(
            module=module,
            dist_name=aliases[module],
            confidence="high",
            reason=f"Known alias: {module} → {aliases[module]}",
        )

    # Case-insensitive check
    module_lower = module.lower()
    for alias_module, dist_name in aliases.items():
        if alias_module.lower() == module_lower:
            return MappedImport(
                module=module,
                dist_name=dist_name,
                confidence="high",
                reason=f"Known alias (case-insensitive): {module} → {dist_name}",
            )

    # Default: assume module name equals distribution name
    # This works for most packages (requests, numpy, pandas, etc.)
    return MappedImport(
        module=module,
        dist_name=module,
        confidence="low",
        reason="Assumed module name equals distribution name",
    )


def map_modules_to_dists(modules: list[str]) -> list[MappedImport]:
    """
    Map multiple modules to their distribution names.

    Args:
        modules: List of module names

    Returns:
        List of MappedImport objects

    Example:
        >>> modules = ['PIL', 'requests', 'cv2']
        >>> mapped = map_modules_to_dists(modules)
        >>> [m.dist_name for m in mapped]
        ['Pillow', 'requests', 'opencv-python']
    """
    return [map_module_to_dist(module) for module in modules]


def get_dist_name(module: str) -> str:
    """
    Get distribution name for a module (convenience function).

    Args:
        module: Module name

    Returns:
        Distribution name

    Example:
        >>> get_dist_name('PIL')
        'Pillow'
        >>> get_dist_name('requests')
        'requests'
    """
    mapped = map_module_to_dist(module)
    return mapped.dist_name


def normalize_dist_name(name: str) -> str:
    """
    Normalize a distribution name according to PyPI rules.

    - Convert to lowercase
    - Replace _ and . with -

    Args:
        name: Distribution name

    Returns:
        Normalized name

    Example:
        >>> normalize_dist_name('Pillow')
        'pillow'
        >>> normalize_dist_name('scikit_learn')
        'scikit-learn'
    """
    normalized = name.lower()
    normalized = normalized.replace('_', '-')
    normalized = normalized.replace('.', '-')
    return normalized


def are_same_package(name1: str, name2: str) -> bool:
    """
    Check if two package names refer to the same package.

    Compares normalized versions of the names.

    Args:
        name1: First package name
        name2: Second package name

    Returns:
        True if they refer to the same package

    Example:
        >>> are_same_package('Pillow', 'pillow')
        True
        >>> are_same_package('scikit_learn', 'scikit-learn')
        True
        >>> are_same_package('requests', 'numpy')
        False
    """
    return normalize_dist_name(name1) == normalize_dist_name(name2)


def clear_cache() -> None:
    """
    Clear the aliases cache.

    Useful for testing or when the aliases file is updated.
    """
    global _aliases_cache
    _aliases_cache = None

