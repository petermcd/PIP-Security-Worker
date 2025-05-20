"""Code to test the Requirement model."""

import pytest

from pip_security_worker.models.requirement import Requirement


class TestRequirement(object):
    """Test suite to test the Requirement model."""

    @pytest.mark.parametrize(
        'name,version,expected_string',
        [
            ('monzo-api', '1.0.0', 'monzo-api - 1.0.0'),
            (
                'monzo-api',
                '1.0.1',
                'monzo-api - 1.0.1',
            ),
            (
                'requests',
                '1.0.0',
                'requests - 1.0.0',
            ),
        ],
    )
    def test_str(self, name: str, version: str, expected_string: str) -> None:
        """
        Test to ensure the string representation is correct.

        Args:
            name: The name of the requirement.
            version: The versions of the requirement.
            expected_string: The expected string representation.
        """
        requirement = Requirement(
            name=name,
            version=version,
        )
        assert str(requirement) == expected_string
