"""Tests for configuration management."""

from __future__ import annotations

from pathlib import Path

import pytest

from typo_shield.config import (
    Config,
    create_default_config_file,
    load_config,
    merge_config_with_cli_args,
)


class TestConfig:
    """Tests for Config dataclass."""

    def test_default_config(self) -> None:
        """Test creating config with default values."""
        config = Config()

        assert config.fail_on == "fail"
        assert config.strict_imports is False
        assert config.allow_deps == []
        assert config.allow_modules == []
        assert config.exclude_paths == []

    def test_custom_config(self) -> None:
        """Test creating config with custom values."""
        config = Config(
            fail_on="warn",
            strict_imports=True,
            allow_deps=["internal-lib"],
            allow_modules=["internalpkg"],
            exclude_paths=["tests/**"],
        )

        assert config.fail_on == "warn"
        assert config.strict_imports is True
        assert config.allow_deps == ["internal-lib"]
        assert config.allow_modules == ["internalpkg"]
        assert config.exclude_paths == ["tests/**"]

    def test_invalid_fail_on(self) -> None:
        """Test that invalid fail_on value raises error."""
        with pytest.raises(ValueError, match="Invalid fail_on value"):
            Config(fail_on="invalid")

    def test_invalid_strict_imports_type(self) -> None:
        """Test that invalid strict_imports type raises error."""
        with pytest.raises(ValueError, match="strict_imports must be a boolean"):
            Config(strict_imports="yes")  # type: ignore

    def test_invalid_allow_deps_type(self) -> None:
        """Test that invalid allow_deps type raises error."""
        with pytest.raises(ValueError, match="allow_deps must be a list"):
            Config(allow_deps="not-a-list")  # type: ignore

    def test_invalid_allow_modules_type(self) -> None:
        """Test that invalid allow_modules type raises error."""
        with pytest.raises(ValueError, match="allow_modules must be a list"):
            Config(allow_modules="not-a-list")  # type: ignore

    def test_invalid_exclude_paths_type(self) -> None:
        """Test that invalid exclude_paths type raises error."""
        with pytest.raises(ValueError, match="exclude_paths must be a list"):
            Config(exclude_paths="not-a-list")  # type: ignore


class TestLoadConfig:
    """Tests for load_config()."""

    def test_load_nonexistent_file(self, tmp_path: Path) -> None:
        """Test loading config from nonexistent file returns default."""
        config_path = tmp_path / "nonexistent.toml"

        config = load_config(config_path)

        # Should return default config
        assert config.fail_on == "fail"
        assert config.strict_imports is False

    def test_load_none_path(self) -> None:
        """Test loading config with None path returns default."""
        config = load_config(None)

        assert config.fail_on == "fail"
        assert config.strict_imports is False

    def test_load_valid_config(self, tmp_path: Path) -> None:
        """Test loading valid config file."""
        config_path = tmp_path / ".typo-shield.toml"
        config_path.write_text("""
[policy]
fail_on = "warn"
strict_imports = true

[allow]
deps = ["internal-lib", "private-package"]
modules = ["internalpkg"]

[exclude]
paths = ["tests/**", "docs/**"]
""")

        config = load_config(config_path)

        assert config.fail_on == "warn"
        assert config.strict_imports is True
        assert config.allow_deps == ["internal-lib", "private-package"]
        assert config.allow_modules == ["internalpkg"]
        assert config.exclude_paths == ["tests/**", "docs/**"]

    def test_load_partial_config(self, tmp_path: Path) -> None:
        """Test loading config with only some values set."""
        config_path = tmp_path / ".typo-shield.toml"
        config_path.write_text("""
[policy]
fail_on = "warn"
""")

        config = load_config(config_path)

        # Should have specified value
        assert config.fail_on == "warn"

        # Should have defaults for unspecified values
        assert config.strict_imports is False
        assert config.allow_deps == []

    def test_load_empty_config(self, tmp_path: Path) -> None:
        """Test loading empty config file."""
        config_path = tmp_path / ".typo-shield.toml"
        config_path.write_text("")

        config = load_config(config_path)

        # Should return default config
        assert config.fail_on == "fail"
        assert config.strict_imports is False

    def test_load_invalid_toml(self, tmp_path: Path) -> None:
        """Test loading invalid TOML raises error."""
        config_path = tmp_path / ".typo-shield.toml"
        config_path.write_text("not valid toml [[[")

        with pytest.raises(ValueError, match="Failed to parse config file"):
            load_config(config_path)

    def test_load_invalid_fail_on_value(self, tmp_path: Path) -> None:
        """Test loading config with invalid fail_on value."""
        config_path = tmp_path / ".typo-shield.toml"
        config_path.write_text("""
[policy]
fail_on = "invalid"
""")

        with pytest.raises(ValueError, match="Invalid configuration"):
            load_config(config_path)

    def test_load_config_with_comments(self, tmp_path: Path) -> None:
        """Test loading config with comments."""
        config_path = tmp_path / ".typo-shield.toml"
        config_path.write_text("""
# This is a comment
[policy]
fail_on = "warn"  # inline comment
strict_imports = true

# Another comment
[allow]
deps = ["internal-lib"]
""")

        config = load_config(config_path)

        assert config.fail_on == "warn"
        assert config.strict_imports is True
        assert config.allow_deps == ["internal-lib"]


class TestCreateDefaultConfigFile:
    """Tests for create_default_config_file()."""

    def test_create_default_file(self, tmp_path: Path) -> None:
        """Test creating default config file."""
        config_path = tmp_path / ".typo-shield.toml"

        create_default_config_file(config_path)

        # File should exist
        assert config_path.exists()

        # File should be valid TOML and loadable
        config = load_config(config_path)
        assert config.fail_on == "fail"
        assert config.strict_imports is False

    def test_created_file_has_comments(self, tmp_path: Path) -> None:
        """Test that created file has helpful comments."""
        config_path = tmp_path / ".typo-shield.toml"

        create_default_config_file(config_path)

        content = config_path.read_text()

        # Should have comments explaining options
        assert "#" in content
        assert "policy" in content
        assert "allow" in content
        assert "exclude" in content


class TestMergeConfigWithCliArgs:
    """Tests for merge_config_with_cli_args()."""

    def test_merge_no_cli_args(self) -> None:
        """Test merging with no CLI args returns original config."""
        base_config = Config(fail_on="fail", strict_imports=False)

        merged = merge_config_with_cli_args(base_config)

        assert merged.fail_on == "fail"
        assert merged.strict_imports is False

    def test_merge_fail_on(self) -> None:
        """Test merging fail_on from CLI."""
        base_config = Config(fail_on="fail")

        merged = merge_config_with_cli_args(base_config, cli_fail_on="warn")

        assert merged.fail_on == "warn"

    def test_merge_strict_imports(self) -> None:
        """Test merging strict_imports from CLI."""
        base_config = Config(strict_imports=False)

        merged = merge_config_with_cli_args(base_config, cli_strict_imports=True)

        assert merged.strict_imports is True

    def test_merge_exclude_paths(self) -> None:
        """Test merging exclude paths from CLI."""
        base_config = Config(exclude_paths=["tests/**"])

        merged = merge_config_with_cli_args(
            base_config, cli_exclude=["docs/**", "*.pyc"]
        )

        # Should merge both lists
        assert "tests/**" in merged.exclude_paths
        assert "docs/**" in merged.exclude_paths
        assert "*.pyc" in merged.exclude_paths

    def test_merge_multiple_args(self) -> None:
        """Test merging multiple CLI args."""
        base_config = Config(
            fail_on="fail",
            strict_imports=False,
            exclude_paths=["tests/**"],
        )

        merged = merge_config_with_cli_args(
            base_config,
            cli_fail_on="warn",
            cli_strict_imports=True,
            cli_exclude=["docs/**"],
        )

        assert merged.fail_on == "warn"
        assert merged.strict_imports is True
        assert "tests/**" in merged.exclude_paths
        assert "docs/**" in merged.exclude_paths

    def test_merge_preserves_allow_lists(self) -> None:
        """Test that merging preserves allow lists."""
        base_config = Config(
            allow_deps=["internal-lib"],
            allow_modules=["internalpkg"],
        )

        merged = merge_config_with_cli_args(base_config, cli_fail_on="warn")

        # Allow lists should be preserved
        assert merged.allow_deps == ["internal-lib"]
        assert merged.allow_modules == ["internalpkg"]


class TestConfigIntegration:
    """Integration tests for configuration."""

    def test_full_workflow(self, tmp_path: Path) -> None:
        """Test full workflow: create, load, merge."""
        config_path = tmp_path / ".typo-shield.toml"

        # Create default config
        create_default_config_file(config_path)

        # Load it
        config = load_config(config_path)
        assert config.fail_on == "fail"

        # Merge with CLI args
        merged = merge_config_with_cli_args(config, cli_fail_on="warn")
        assert merged.fail_on == "warn"

    def test_config_with_real_use_case(self, tmp_path: Path) -> None:
        """Test config with realistic use case."""
        config_path = tmp_path / ".typo-shield.toml"
        config_path.write_text("""
[policy]
fail_on = "warn"
strict_imports = true

[allow]
deps = ["company-internal-lib", "legacy-package"]
modules = ["legacy_module"]

[exclude]
paths = [
    "tests/**",
    "docs/**",
    "*.pyc",
    "__pycache__/**",
    "build/**",
    "dist/**",
]
""")

        config = load_config(config_path)

        assert config.fail_on == "warn"
        assert config.strict_imports is True
        assert "company-internal-lib" in config.allow_deps
        assert "legacy_module" in config.allow_modules
        assert len(config.exclude_paths) == 6

