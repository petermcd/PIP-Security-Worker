"""Code to test the models.py module."""

from datetime import datetime

import pytest

from pip_security_worker.models.package import Package
from pip_security_worker.models.package_version import PackageVersion


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
            (
                # Test to ensure the URL is correct for PackageVersion when the link ends with a trailing slash.
                PackageVersion(
                    name='test',
                    version='1.0.0',
                    url='https://pypi.org/project/contact/1.3.9/',
                    published=datetime.now(),
                ),
                'https://pypi.org/rss/project/contact/releases.xml',
            ),
            (
                # Test to ensure the URL is correct for PackageVersion when the link ends without a trailing slash.
                PackageVersion(
                    name='test',
                    version='1.0.0',
                    url='https://pypi.org/project/contact/1.3.9',
                    published=datetime.now(),
                ),
                'https://pypi.org/rss/project/contact/releases.xml',
            ),
        ],
    )
    def test_release_url(self, package: Package | PackageVersion, expected_release_url: str):
        """
        Test to ensure the release URL is set correctly.

        Args:
            url: The package URL to be tested.
            expected_release_url: The expected release URL.
        """
        assert package.releases_url == expected_release_url

    @pytest.mark.parametrize(
        'url,expected_release_detail_json_url',
        [
            (
                # Test to ensure the JSON URL is correct when the link ends with a trailing slash.
                'https://pypi.org/project/contact/1.3.9/',
                'https://pypi.python.org/pypi/contact/1.3.9/json'
            ),
            (
                # Test to ensure the JSON URL is correct when the link ends without a trailing slash.
                'https://pypi.org/project/contact/1.3.9',
                'https://pypi.python.org/pypi/contact/1.3.9/json',
            ),
        ],
    )
    def test_release_json_url(self, url: str, expected_release_detail_json_url: str):
        """
        Test to ensure the JSON URl for the package release is set correctly.

        Args:
            url: The package URL to be tested.
            expected_release_detail_json_url: The expected JSON URL for the package release.
        """
        package = PackageVersion(
            name='contact',
            version='1.3.9',
            url=url,
            published=datetime.now(),
        )
        assert package.release_json_url == expected_release_detail_json_url
