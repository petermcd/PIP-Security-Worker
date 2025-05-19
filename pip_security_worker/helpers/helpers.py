"""Helper function§s for package analysis."""

import logging
from datetime import datetime
from json import JSONDecodeError, loads
from xml.parsers.expat import ExpatError
from xmlrpc.client import DateTime

import requests
from defusedxml.minidom import parseString
from kafka import KafkaConsumer

from pip_security_worker import settings
from pip_security_worker.helpers.exceptions import NoTasksError
from pip_security_worker.models.package_version import PackageVersion

LOG = logging.getLogger(__name__)


def fetch_next() -> PackageVersion | None:
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
        consumer_timeout_ms=int(settings.KAFKA_TIMEOUT),
        auto_offset_reset='earliest',
    )

    try:
        LOG.debug('Fetching next package from Kafka')
        data_str = next(consumer).value.decode('utf-8')
        data_json = loads(data_str)
        LOG.debug(f'Fetched package {data_json["package_name"]} {data_json["package_version"]}')
        package: PackageVersion = PackageVersion(
            name=data_json['package_name'],
            version=data_json['package_version'],
            url=data_json['package_link'],
            published=datetime.fromisoformat(data_json['published']),
        )
    except StopIteration as exc:
        LOG.debug('No tasks waiting in Kafka.')
        raise NoTasksError('No tasks waiting.') from exc
    except JSONDecodeError:
        LOG.debug('Failed to decode JSON data')
        raise NoTasksError('Task not in expected format.') from None
    finally:
        consumer.close()

    return package


def fetch_recent() -> list[PackageVersion]:
    """
    Fetch a list of recently updated packages

    Returns:
        list[Package]: A list of recently updated packages.
    """
    LOG.debug('Starting fetch of recently updated packages')
    url = settings.PYPI_RECENT_PACKAGE_UPDATE_FEED
    response = requests.get(url)
    packages: list[PackageVersion] = []
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
            # TODO Fix this typing
            link = item.getElementsByTagName('link')[0].firstChild.nodeValue  # type: ignore[union-attr]
            xml_date: DateTime = item.getElementsByTagName('pubDate')[0].firstChild.nodeValue  # type: ignore[union-attr]
            published = datetime.strptime(str(xml_date), '%a, %d %b %Y %H:%M:%S %Z')
            link_split = link.split('/')
            if not link_split[-1]:
                del link_split[-1]
            title = link_split[-2]
            version = link_split[-1]
            packages.append(PackageVersion(name=title, version=version, url=link, published=published))
    LOG.info(f'Successfully fetched {len(packages)} packages')
    return packages
