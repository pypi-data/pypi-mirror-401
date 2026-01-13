"""Tests for local modules detection."""

from __future__ import annotations

from pathlib import Path

from typo_shield.mapping.project_modules import (
    clear_cache,
    discover_local_modules,
    discover_local_modules_cached,
    is_local_module,
    is_local_module_cached,
)


class TestDiscoverLocalModules:
    """Tests for discover_local_modules()."""

    def test_flat_layout_with_package(self, tmp_path: Path) -> None:
        """Test discovering packages in flat layout."""
        # Create package structure
        myapp = tmp_path / "myapp"
        myapp.mkdir()
        (myapp / "__init__.py").touch()

        modules = discover_local_modules(tmp_path)

        assert "myapp" in modules

    def test_flat_layout_with_multiple_packages(self, tmp_path: Path) -> None:
        """Test discovering multiple packages."""
        # Create multiple packages
        for name in ["app", "backend", "utils"]:
            pkg = tmp_path / name
            pkg.mkdir()
            (pkg / "__init__.py").touch()

        modules = discover_local_modules(tmp_path)

        assert "app" in modules
        assert "backend" in modules
        assert "utils" in modules

    def test_flat_layout_with_single_file(self, tmp_path: Path) -> None:
        """Test discovering single .py files."""
        (tmp_path / "utils.py").touch()
        (tmp_path / "helpers.py").touch()

        modules = discover_local_modules(tmp_path)

        assert "utils" in modules
        assert "helpers" in modules

    def test_mixed_packages_and_files(self, tmp_path: Path) -> None:
        """Test discovering both packages and single files."""
        # Package
        myapp = tmp_path / "myapp"
        myapp.mkdir()
        (myapp / "__init__.py").touch()

        # Single file
        (tmp_path / "utils.py").touch()

        modules = discover_local_modules(tmp_path)

        assert "myapp" in modules
        assert "utils" in modules

    def test_src_layout(self, tmp_path: Path) -> None:
        """Test discovering packages in src/ layout."""
        src = tmp_path / "src"
        src.mkdir()

        myapp = src / "myapp"
        myapp.mkdir()
        (myapp / "__init__.py").touch()

        modules = discover_local_modules(tmp_path)

        assert "myapp" in modules

    def test_src_layout_with_multiple_packages(self, tmp_path: Path) -> None:
        """Test discovering multiple packages in src/."""
        src = tmp_path / "src"
        src.mkdir()

        for name in ["app", "backend"]:
            pkg = src / name
            pkg.mkdir()
            (pkg / "__init__.py").touch()

        modules = discover_local_modules(tmp_path)

        assert "app" in modules
        assert "backend" in modules

    def test_src_layout_with_single_file(self, tmp_path: Path) -> None:
        """Test discovering single files in src/."""
        src = tmp_path / "src"
        src.mkdir()
        (src / "utils.py").touch()

        modules = discover_local_modules(tmp_path)

        assert "utils" in modules

    def test_both_root_and_src(self, tmp_path: Path) -> None:
        """Test discovering modules in both root and src/."""
        # Root package
        root_pkg = tmp_path / "root_app"
        root_pkg.mkdir()
        (root_pkg / "__init__.py").touch()

        # Src package
        src = tmp_path / "src"
        src.mkdir()
        src_pkg = src / "src_app"
        src_pkg.mkdir()
        (src_pkg / "__init__.py").touch()

        modules = discover_local_modules(tmp_path)

        assert "root_app" in modules
        assert "src_app" in modules

    def test_skip_tests_directory(self, tmp_path: Path) -> None:
        """Test that tests/ directory is skipped."""
        tests = tmp_path / "tests"
        tests.mkdir()
        (tests / "__init__.py").touch()

        modules = discover_local_modules(tmp_path)

        assert "tests" not in modules

    def test_skip_common_directories(self, tmp_path: Path) -> None:
        """Test that common non-package directories are skipped."""
        for name in ["docs", "build", "dist", "venv", "env", "__pycache__"]:
            d = tmp_path / name
            d.mkdir()
            (d / "__init__.py").touch()

        modules = discover_local_modules(tmp_path)

        for name in ["docs", "build", "dist", "venv", "env", "__pycache__"]:
            assert name not in modules

    def test_skip_hidden_directories(self, tmp_path: Path) -> None:
        """Test that hidden directories (starting with .) are skipped."""
        hidden = tmp_path / ".hidden"
        hidden.mkdir()
        (hidden / "__init__.py").touch()

        modules = discover_local_modules(tmp_path)

        assert ".hidden" not in modules

    def test_skip_setup_py(self, tmp_path: Path) -> None:
        """Test that setup.py is not detected as a module."""
        (tmp_path / "setup.py").touch()

        modules = discover_local_modules(tmp_path)

        assert "setup" not in modules

    def test_skip_conftest_py(self, tmp_path: Path) -> None:
        """Test that conftest.py is not detected as a module."""
        (tmp_path / "conftest.py").touch()

        modules = discover_local_modules(tmp_path)

        assert "conftest" not in modules

    def test_directory_without_init_py(self, tmp_path: Path) -> None:
        """Test that directories without __init__.py are not packages."""
        notpkg = tmp_path / "notpkg"
        notpkg.mkdir()
        # No __init__.py

        modules = discover_local_modules(tmp_path)

        assert "notpkg" not in modules

    def test_empty_directory(self, tmp_path: Path) -> None:
        """Test discovering modules in empty directory."""
        modules = discover_local_modules(tmp_path)

        assert len(modules) == 0

    def test_nonexistent_directory(self, tmp_path: Path) -> None:
        """Test with non-existent directory."""
        nonexistent = tmp_path / "does_not_exist"

        modules = discover_local_modules(nonexistent)

        assert len(modules) == 0


class TestIsLocalModule:
    """Tests for is_local_module()."""

    def test_local_package(self, tmp_path: Path) -> None:
        """Test detection of local package."""
        myapp = tmp_path / "myapp"
        myapp.mkdir()
        (myapp / "__init__.py").touch()

        assert is_local_module("myapp", tmp_path) is True

    def test_not_local_package(self, tmp_path: Path) -> None:
        """Test that third-party packages are not detected as local."""
        myapp = tmp_path / "myapp"
        myapp.mkdir()
        (myapp / "__init__.py").touch()

        assert is_local_module("requests", tmp_path) is False
        assert is_local_module("numpy", tmp_path) is False

    def test_local_single_file(self, tmp_path: Path) -> None:
        """Test detection of local single file module."""
        (tmp_path / "utils.py").touch()

        assert is_local_module("utils", tmp_path) is True

    def test_src_layout(self, tmp_path: Path) -> None:
        """Test detection in src/ layout."""
        src = tmp_path / "src"
        src.mkdir()
        myapp = src / "myapp"
        myapp.mkdir()
        (myapp / "__init__.py").touch()

        assert is_local_module("myapp", tmp_path) is True


class TestDiscoverLocalModulesCached:
    """Tests for cached discovery."""

    def test_cache_works(self, tmp_path: Path) -> None:
        """Test that cache returns same results."""
        clear_cache()

        myapp = tmp_path / "myapp"
        myapp.mkdir()
        (myapp / "__init__.py").touch()

        # First call
        modules1 = discover_local_modules_cached(tmp_path)
        assert "myapp" in modules1

        # Second call (should use cache)
        modules2 = discover_local_modules_cached(tmp_path)
        assert "myapp" in modules2

        # Should be the same set
        assert modules1 == modules2

    def test_cache_different_repos(self, tmp_path: Path) -> None:
        """Test that cache is separate for different repos."""
        clear_cache()

        # Repo 1
        repo1 = tmp_path / "repo1"
        repo1.mkdir()
        app1 = repo1 / "app1"
        app1.mkdir()
        (app1 / "__init__.py").touch()

        # Repo 2
        repo2 = tmp_path / "repo2"
        repo2.mkdir()
        app2 = repo2 / "app2"
        app2.mkdir()
        (app2 / "__init__.py").touch()

        modules1 = discover_local_modules_cached(repo1)
        modules2 = discover_local_modules_cached(repo2)

        assert "app1" in modules1
        assert "app1" not in modules2
        assert "app2" in modules2
        assert "app2" not in modules1

    def test_clear_cache(self, tmp_path: Path) -> None:
        """Test that cache can be cleared."""
        clear_cache()

        myapp = tmp_path / "myapp"
        myapp.mkdir()
        (myapp / "__init__.py").touch()

        # Populate cache
        modules1 = discover_local_modules_cached(tmp_path)
        assert "myapp" in modules1

        # Clear cache
        clear_cache()

        # Should work after clearing
        modules2 = discover_local_modules_cached(tmp_path)
        assert "myapp" in modules2


class TestIsLocalModuleCached:
    """Tests for cached is_local_module()."""

    def test_cached_detection(self, tmp_path: Path) -> None:
        """Test cached local module detection."""
        clear_cache()

        myapp = tmp_path / "myapp"
        myapp.mkdir()
        (myapp / "__init__.py").touch()

        # First call
        assert is_local_module_cached("myapp", tmp_path) is True

        # Second call (should use cache)
        assert is_local_module_cached("myapp", tmp_path) is True

        # Non-local module
        assert is_local_module_cached("requests", tmp_path) is False

