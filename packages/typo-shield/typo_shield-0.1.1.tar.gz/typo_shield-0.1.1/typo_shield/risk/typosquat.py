"""
Typosquat detection module.

Detects potential typosquatting by comparing package names against
a list of popular PyPI packages using Levenshtein distance.
"""

from __future__ import annotations

import re
from functools import lru_cache
from pathlib import Path
from typing import Iterable

from rapidfuzz.distance import Levenshtein

from typo_shield.risk.models import RiskFinding

# Thresholds for typosquat detection
DISTANCE_FAIL_THRESHOLD = 1  # distance <= 1 → FAIL
DISTANCE_WARN_THRESHOLD = 2  # distance == 2 and in top 50 → WARN
TOP_N_FOR_WARN = 50  # Top N packages for stricter checking


@lru_cache(maxsize=1)
def load_top_packages() -> list[str]:
    """
    Load list of top PyPI packages from data file.

    Returns:
        List of package names (normalized)

    Example:
        >>> packages = load_top_packages()
        >>> 'requests' in packages
        True
    """
    data_dir = Path(__file__).parent.parent / "data"
    top_packages_file = data_dir / "top_packages.txt"

    if not top_packages_file.exists():
        return []

    packages = []
    with open(top_packages_file, encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            # Skip empty lines and comments
            if not line or line.startswith('#'):
                continue
            packages.append(line.lower())

    return packages


def check_typosquat(
    name: str,
    top_packages: list[str] | None = None,
) -> RiskFinding | None:
    """
    Check if a package name is a potential typosquat.

    Uses Levenshtein distance to find similar popular packages:
    - distance <= 1 and name != target → FAIL (likely typosquat)
    - distance == 2 and target in top 50 → WARN (possible typosquat)

    Args:
        name: Package name to check (will be normalized)
        top_packages: Optional list of top packages (uses cached if None)

    Returns:
        RiskFinding if typosquat detected, None otherwise

    Examples:
        >>> finding = check_typosquat('reqeusts')  # typo in 'requests'
        >>> finding.level
        'FAIL'
        >>> finding.target
        'requests'

        >>> finding = check_typosquat('requests')  # exact match
        >>> finding is None
        True
    """
    if top_packages is None:
        top_packages = load_top_packages()

    if not top_packages:
        return None

    # Normalize name
    normalized_name = name.lower().replace('_', '-')

    # Check for suspicious characters (homoglyphs, unusual patterns)
    suspicious_chars = check_suspicious_characters(name)
    if suspicious_chars:
        return suspicious_chars

    # Find closest match
    min_distance = float('inf')
    closest_package = None

    for package in top_packages:
        if normalized_name == package:
            # Exact match → not a typosquat
            return None

        distance = Levenshtein.distance(normalized_name, package)

        if distance < min_distance:
            min_distance = distance
            closest_package = package

    if closest_package is None:
        return None

    # Apply thresholds
    if min_distance <= DISTANCE_FAIL_THRESHOLD:
        # Very close → likely typosquat
        return RiskFinding(
            kind="typosquat",
            subject="dep",
            name=name,
            target=closest_package,
            level="FAIL",
            code="TS001",
            message=f"Suspected typosquat: '{name}' is very similar to '{closest_package}' (distance: {min_distance})",
            context={
                "distance": str(min_distance),
                "algorithm": "levenshtein",
            },
        )

    if min_distance == DISTANCE_WARN_THRESHOLD:
        # Check if target is in top N
        top_n_packages = top_packages[:TOP_N_FOR_WARN]
        if closest_package in top_n_packages:
            return RiskFinding(
                kind="typosquat",
                subject="dep",
                name=name,
                target=closest_package,
                level="WARN",
                code="TS002",
                message=f"Possible typosquat: '{name}' is similar to popular package '{closest_package}' (distance: {min_distance})",
                context={
                    "distance": str(min_distance),
                    "algorithm": "levenshtein",
                },
            )

    return None


def check_suspicious_characters(name: str) -> RiskFinding | None:
    """
    Check for suspicious characters in package name.

    Detects:
    - Characters outside [a-z0-9._-]
    - Mixed separators (both _ and - in unusual patterns)

    Args:
        name: Package name to check

    Returns:
        RiskFinding if suspicious patterns detected, None otherwise

    Examples:
        >>> finding = check_suspicious_characters('req_ue-sts')
        >>> finding.level
        'WARN'

        >>> finding = check_suspicious_characters('requests')
        >>> finding is None
        True
    """
    # Check for characters outside allowed set
    if not re.match(r'^[a-zA-Z0-9._-]+$', name):
        return RiskFinding(
            kind="suspicious_chars",
            subject="dep",
            name=name,
            target=None,
            level="WARN",
            code="TS003",
            message=f"Package name '{name}' contains suspicious characters (only a-z, 0-9, ., _, - allowed)",
        )

    # Check for mixed separators (both _ and -)
    has_underscore = '_' in name
    has_dash = '-' in name

    if has_underscore and has_dash:
        return RiskFinding(
            kind="suspicious_pattern",
            subject="dep",
            name=name,
            target=None,
            level="WARN",
            code="TS004",
            message=f"Package name '{name}' mixes underscores and dashes (unusual pattern)",
        )

    return None


def check_multiple_packages(
    names: Iterable[str],
    top_packages: list[str] | None = None,
) -> list[RiskFinding]:
    """
    Check multiple package names for typosquatting.

    Args:
        names: Iterable of package names to check
        top_packages: Optional list of top packages (uses cached if None)

    Returns:
        List of RiskFindings (empty if no typosquats detected)

    Example:
        >>> findings = check_multiple_packages(['reqeusts', 'numpy', 'flsk'])
        >>> len(findings)
        2
        >>> findings[0].target
        'requests'
    """
    if top_packages is None:
        top_packages = load_top_packages()

    findings = []
    for name in names:
        finding = check_typosquat(name, top_packages)
        if finding:
            findings.append(finding)

    return findings


def get_top_n_packages(n: int = 50) -> list[str]:
    """
    Get the top N most popular packages.

    Args:
        n: Number of packages to return

    Returns:
        List of top N package names

    Example:
        >>> top_50 = get_top_n_packages(50)
        >>> len(top_50)
        50
        >>> 'requests' in top_50
        True
    """
    packages = load_top_packages()
    return packages[:n]

