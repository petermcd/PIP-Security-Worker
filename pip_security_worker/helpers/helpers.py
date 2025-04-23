"""Helper function§s for package analysis."""
import logging
from xml.parsers.expat import ExpatError
from xmlrpc.client import DateTime

import requests
from defusedxml.minidom import parseString
from kafka import KafkaConsumer

from pip_security_worker import settings
from pip_security_worker.helpers.exceptions import NoTasksException
from pip_security_worker.models.package import Package

LOG = logging.getLogger(__name__)


def fetch_next() -> Package | None:
    """
    Fetch the next package in the list from the fifo Queue.

    Raises:
        NoTasksException: On failure to get a task from the FIFO queue.

    Returns:
        Package: The next package to be analyzed is taken from the FIFO queue.
    """
    LOG.debug('Starting fetch of next package from Kafka')
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
        LOG.debug('No tasks waiting in Kafka.')
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
    LOG.debug('Starting fetch of recently updated packages')
    url = settings.PYPI_RECENT_PACKAGE_UPDATE_FEED
    response = requests.get(url)
    packages: list[Package] = []
    if response.status_code == requests.codes.ok:
        LOG.debug('Successfully fetched recently updated packages')
        xml_data = response.content
        try:
            dom = parseString(xml_data.decode('utf-8'))
        except ExpatError:
            LOG.critical('Failed to parse XML data')
            return packages
        items = dom.getElementsByTagName('item')
        for item in items:
            #TODO Fix this typing
            link = item.getElementsByTagName('link')[0].firstChild.nodeValue  # type: ignore[union-attr]
            published = DateTime(item.getElementsByTagName('pubDate')[0].firstChild.nodeValue)  # type: ignore[union-attr]
            link_split = link.split('/')
            if not link_split[-1]:
                del link_split[-1]
            title = link_split[-2]
            version = link_split[-1]
            packages.append(Package(name=title, version=version, link=link, published=published))
    LOG.info(f'Successfully fetched {len(packages)} packages')
    return packages
