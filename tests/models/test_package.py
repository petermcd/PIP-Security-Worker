"""Code to test the Package model."""

import pytest

from pip_security_worker.models.package import Package


class TestPackageModel(object):
    """
    Set of tests to ensure models are working as expected.
    """

    @pytest.mark.parametrize(
        'package,expected_release_url',
        [
            (
                # Test to ensure the URL is correct for 'Package' when the link ends with a trailing slash.
                Package(
                    name='test',
                    package_url='https://pypi.org/project/contact/',
                ),
                'https://pypi.org/rss/project/contact/releases.xml',
            ),
            (
                # Test to ensure the URL is correct for 'Package' when the link ends without a trailing slash.
                Package(
                    name='test',
                    package_url='https://pypi.org/project/contact',
                ),
                'https://pypi.org/rss/project/contact/releases.xml',
            ),
        ],
    )
    def test_release_url(self, package: Package, expected_release_url: str) -> None:
        """
        Test to ensure the release URL is set correctly.

        Args:
            package: The package URL to be tested.
            expected_release_url: The expected release URL.
        """
        assert package.releases_url == expected_release_url

    @pytest.mark.parametrize(
        'name,package_url,expected_string',
        [
            (
                'contact',
                'https://pypi.org/project/contact/',
                'contact',
            ),
            (
                'monzo-api',
                'https://pypi.org/project/monzo-api/',
                'monzo-api',
            ),
            (
                'Requests',
                'https://pypi.org/project/requests/',
                'Requests',
            ),
        ],
    )
    def test_str(self, name: str, package_url: str, expected_string: str) -> None:
        """
        Test to ensure the string representation is correct.

        Args:
            name: The name of the package.
            package_url: The URL of the package.
            expected_string: The expected string representation.
        """
        package = Package(
            name=name,
            package_url=package_url,
        )
        assert str(package) == expected_string
