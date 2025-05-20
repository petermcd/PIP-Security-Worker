"""Code to test the helpers.py module."""

from datetime import datetime, timezone
from unittest.mock import patch

import pytest

from pip_security_worker.helpers.helper_functions import (fetch_next,
                                                          fetch_recent)
from pip_security_worker.models.package_version import PackageVersion


class MockedRequest(object):
    """
    Helper class to for mocking request response.
    """

    status_code = 400
    content: bytes = ''.encode('utf-8')

    def __init__(self, *args, **kwargs):
        """
        Helper class to mock a request response.

        Args:
            args: No positional arguments are used.
            kwargs: status_code and xml_document are used if set.
        """
        _ = args
        if 'status_code' in kwargs:
            self.status_code = kwargs['status_code']
        if 'xml_document' in kwargs and kwargs['xml_document']:
            self._fetch_document(kwargs['xml_document'])

    def _fetch_document(self, document: str):
        """
        Fetch the document content.

        Args:
            document (str): The document to be fetched.
        """
        with open(document, 'r') as fh:
            self.content = fh.read().encode('utf-8')


class MockedKafkaItem(object):
    """
    Helper class to mock a Kafka record.
    """

    value = ''

    def __init__(self, *args, **kwargs):
        """
        Initialise MockedKafkaItem.

        Args:
            args: No positional arguments are used.
            kwargs: value is used if set.
        """
        _ = args
        if 'value' in kwargs:
            self.value = kwargs['value']


class TestHelpers(object):
    """
    Test class to ensure the helpers are working as expected.
    """

    @pytest.mark.parametrize(
        'status_code,xml_document,expected_packages',
        [
            (
                # Test to ensure fetch_recent returns an empty list when the status code is not 200.
                400,
                '',
                [],
            ),
            (
                # Test to ensure fetch_recent returns an empty list when the XML document is malformed.
                200,
                './tests/test_data/malformed.xml',
                [],
            ),
            (
                # Test to ensure fetch_recent returns an empty list when the XML document is empty.
                200,
                './tests/test_data/empty.xml',
                [],
            ),
            (
                # Test to ensure fetch_recent returns the expected packages when the XML document is valid.
                200,
                './tests/test_data/single.xml',
                [
                    PackageVersion(
                        name='bbbctl',
                        version='0.3.2',
                        url='https://pypi.org/project/bbbctl/0.3.2/',
                        published=datetime.strptime('Tue, 22 Apr 2025 15:09:38 GMT', '%a, %d %b %Y %H:%M:%S GMT'),
                    ),
                ],
            ),
            (
                # Test to ensure fetch_recent returns the expected packages when the XML document has an alternate URL.
                200,
                './tests/test_data/single_alt_url.xml',
                [
                    PackageVersion(
                        name='bbbctl',
                        version='0.3.2',
                        url='https://pypi.org/project/bbbctl/0.3.2',
                        published=datetime.strptime('Tue, 22 Apr 2025 15:09:38 GMT', '%a, %d %b %Y %H:%M:%S GMT'),
                    ),
                ],
            ),
            (
                # Test to ensure fetch_recent returns the expected packages when the XML document has multiple packages.
                200,
                './tests/test_data/multiple.xml',
                [
                    PackageVersion(
                        name='flytekitplugins-papermill',
                        version='1.14.8',
                        url='https://pypi.org/project/flytekitplugins-papermill/1.14.8/',
                        published=datetime.strptime('Wed, 23 Apr 2025 06:58:26 GMT', '%a, %d %b %Y %H:%M:%S GMT'),
                    ),
                    PackageVersion(
                        name='flytekitplugins-pandera',
                        version='1.14.8',
                        url='https://pypi.org/project/flytekitplugins-pandera/1.14.8/',
                        published=datetime.strptime('Wed, 23 Apr 2025 06:58:25 GMT', '%a, %d %b %Y %H:%M:%S GMT'),
                    ),
                    PackageVersion(
                        name='flytekitplugins-openai',
                        version='1.14.8',
                        url='https://pypi.org/project/flytekitplugins-openai/1.14.8/',
                        published=datetime.strptime('Wed, 23 Apr 2025 06:58:24 GMT', '%a, %d %b %Y %H:%M:%S GMT'),
                    ),
                ],
            ),
        ],
    )
    def test_fetch_recent(self, status_code: int, xml_document: str, expected_packages: list[PackageVersion]):
        """
        Test to ensure fetch_recent returns the expected packages.

        Args:
            status_code: Mocked response status code.
            xml_document: XML document to be used for mocked response.
            expected_packages: Expected packages to be returned.
        """
        with patch('requests.get', return_value=MockedRequest(status_code=status_code, xml_document=xml_document)):
            returned_packages = fetch_recent()
        assert returned_packages == expected_packages

    @pytest.mark.parametrize(
        'record,expected_package',
        [
            (
                # Test to ensure a record is parsed and returned correctly.
                MockedKafkaItem(
                    value=b'{"package_link": "https://pypi.org/project/Monzo-API/", "package_name": "monzo-api", "package_version": "1.2.0", "published": "2025-04-18T10:30:00.000Z"}'
                ),
                PackageVersion(
                    name='monzo-api',
                    version='1.2.0',
                    url='https://pypi.org/project/Monzo-API/',
                    published=datetime(2025, 4, 18, 10, 30, tzinfo=timezone.utc),
                ),
            ),
        ],
    )
    def test_fetch_next(self, record: str, expected_package: PackageVersion):
        """
        Test to ensure fetch_next provides a record as expected from a Kafka response.

        Args:
            record: The Kafka record to be returned.
            expected_package: The expected package to be returned.
        """
        with patch('kafka.KafkaConsumer.__init__', return_value=None):
            with patch('kafka.KafkaConsumer.close', return_value=None):
                with patch('kafka.KafkaConsumer.__next__', return_value=record):
                    returned_package = fetch_next()

        assert returned_package == expected_package
