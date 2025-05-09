from datetime import datetime, timezone
from unittest.mock import patch

import pytest

from pip_security_worker.helpers.helpers import fetch_recent, fetch_next
from pip_security_worker.models.package import Package


class MockedRequest(object):
    status_code = 400
    content: bytes = ''.encode('utf-8')

    def __init__(self, *args, **kwargs):
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
    value = ''
    def __init__(self, *args, **kwargs):
        if 'value' in kwargs:
            self.value = kwargs['value']


class TestHelpers(object):
    @pytest.mark.parametrize(
        'status_code,xml_document,expected_packages',
        [
            (
                400,
                '',
                [],
            ),
            (
                200,
                './tests/test_data/malformed.xml',
                [],
            ),
            (
                200,
                './tests/test_data/empty.xml',
                [],
            ),
            (
                200,
                './tests/test_data/single.xml',
                [
                    Package(
                        name='bbbctl',
                        version='0.3.2',
                        link='https://pypi.org/project/bbbctl/0.3.2/',
                        published=datetime.strptime('Tue, 22 Apr 2025 15:09:38 GMT', '%a, %d %b %Y %H:%M:%S GMT'),
                    ),
                ],
            ),
            (
                200,
                './tests/test_data/single_alt_url.xml',
                [
                    Package(
                        name='bbbctl',
                        version='0.3.2',
                        link='https://pypi.org/project/bbbctl/0.3.2',
                        published=datetime.strptime('Tue, 22 Apr 2025 15:09:38 GMT', '%a, %d %b %Y %H:%M:%S GMT'),
                    ),
                ],
            ),
            (
                200,
                './tests/test_data/multiple.xml',
                [
                    Package(
                        name='flytekitplugins-papermill',
                        version='1.14.8',
                        link='https://pypi.org/project/flytekitplugins-papermill/1.14.8/',
                        published=datetime.strptime('Wed, 23 Apr 2025 06:58:26 GMT', '%a, %d %b %Y %H:%M:%S GMT'),
                    ),
                    Package(
                        name='flytekitplugins-pandera',
                        version='1.14.8',
                        link='https://pypi.org/project/flytekitplugins-pandera/1.14.8/',
                        published=datetime.strptime('Wed, 23 Apr 2025 06:58:25 GMT', '%a, %d %b %Y %H:%M:%S GMT'),
                    ),
                    Package(
                        name='flytekitplugins-openai',
                        version='1.14.8',
                        link='https://pypi.org/project/flytekitplugins-openai/1.14.8/',
                        published=datetime.strptime('Wed, 23 Apr 2025 06:58:24 GMT', '%a, %d %b %Y %H:%M:%S GMT'),
                    ),
                ],
            ),
        ],
    )
    def test_fetch_recent(self, status_code: int, xml_document: str, expected_packages: list[Package]):
        with patch('requests.get', return_value=MockedRequest(status_code=status_code, xml_document=xml_document)):
            returned_packages = fetch_recent()
        assert returned_packages == expected_packages

    @pytest.mark.parametrize(
        'record,expected_package',
        [
            (
                MockedKafkaItem(value=b'{"package_link": "https://pypi.org/project/Monzo-API/", "package_name": "monzo-api", "package_version": "1.2.0", "published": "2025-04-18T10:30:00.000Z"}'),
                Package(
                    name='monzo-api',
                    version='1.2.0',
                    link="https://pypi.org/project/Monzo-API/",
                    published=datetime(2025, 4, 18, 10, 30, tzinfo=timezone.utc),
                )
            ),
        ],
    )
    def test_fetch_next(self, record: str ,expected_package: Package):
        with patch('kafka.KafkaConsumer.__init__', return_value=None):
            with patch('kafka.KafkaConsumer.close', return_value=None):
                with patch('kafka.KafkaConsumer.__next__', return_value=record):
                    returned_package = fetch_next()

        assert returned_package == expected_package
