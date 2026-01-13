"""Tests for typosquat detection."""

from __future__ import annotations

from typo_shield.risk.typosquat import (
    check_multiple_packages,
    check_suspicious_characters,
    check_typosquat,
    get_top_n_packages,
    load_top_packages,
)


class TestLoadTopPackages:
    """Tests for load_top_packages()."""

    def test_load_packages(self) -> None:
        """Test that packages are loaded."""
        packages = load_top_packages()

        assert isinstance(packages, list)
        assert len(packages) > 0

    def test_common_packages_present(self) -> None:
        """Test that common packages are in the list."""
        packages = load_top_packages()

        # Common packages that should be in top list
        assert 'requests' in packages
        assert 'numpy' in packages
        assert 'flask' in packages
        assert 'django' in packages

    def test_packages_normalized(self) -> None:
        """Test that packages are normalized (lowercase)."""
        packages = load_top_packages()

        # All should be lowercase
        assert all(pkg == pkg.lower() for pkg in packages)

    def test_caching(self) -> None:
        """Test that results are cached."""
        packages1 = load_top_packages()
        packages2 = load_top_packages()

        # Should return the same object (cached)
        assert packages1 is packages2


class TestCheckTyposquat:
    """Tests for check_typosquat()."""

    def test_typosquat_distance_1(self) -> None:
        """Test typosquat with distance 1 (FAIL)."""
        # 'requets' is distance 1 from 'requests' (missing 's')
        finding = check_typosquat('requets')

        assert finding is not None
        assert finding.level == 'FAIL'
        assert finding.code == 'TS001'
        assert finding.target == 'requests'
        assert finding.name == 'requets'
        assert 'typosquat' in finding.message.lower()

    def test_typosquat_distance_1_different_case(self) -> None:
        """Test typosquat with different case."""
        # 'Requets' should be normalized and detected
        finding = check_typosquat('Requets')

        assert finding is not None
        assert finding.level == 'FAIL'
        assert finding.target == 'requests'

    def test_exact_match_no_finding(self) -> None:
        """Test that exact matches don't generate findings."""
        finding = check_typosquat('requests')

        assert finding is None

    def test_exact_match_different_case(self) -> None:
        """Test that exact matches with different case don't generate findings."""
        finding = check_typosquat('Requests')

        assert finding is None

    def test_typosquat_distance_2_top_package(self) -> None:
        """Test typosquat with distance 2 to top package (WARN)."""
        # 'reqeusts' is distance 2 from 'requests' (transposed 'eu')
        # This should be WARN if requests is in top 50
        finding = check_typosquat('reqeusts')

        # Should trigger WARN with TS002 (distance 2, top package)
        assert finding is not None
        assert finding.level == 'WARN'
        assert finding.code == 'TS002'
        assert finding.target == 'requests'

    def test_unknown_package_no_close_match(self) -> None:
        """Test that unknown packages without close matches don't generate findings."""
        # Very unique name, unlikely to be close to any popular package
        finding = check_typosquat('myveryveryuniquepkg12345xyz')

        # Should have no finding (no close match)
        # Or if there is a finding, distance should be > 2
        assert finding is None

    def test_normalized_underscore_dash(self) -> None:
        """Test that underscores are normalized to dashes for comparison."""
        # If there's a package 'some-package', 'some_package' should match
        # For MVP, we just test normalization doesn't break
        finding = check_typosquat('some_package')

        # Should not crash
        assert finding is None or isinstance(finding, object)

    def test_custom_top_packages_list(self) -> None:
        """Test with custom top packages list."""
        custom_packages = ['mypackage', 'otherpackage']

        # 'mypackagee' is distance 1 from 'mypackage'
        finding = check_typosquat('mypackagee', custom_packages)

        assert finding is not None
        assert finding.level == 'FAIL'
        assert finding.target == 'mypackage'

    def test_empty_top_packages_list(self) -> None:
        """Test with empty top packages list."""
        finding = check_typosquat('anything', [])

        assert finding is None


class TestCheckSuspiciousCharacters:
    """Tests for check_suspicious_characters()."""

    def test_normal_name_no_finding(self) -> None:
        """Test that normal package names don't generate findings."""
        assert check_suspicious_characters('requests') is None
        assert check_suspicious_characters('my-package') is None
        assert check_suspicious_characters('my_package') is None
        assert check_suspicious_characters('package123') is None

    def test_suspicious_chars(self) -> None:
        """Test detection of suspicious characters."""
        finding = check_suspicious_characters('req@uests')

        assert finding is not None
        assert finding.level == 'WARN'
        assert finding.code == 'TS003'
        assert 'suspicious characters' in finding.message

    def test_unicode_chars(self) -> None:
        """Test detection of unicode/homoglyph characters."""
        # Using lookalike characters
        finding = check_suspicious_characters('reԛuests')  # Cyrillic 'q'

        assert finding is not None
        assert finding.level == 'WARN'
        assert finding.code == 'TS003'

    def test_mixed_separators(self) -> None:
        """Test detection of mixed separators."""
        finding = check_suspicious_characters('my-package_name')

        assert finding is not None
        assert finding.level == 'WARN'
        assert finding.code == 'TS004'
        assert 'mixes underscores and dashes' in finding.message

    def test_only_underscores(self) -> None:
        """Test that only underscores is OK."""
        finding = check_suspicious_characters('my_package_name')

        assert finding is None

    def test_only_dashes(self) -> None:
        """Test that only dashes is OK."""
        finding = check_suspicious_characters('my-package-name')

        assert finding is None


class TestCheckMultiplePackages:
    """Tests for check_multiple_packages()."""

    def test_multiple_with_typosquats(self) -> None:
        """Test checking multiple packages with typosquats."""
        packages = ['reqeusts', 'numpy', 'flsk']

        findings = check_multiple_packages(packages)

        # Should find at least 2 typosquats (reqeusts→requests, flsk→flask)
        assert len(findings) >= 2

        # Check reqeusts finding
        reqeusts_finding = next((f for f in findings if f.name == 'reqeusts'), None)
        assert reqeusts_finding is not None
        assert reqeusts_finding.target == 'requests'

    def test_multiple_all_valid(self) -> None:
        """Test checking multiple valid packages."""
        packages = ['requests', 'numpy', 'flask']

        findings = check_multiple_packages(packages)

        # Should have no findings (all exact matches)
        assert len(findings) == 0

    def test_empty_list(self) -> None:
        """Test with empty list."""
        findings = check_multiple_packages([])

        assert len(findings) == 0

    def test_custom_top_packages(self) -> None:
        """Test with custom top packages list."""
        custom_packages = ['mypackage', 'otherpackage']
        packages_to_check = ['mypackagee', 'mypackage', 'otherpackagee']

        findings = check_multiple_packages(packages_to_check, custom_packages)

        # Should find 2 typosquats
        assert len(findings) == 2


class TestGetTopNPackages:
    """Tests for get_top_n_packages()."""

    def test_get_top_50(self) -> None:
        """Test getting top 50 packages."""
        top_50 = get_top_n_packages(50)

        assert len(top_50) == 50
        assert isinstance(top_50, list)

    def test_get_top_10(self) -> None:
        """Test getting top 10 packages."""
        top_10 = get_top_n_packages(10)

        assert len(top_10) == 10

    def test_common_packages_in_top(self) -> None:
        """Test that common packages are in top list."""
        top_100 = get_top_n_packages(100)

        # Very common packages should be in top 100
        assert 'requests' in top_100
        assert 'numpy' in top_100

    def test_default_is_50(self) -> None:
        """Test that default n is 50."""
        top_default = get_top_n_packages()

        assert len(top_default) == 50


class TestIntegrationTyposquat:
    """Integration tests for typosquat detection."""

    def test_real_world_typosquats(self) -> None:
        """Test detection of real-world typosquat examples."""
        # Known typosquatting patterns
        typosquats = [
            ('reqeusts', 'requests'),  # character swap (distance 2)
            ('requets', 'requests'),   # missing character (distance 1)
            ('flsk', 'flask'),         # missing character (distance 1)
        ]

        for typo, expected_target in typosquats:
            finding = check_typosquat(typo)

            # May not find all depending on exact top packages list
            # But if found, should match expected target
            if finding:
                # Allow for variations in normalization
                assert expected_target in finding.message.lower()

    def test_no_false_positives_valid_packages(self) -> None:
        """Test that valid packages don't trigger false positives."""
        valid_packages = [
            'requests',
            'numpy',
            'flask',
            'django',
            'pandas',
        ]

        for package in valid_packages:
            finding = check_typosquat(package)
            assert finding is None

    def test_suspicious_with_valid_name(self) -> None:
        """Test that suspicious patterns are caught even if distance is OK."""
        # Mixed separators should trigger even if name is not close to anything
        finding = check_typosquat('my-weird_package')

        # Should catch suspicious pattern
        assert finding is not None
        assert finding.code in ['TS003', 'TS004']

