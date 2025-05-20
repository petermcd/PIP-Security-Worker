"""Code to test the Advisory model."""

from datetime import datetime

import pytest
from freezegun import freeze_time

from pip_security_worker.models.advisory import Advisory


class TestAdvisory(object):
    """Test suite to test the Advisory model."""

    @freeze_time('2025-01-01')
    @pytest.mark.parametrize(
        'name,advisory_id,versions,expected_string',
        [
            (
                # Test to ensure the string is correct when a single version is provided.
                'Requests',
                'abc123',
                ['1.0.0'],
                "2025-01-01T00:00:00 abc123 Requests versions '1.0.0'",
            ),
            (
                # Test to ensure the string is correct when multiple versions are provided.
                'Monzo-API',
                'def456',
                ['1.0.0', '2.0.0'],
                "2025-01-01T00:00:00 def456 Monzo-API versions '1.0.0, 2.0.0'",
            ),
            (
                # Test to ensure the string is correct when no versions are provided.
                'Monzo-API',
                'def456',
                None,
                "2025-01-01T00:00:00 def456 Monzo-API versions 'ANY'",
            ),
        ],
    )
    def test_str(self, name: str, advisory_id: str, versions: list[str], expected_string: str) -> None:
        """
        Test to ensure the string representation is correct.

        Args:
            name: The name of the advisory.
            advisory_id: The ID of the advisory.
            versions: The versions of the advisory.
            expected_string: The expected string representation.
        """
        advisory = Advisory(
            name=name,
            description='No description to see.',
            published=datetime.now(),
            advisory_id=advisory_id,
            raw='No raw data to see.',
            versions=versions,
        )
        assert str(advisory) == expected_string
