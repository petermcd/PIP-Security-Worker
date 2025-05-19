""" "Fetch tasks."""

import logging
from json import dumps

from kafka import KafkaProducer

from pip_security_worker import settings
from pip_security_worker.helpers.helpers import fetch_recent
from pip_security_worker.models.package_version import PackageVersion

LOG = logging.getLogger(__name__)


class FetchTasks(object):
    """Class to handle fetching new packages to analyze from the pypi update feed."""

    @staticmethod
    def update() -> None:
        """Fetch new packages to analyze from the pypi update feed."""
        LOG.debug('Fetching new packages to analyze from the pypi update feed')
        new_package_versions: list[PackageVersion] = fetch_recent()
        # TODO identify if the packages have already been added
        kafka_producer = KafkaProducer(bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS)
        for package in new_package_versions:
            LOG.debug(f'Sending package {package.name} {package.version} to Kafka')
            payload = {
                'package_name': package.name,
                'package_version': package.version,
                'package_link': package.url,
                'published': package.published.isoformat(),
            }
            kafka_producer.send(settings.KAFKA_TOPIC, value=dumps(payload).encode('utf-8'))
            kafka_producer.flush()
        kafka_producer.close()
