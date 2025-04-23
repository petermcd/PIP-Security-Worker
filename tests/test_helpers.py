from unittest.mock import patch
from xmlrpc.client import DateTime

import pytest

from pip_security_worker.helpers.helpers import fetch_recent
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


class TestHelpers(object):

    @pytest.mark.parametrize(
        'status_code,xml_document,expected_packages',[
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
                    published=DateTime('Tue, 22 Apr 2025 15:09:38 GMT')
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
                    published=DateTime('Wed, 23 Apr 2025 06:58:26 GMT')
                ),
                Package(
                    name='flytekitplugins-pandera',
                    version='1.14.8',
                    link='https://pypi.org/project/flytekitplugins-pandera/1.14.8/',
                    published=DateTime('Wed, 23 Apr 2025 06:58:25 GMT')
                ),
                Package(
                    name='flytekitplugins-openai',
                    version='1.14.8',
                    link='https://pypi.org/project/flytekitplugins-openai/1.14.8/',
                    published=DateTime('Wed, 23 Apr 2025 06:58:24 GMT')
                ),
            ],
        ),
    ])
    def test_fetch_recent(self, status_code: int, xml_document: str,expected_packages: list[Package]):
        with patch('requests.get', return_value=MockedRequest(status_code=status_code, xml_document=xml_document)):
            packages = fetch_recent()
        assert packages == expected_packages
