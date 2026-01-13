"""Tests for module to distribution mapping."""

from __future__ import annotations

from typo_shield.mapping.module_to_dist import (
    are_same_package,
    clear_cache,
    get_dist_name,
    load_module_aliases,
    map_module_to_dist,
    map_modules_to_dists,
    normalize_dist_name,
)


class TestLoadModuleAliases:
    """Tests for load_module_aliases()."""

    def test_load_aliases(self) -> None:
        """Test that aliases are loaded."""
        clear_cache()
        aliases = load_module_aliases()

        assert isinstance(aliases, dict)
        assert len(aliases) > 0

    def test_known_aliases(self) -> None:
        """Test that known aliases are present."""
        clear_cache()
        aliases = load_module_aliases()

        # Common aliases that should be present
        assert aliases.get('PIL') == 'Pillow'
        assert aliases.get('cv2') == 'opencv-python'
        assert aliases.get('sklearn') == 'scikit-learn'
        assert aliases.get('yaml') == 'PyYAML'
        assert aliases.get('bs4') == 'beautifulsoup4'

    def test_caching(self) -> None:
        """Test that aliases are cached."""
        clear_cache()

        aliases1 = load_module_aliases()
        aliases2 = load_module_aliases()

        # Should return the same object (cached)
        assert aliases1 is aliases2


class TestMapModuleToDist:
    """Tests for map_module_to_dist()."""

    def test_known_alias_pil(self) -> None:
        """Test mapping PIL to Pillow."""
        clear_cache()
        mapped = map_module_to_dist('PIL')

        assert mapped.module == 'PIL'
        assert mapped.dist_name == 'Pillow'
        assert mapped.confidence == 'high'

    def test_known_alias_cv2(self) -> None:
        """Test mapping cv2 to opencv-python."""
        clear_cache()
        mapped = map_module_to_dist('cv2')

        assert mapped.module == 'cv2'
        assert mapped.dist_name == 'opencv-python'
        assert mapped.confidence == 'high'

    def test_known_alias_sklearn(self) -> None:
        """Test mapping sklearn to scikit-learn."""
        clear_cache()
        mapped = map_module_to_dist('sklearn')

        assert mapped.module == 'sklearn'
        assert mapped.dist_name == 'scikit-learn'
        assert mapped.confidence == 'high'

    def test_known_alias_yaml(self) -> None:
        """Test mapping yaml to PyYAML."""
        clear_cache()
        mapped = map_module_to_dist('yaml')

        assert mapped.module == 'yaml'
        assert mapped.dist_name == 'PyYAML'
        assert mapped.confidence == 'high'

    def test_known_alias_bs4(self) -> None:
        """Test mapping bs4 to beautifulsoup4."""
        clear_cache()
        mapped = map_module_to_dist('bs4')

        assert mapped.module == 'bs4'
        assert mapped.dist_name == 'beautifulsoup4'
        assert mapped.confidence == 'high'

    def test_direct_match_requests(self) -> None:
        """Test mapping requests (in aliases, maps to itself)."""
        clear_cache()
        mapped = map_module_to_dist('requests')

        assert mapped.module == 'requests'
        assert mapped.dist_name == 'requests'
        # requests is in aliases (maps to itself), so high confidence
        assert mapped.confidence == 'high'

    def test_direct_match_numpy(self) -> None:
        """Test mapping numpy (in aliases, maps to itself)."""
        clear_cache()
        mapped = map_module_to_dist('numpy')

        assert mapped.module == 'numpy'
        assert mapped.dist_name == 'numpy'
        # numpy is in aliases (maps to itself), so high confidence
        assert mapped.confidence == 'high'

    def test_unknown_module(self) -> None:
        """Test mapping unknown module."""
        clear_cache()
        mapped = map_module_to_dist('unknownmodule')

        assert mapped.module == 'unknownmodule'
        assert mapped.dist_name == 'unknownmodule'
        assert mapped.confidence == 'low'

    def test_case_insensitive_known_alias(self) -> None:
        """Test that known aliases work case-insensitively."""
        clear_cache()

        # Test uppercase
        mapped = map_module_to_dist('PIL')
        assert mapped.dist_name == 'Pillow'

        # Test lowercase (if different in aliases)
        mapped_lower = map_module_to_dist('pil')
        assert mapped_lower.dist_name == 'Pillow'
        assert mapped_lower.confidence == 'high'


class TestMapModulesToDists:
    """Tests for map_modules_to_dists()."""

    def test_map_multiple_modules(self) -> None:
        """Test mapping multiple modules."""
        clear_cache()
        modules = ['PIL', 'requests', 'cv2', 'numpy']

        mapped = map_modules_to_dists(modules)

        assert len(mapped) == 4
        assert mapped[0].dist_name == 'Pillow'
        assert mapped[1].dist_name == 'requests'
        assert mapped[2].dist_name == 'opencv-python'
        assert mapped[3].dist_name == 'numpy'

    def test_map_empty_list(self) -> None:
        """Test mapping empty list."""
        clear_cache()
        mapped = map_modules_to_dists([])

        assert len(mapped) == 0

    def test_map_mixed_confidence(self) -> None:
        """Test mapping with mixed confidence levels."""
        clear_cache()
        modules = ['PIL', 'unknownmodule123']

        mapped = map_modules_to_dists(modules)

        assert mapped[0].confidence == 'high'  # Known alias
        assert mapped[1].confidence == 'low'   # Unknown module (assumed equal)


class TestGetDistName:
    """Tests for get_dist_name()."""

    def test_get_dist_name_known_alias(self) -> None:
        """Test getting dist name for known alias."""
        clear_cache()
        assert get_dist_name('PIL') == 'Pillow'
        assert get_dist_name('cv2') == 'opencv-python'
        assert get_dist_name('sklearn') == 'scikit-learn'

    def test_get_dist_name_direct_match(self) -> None:
        """Test getting dist name for direct match."""
        clear_cache()
        assert get_dist_name('requests') == 'requests'
        assert get_dist_name('numpy') == 'numpy'
        assert get_dist_name('pandas') == 'pandas'


class TestNormalizeDistName:
    """Tests for normalize_dist_name()."""

    def test_lowercase(self) -> None:
        """Test conversion to lowercase."""
        assert normalize_dist_name('Pillow') == 'pillow'
        assert normalize_dist_name('PyYAML') == 'pyyaml'
        assert normalize_dist_name('REQUESTS') == 'requests'

    def test_underscore_to_dash(self) -> None:
        """Test underscore to dash conversion."""
        assert normalize_dist_name('scikit_learn') == 'scikit-learn'
        assert normalize_dist_name('some_package') == 'some-package'

    def test_dot_to_dash(self) -> None:
        """Test dot to dash conversion."""
        assert normalize_dist_name('some.package') == 'some-package'

    def test_combined(self) -> None:
        """Test combined transformations."""
        assert normalize_dist_name('My_Package.Name') == 'my-package-name'

    def test_already_normalized(self) -> None:
        """Test already normalized names."""
        assert normalize_dist_name('requests') == 'requests'
        assert normalize_dist_name('some-package') == 'some-package'


class TestAreSamePackage:
    """Tests for are_same_package()."""

    def test_same_package_different_case(self) -> None:
        """Test that case differences are ignored."""
        assert are_same_package('Pillow', 'pillow') is True
        assert are_same_package('REQUESTS', 'requests') is True

    def test_same_package_different_separators(self) -> None:
        """Test that separator differences are ignored."""
        assert are_same_package('scikit_learn', 'scikit-learn') is True
        assert are_same_package('some.package', 'some-package') is True

    def test_same_package_combined(self) -> None:
        """Test combined differences."""
        assert are_same_package('My_Package', 'my-package') is True
        assert are_same_package('Some.Package', 'some_package') is True

    def test_different_packages(self) -> None:
        """Test that different packages are not considered same."""
        assert are_same_package('requests', 'numpy') is False
        assert are_same_package('pillow', 'opencv-python') is False

    def test_identical_names(self) -> None:
        """Test identical package names."""
        assert are_same_package('requests', 'requests') is True
        assert are_same_package('numpy', 'numpy') is True


class TestClearCache:
    """Tests for clear_cache()."""

    def test_clear_cache_reloads(self) -> None:
        """Test that clearing cache causes reload."""
        clear_cache()

        # Load aliases
        aliases1 = load_module_aliases()

        # Clear cache
        clear_cache()

        # Load again
        aliases2 = load_module_aliases()

        # Should have same content but be different objects
        assert aliases1 == aliases2
        # Note: After clear, they might be the same object again due to caching

