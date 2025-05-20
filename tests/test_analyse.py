"""Code to test the analyze.py module."""

from datetime import datetime

import pytest

from pip_security_worker.models.package_version import PackageVersion
from pip_security_worker.models.requirement import Requirement
from pip_security_worker.package_analysis.analyze import Analyze


class TestAnalyze(object):
    """
    Set of tests to ensure the 'analyze' class is working as expected.
    """

    @pytest.mark.parametrize(
        'extras,requirements,expected_requirements',
        [
            (
                # Test to ensure that an empty list of extras is parsed correctly.
                [],
                [],
                {
                    'standard': [],
                },
            ),
            (
                # Test to a requirement without a version is parsed correctly.
                [],
                ['requests'],
                {
                    'standard': [Requirement(name='requests', version='any')],
                },
            ),
            (
                # Test to ensure that an extra with no required packages is parsed correctly.
                ['security'],
                ['requests'],
                {
                    'security': [],
                    'standard': [Requirement(name='requests', version='any')],
                },
            ),
            (
                # Test to ensure that multiple extras are parsed correctly with versions.
                ['security', 'socks'],
                [
                    'requests',
                    'PySocks!=1.5.7,>=1.5.6; extra == "socks"',
                ],
                {
                    'security': [],
                    'socks': [
                        Requirement(name='PySocks', version='!=1.5.7,>=1.5.6'),
                    ],
                    'standard': [Requirement(name='requests', version='any')],
                },
            ),
        ],
    )
    def test_parse_requirements(
        self,
        extras: list[str],
        requirements: list[str],
        expected_requirements,
        mocker,
    ):
        """
        Test to ensure that package requirements are parsed correctly.

        Args:
            extras: A list of extras to be parsed.
            requirements: A list of requirements to be parsed.
            expected_requirements: The expected requirements.
            mocker: Pytest mocker object.
        """
        package = PackageVersion(
            name='nothing',
            version='2.32.3',
            url='https://pypi.org/project/nothing/1.0.0/',
            published=datetime.now(),
        )
        mocker.patch('pip_security_worker.package_analysis.analyze.Analyze._fetch_release_info')
        analyze = Analyze(package=package)

        assert analyze._parse_requirements(extras, requirements) == expected_requirements
