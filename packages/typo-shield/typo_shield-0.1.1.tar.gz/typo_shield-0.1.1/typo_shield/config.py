"""
Configuration management.

Handles loading and validating .typo-shield.toml configuration files.
"""

from __future__ import annotations

import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

# Conditional import for toml parser
if sys.version_info >= (3, 11):
    import tomllib
else:
    import tomli as tomllib


@dataclass
class Config:
    """
    Configuration for typo-shield.

    Attributes:
        fail_on: Failure threshold ("fail" or "warn")
        strict_imports: If True, fail on unknown imports (not in stdlib or deps)
        allow_deps: List of package names to allow (skip typosquat checks)
        allow_modules: List of module names to allow (skip import checks)
        exclude_paths: List of glob patterns to exclude from scanning

    Example:
        >>> config = Config(fail_on="warn", strict_imports=True)
        >>> config.fail_on
        'warn'
    """

    fail_on: str = "fail"
    strict_imports: bool = False
    allow_deps: list[str] = field(default_factory=list)
    allow_modules: list[str] = field(default_factory=list)
    exclude_paths: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        """Validate configuration values after initialization."""
        self._validate()

    def _validate(self) -> None:
        """Validate configuration values."""
        # Validate fail_on
        if self.fail_on not in ["fail", "warn"]:
            raise ValueError(
                f"Invalid fail_on value: '{self.fail_on}'. Must be 'fail' or 'warn'."
            )

        # Validate types
        if not isinstance(self.strict_imports, bool):
            raise ValueError(
                f"strict_imports must be a boolean, got: {type(self.strict_imports)}"
            )

        if not isinstance(self.allow_deps, list):
            raise ValueError(
                f"allow_deps must be a list, got: {type(self.allow_deps)}"
            )

        if not isinstance(self.allow_modules, list):
            raise ValueError(
                f"allow_modules must be a list, got: {type(self.allow_modules)}"
            )

        if not isinstance(self.exclude_paths, list):
            raise ValueError(
                f"exclude_paths must be a list, got: {type(self.exclude_paths)}"
            )


def load_config(config_path: Path | None = None) -> Config:
    """
    Load configuration from a TOML file.

    If config_path is None or file doesn't exist, returns default config.

    Args:
        config_path: Path to .typo-shield.toml file (optional)

    Returns:
        Config object

    Raises:
        ValueError: If config file is invalid

    Example:
        >>> config = load_config(Path(".typo-shield.toml"))
        >>> config.fail_on
        'fail'
    """
    # Return default config if no path or file doesn't exist
    if config_path is None or not config_path.exists():
        return Config()

    try:
        with open(config_path, "rb") as f:
            toml_data = tomllib.load(f)
    except Exception as e:
        raise ValueError(f"Failed to parse config file '{config_path}': {e}") from e

    # Extract config values
    config_dict = _parse_config_toml(toml_data)

    # Create and return Config
    try:
        return Config(**config_dict)
    except (ValueError, TypeError) as e:
        raise ValueError(f"Invalid configuration: {e}") from e


def _parse_config_toml(toml_data: dict[str, Any]) -> dict[str, Any]:
    """
    Parse TOML data into Config dictionary.

    Expected format:
    ```toml
    [policy]
    fail_on = "fail"
    strict_imports = false

    [allow]
    deps = ["internal-lib", "private-package"]
    modules = ["internalpkg"]

    [exclude]
    paths = ["tests/**", "docs/**"]
    ```

    Args:
        toml_data: Parsed TOML data

    Returns:
        Dictionary with config values
    """
    config_dict: dict[str, Any] = {}

    # Parse [policy] section
    if "policy" in toml_data:
        policy = toml_data["policy"]

        if "fail_on" in policy:
            config_dict["fail_on"] = policy["fail_on"]

        if "strict_imports" in policy:
            config_dict["strict_imports"] = policy["strict_imports"]

    # Parse [allow] section
    if "allow" in toml_data:
        allow = toml_data["allow"]

        if "deps" in allow:
            config_dict["allow_deps"] = allow["deps"]

        if "modules" in allow:
            config_dict["allow_modules"] = allow["modules"]

    # Parse [exclude] section
    if "exclude" in toml_data:
        exclude = toml_data["exclude"]

        if "paths" in exclude:
            config_dict["exclude_paths"] = exclude["paths"]

    return config_dict


def create_default_config_file(path: Path) -> None:
    """
    Create a default .typo-shield.toml configuration file.

    Args:
        path: Path where to create the config file

    Example:
        >>> create_default_config_file(Path(".typo-shield.toml"))
    """
    default_config = """# typo-shield configuration file
# https://github.com/kszmigiel/typo-shield

[policy]
# Failure threshold: "fail" (only FAIL findings) or "warn" (WARN and FAIL findings)
fail_on = "fail"

# If true, fail on unknown imports (not in stdlib or declared dependencies)
strict_imports = false

[allow]
# Package names to allow (skip typosquat checks)
# Useful for internal/private packages
deps = []

# Module names to allow (skip missing dependency checks)
# Useful for optional dependencies or modules from non-PyPI sources
modules = []

[exclude]
# Glob patterns to exclude from scanning
paths = [
    "tests/**",
    "docs/**",
    "*.pyc",
    "__pycache__/**",
]
"""

    path.write_text(default_config, encoding="utf-8")


def merge_config_with_cli_args(
    config: Config,
    cli_fail_on: str | None = None,
    cli_strict_imports: bool | None = None,
    cli_exclude: list[str] | None = None,
) -> Config:
    """
    Merge configuration from file with CLI arguments.

    CLI arguments take precedence over config file.

    Args:
        config: Base configuration (from file or default)
        cli_fail_on: fail_on from CLI (optional)
        cli_strict_imports: strict_imports from CLI (optional)
        cli_exclude: exclude patterns from CLI (optional)

    Returns:
        Merged Config object

    Example:
        >>> base_config = Config(fail_on="fail")
        >>> merged = merge_config_with_cli_args(base_config, cli_fail_on="warn")
        >>> merged.fail_on
        'warn'
    """
    # Start with config values
    fail_on = config.fail_on
    strict_imports = config.strict_imports
    allow_deps = config.allow_deps.copy()
    allow_modules = config.allow_modules.copy()
    exclude_paths = config.exclude_paths.copy()

    # Override with CLI args if provided
    if cli_fail_on is not None:
        fail_on = cli_fail_on

    if cli_strict_imports is not None:
        strict_imports = cli_strict_imports

    if cli_exclude is not None:
        # Merge CLI exclude patterns
        exclude_paths.extend(cli_exclude)

    return Config(
        fail_on=fail_on,
        strict_imports=strict_imports,
        allow_deps=allow_deps,
        allow_modules=allow_modules,
        exclude_paths=exclude_paths,
    )

