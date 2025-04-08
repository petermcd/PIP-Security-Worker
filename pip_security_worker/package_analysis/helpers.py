"""Helper function§s for package analysis."""

from xml.dom.minidom import parseString
from xmlrpc.client import DateTime

import requests

from pip_security_worker import settings
from pip_security_worker.models.package import Package


def fetch_next() -> Package:
    """
    Fetch the next package in the list from the fifo Queue.

    Returns:
        Package: The next package to be analyzed taken from the FIFO queue.
    """
    # TODO: Implement the logic to fetch the next package from the FIFO queue.
    return Package(
        name='example',
        version='2.0.0',
        link='https://example.com',
        published=DateTime('2023-10-01T12:00:00Z'),
    )


def fetch_recent() -> list[Package]:
    """
    Fetch a list of recently updated packages

    Returns:
        list[Package]: A list of recently updated packages.
    """
    url = settings.PYPI_RECENT_PACKAGE_UPDATE_FEED
    response = requests.get(url)
    packages: list[Package] = []
    if response.status_code == requests.codes.ok:
        xml_data = response.content
        dom = parseString(xml_data)
        items = dom.getElementsByTagName('item')
        for item in items:
            link = item.getElementsByTagName('link')[0].firstChild.nodeValue
            link_split = link.split('/')
            title = link_split[-2]
            version = link_split[-1]
            published = DateTime(item.getElementsByTagName('pubDate')[0].firstChild.nodeValue)
            packages.append(Package(name=title, version=version, link=link, published=published))
    return packages


fetch_recent()
