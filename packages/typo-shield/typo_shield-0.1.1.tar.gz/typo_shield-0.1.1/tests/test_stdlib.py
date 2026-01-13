"""Tests for stdlib detection."""

from __future__ import annotations

import sys

from typo_shield.mapping.stdlib import (
    filter_stdlib_modules,
    get_stdlib_modules,
    is_stdlib,
    separate_stdlib_and_third_party,
)


class TestIsStdlib:
    """Tests for is_stdlib()."""

    def test_common_stdlib_modules(self) -> None:
        """Test detection of common stdlib modules."""
        common_stdlib = [
            'os',
            'sys',
            'json',
            're',
            'collections',
            'itertools',
            'functools',
            'pathlib',
            'typing',
            'datetime',
            'math',
            'random',
            'subprocess',
            'threading',
            'asyncio',
        ]

        for module in common_stdlib:
            assert is_stdlib(module), f"{module} should be detected as stdlib"

    def test_common_third_party_modules(self) -> None:
        """Test that third-party modules are not detected as stdlib."""
        third_party = [
            'requests',
            'numpy',
            'pandas',
            'django',
            'flask',
            'pytest',
            'pillow',
            'matplotlib',
            'scipy',
            'tensorflow',
        ]

        for module in third_party:
            assert not is_stdlib(module), f"{module} should NOT be detected as stdlib"

    def test_case_insensitive(self) -> None:
        """Test that detection is case-insensitive."""
        assert is_stdlib('os')
        assert is_stdlib('OS')
        assert is_stdlib('Os')

        assert not is_stdlib('requests')
        assert not is_stdlib('REQUESTS')
        assert not is_stdlib('Requests')

    def test_http_modules(self) -> None:
        """Test HTTP-related stdlib modules."""
        assert is_stdlib('http')
        assert is_stdlib('urllib')
        assert is_stdlib('html')

        # requests is third-party
        assert not is_stdlib('requests')

    def test_xml_modules(self) -> None:
        """Test XML-related stdlib modules."""
        assert is_stdlib('xml')
        assert is_stdlib('xmlrpc')

    def test_email_modules(self) -> None:
        """Test email-related stdlib modules."""
        assert is_stdlib('email')
        assert is_stdlib('smtplib')
        assert is_stdlib('imaplib')

    def test_dataclasses(self) -> None:
        """Test dataclasses (Python 3.7+)."""
        assert is_stdlib('dataclasses')

    def test_typing(self) -> None:
        """Test typing module."""
        assert is_stdlib('typing')

        # Note: typing_extensions is third-party
        # but we include it in fallback for compatibility
        # (it's sometimes considered quasi-stdlib)

    def test_pathlib(self) -> None:
        """Test pathlib (Python 3.4+)."""
        assert is_stdlib('pathlib')

    def test_asyncio(self) -> None:
        """Test asyncio (Python 3.4+)."""
        assert is_stdlib('asyncio')

    def test_tomllib(self) -> None:
        """Test tomllib (Python 3.11+)."""
        # tomllib is only in 3.11+
        if sys.version_info >= (3, 11):
            assert is_stdlib('tomllib')

    def test_zoneinfo(self) -> None:
        """Test zoneinfo (Python 3.9+)."""
        if sys.version_info >= (3, 9):
            assert is_stdlib('zoneinfo')


class TestGetStdlibModules:
    """Tests for get_stdlib_modules()."""

    def test_returns_set(self) -> None:
        """Test that it returns a set."""
        stdlib = get_stdlib_modules()
        assert isinstance(stdlib, set)

    def test_contains_common_modules(self) -> None:
        """Test that the set contains common stdlib modules."""
        stdlib = get_stdlib_modules()

        assert 'os' in stdlib
        assert 'sys' in stdlib
        assert 'json' in stdlib
        assert 're' in stdlib

    def test_not_empty(self) -> None:
        """Test that the set is not empty."""
        stdlib = get_stdlib_modules()
        assert len(stdlib) > 0

    def test_has_reasonable_size(self) -> None:
        """Test that the set has a reasonable number of modules."""
        stdlib = get_stdlib_modules()
        # Should have at least 100 modules (conservative estimate)
        assert len(stdlib) > 100

    def test_consistency_with_is_stdlib(self) -> None:
        """Test that get_stdlib_modules() is consistent with is_stdlib()."""
        stdlib = get_stdlib_modules()

        # Test known modules that should definitely be in stdlib
        known_stdlib = ['os', 'sys', 'json', 're', 'pathlib']
        for module in known_stdlib:
            assert module in stdlib, f"{module} should be in stdlib set"
            assert is_stdlib(module), f"{module} should be detected by is_stdlib()"


class TestFilterStdlibModules:
    """Tests for filter_stdlib_modules()."""

    def test_filter_mixed_list(self) -> None:
        """Test filtering a mixed list of stdlib and third-party modules."""
        modules = ['os', 'requests', 'sys', 'numpy', 'json', 'pandas']

        filtered = filter_stdlib_modules(modules)

        assert 'os' not in filtered
        assert 'sys' not in filtered
        assert 'json' not in filtered
        assert 'requests' in filtered
        assert 'numpy' in filtered
        assert 'pandas' in filtered

    def test_filter_all_stdlib(self) -> None:
        """Test filtering a list of only stdlib modules."""
        modules = ['os', 'sys', 'json', 're']

        filtered = filter_stdlib_modules(modules)

        assert len(filtered) == 0

    def test_filter_all_third_party(self) -> None:
        """Test filtering a list of only third-party modules."""
        modules = ['requests', 'numpy', 'pandas']

        filtered = filter_stdlib_modules(modules)

        assert len(filtered) == 3
        assert set(filtered) == {'requests', 'numpy', 'pandas'}

    def test_filter_empty_list(self) -> None:
        """Test filtering an empty list."""
        filtered = filter_stdlib_modules([])
        assert len(filtered) == 0

    def test_preserves_order(self) -> None:
        """Test that the order of modules is preserved."""
        modules = ['requests', 'os', 'numpy', 'sys', 'pandas']

        filtered = filter_stdlib_modules(modules)

        # Should preserve order of third-party modules
        assert filtered == ['requests', 'numpy', 'pandas']


class TestSeparateStdlibAndThirdParty:
    """Tests for separate_stdlib_and_third_party()."""

    def test_separate_mixed_list(self) -> None:
        """Test separating a mixed list."""
        modules = ['os', 'requests', 'sys', 'numpy', 'json']

        stdlib, third_party = separate_stdlib_and_third_party(modules)

        assert set(stdlib) == {'os', 'sys', 'json'}
        assert set(third_party) == {'requests', 'numpy'}

    def test_separate_all_stdlib(self) -> None:
        """Test separating a list of only stdlib modules."""
        modules = ['os', 'sys', 'json']

        stdlib, third_party = separate_stdlib_and_third_party(modules)

        assert set(stdlib) == {'os', 'sys', 'json'}
        assert len(third_party) == 0

    def test_separate_all_third_party(self) -> None:
        """Test separating a list of only third-party modules."""
        modules = ['requests', 'numpy', 'pandas']

        stdlib, third_party = separate_stdlib_and_third_party(modules)

        assert len(stdlib) == 0
        assert set(third_party) == {'requests', 'numpy', 'pandas'}

    def test_separate_empty_list(self) -> None:
        """Test separating an empty list."""
        stdlib, third_party = separate_stdlib_and_third_party([])

        assert len(stdlib) == 0
        assert len(third_party) == 0

    def test_preserves_order(self) -> None:
        """Test that the order is preserved in both lists."""
        modules = ['requests', 'os', 'numpy', 'sys', 'pandas', 'json']

        stdlib, third_party = separate_stdlib_and_third_party(modules)

        assert stdlib == ['os', 'sys', 'json']
        assert third_party == ['requests', 'numpy', 'pandas']

    def test_returns_tuple(self) -> None:
        """Test that it returns a tuple."""
        result = separate_stdlib_and_third_party(['os', 'requests'])

        assert isinstance(result, tuple)
        assert len(result) == 2

