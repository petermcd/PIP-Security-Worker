"""Helper function§s for package analysis."""

from xml.parsers.expat import ExpatError
from xmlrpc.client import DateTime

import requests
from defusedxml.minidom import parseString
from kafka import KafkaConsumer

from pip_security_worker import settings
from pip_security_worker.helpers.exceptions import NoTasksException
from pip_security_worker.models.package import Package


def fetch_next() -> Package | None:
    """
    Fetch the next package in the list from the fifo Queue.

    Raises:
        NoTasksException: On failure to get a task from the FIFO queue.

    Returns:
        Package: The next package to be analyzed is taken from the FIFO queue.
    """
    consumer = KafkaConsumer(
        settings.KAFKA_TOPIC,
        bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
        group_id=settings.KAFKA_GROUP,
        consumer_timeout_ms=settings.KAFKA_TIMEOUT,
    )

    try:
        # TODO create package from message the following message and return it
        _ = next(consumer)
    except StopIteration as exc:
        raise NoTasksException('No tasks waiting.') from exc
    finally:
        consumer.close()

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
        try:
            dom = parseString(xml_data.decode('utf-8'))
        except ExpatError:
            #TODO Log this error
            return packages
        items = dom.getElementsByTagName('item')
        for item in items:
            #TODO Fix this typing
            link = item.getElementsByTagName('link')[0].firstChild.nodeValue  # type: ignore[union-attr]
            published = DateTime(item.getElementsByTagName('pubDate')[0].firstChild.nodeValue)  # type: ignore[union-attr]
            link_split = link.split('/')
            title = link_split[-3]
            version = link_split[-2]
            packages.append(Package(name=title, version=version, link=link, published=published))
    return packages
