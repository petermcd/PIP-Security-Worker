""" "Neo4j handler."""

import logging
from json import dumps

import neo4j
from neo4j import GraphDatabase

from pip_security_worker import settings
from pip_security_worker.helpers.exceptions import DatabaseConnectionError
from pip_security_worker.models.advisory import Advisory
from pip_security_worker.models.package_version import PackageVersion

LOG = logging.getLogger(__name__)


class Neo4jHandler(object):
    """Class to handle Neo4j database operations."""

    __slots__ = ('_driver',)

    def __init__(self) -> None:
        """Initialize the Neo4jHandler."""
        LOG.debug('Neo4jHandler:__init__ - Initializing Neo4jHandler')
        try:
            LOG.debug('Neo4jHandler:__init__ - Connecting to Neo4j database')
            self._driver = GraphDatabase.driver(
                settings.NEO4J_URL,
                auth=(settings.NEO4J_USERNAME, settings.NEO4J_PASSWORD),
            )
        except (neo4j.exceptions.ConfigurationError, neo4j.exceptions.ServiceUnavailable) as exc:
            LOG.critical('Neo4jHandler:__init__ - Failed to connect to Neo4j database')
            raise DatabaseConnectionError('Failed to connect to Neo4j database') from exc

    def add_advisory(self, advisory: Advisory) -> None:
        """
        Add an advisory to the database.

        Args:
            advisory (Advisory): The advisory to be added.
        """
        LOG.debug(f'Neo4jHandler:add_advisory - Adding advisory {advisory.name} to database')
        advisory_url: str = advisory.url or ''
        security_types: str = advisory.security_type or ''
        severity_score: str = advisory.severity_score or ''
        self._driver.execute_query(
            'MERGE (advisory:Advisory {name: $advisory_name, advisory_id: $advisory_id})'
            + 'ON CREATE SET advisory.description = $advisory_description, advisory.published = $advisory_published,'
            + 'advisory.url = $advisory_url, advisory.raw = $advisory_raw,'
            + 'advisory.security_type = $advisory_security_type, advisory.severity_score = $advisory_severity_score,'
            + 'advisory.references = $advisory_references, advisory.versions = $advisory_versions',
            advisory_id=advisory.advisory_id,
            advisory_name=advisory.name,
            advisory_description=advisory.description,
            advisory_published=advisory.published.isoformat(),
            advisory_url=advisory_url,
            advisory_raw=advisory.raw,
            advisory_security_type=security_types,
            advisory_severity_score=severity_score,
            advisory_references=dumps(advisory.references),
            advisory_versions=dumps(advisory.versions),
        )
        self.link_to_package(advisory=advisory)

    def link_to_package(self, advisory: Advisory) -> None:
        """
        Link an advisory to a package.

        Args:
            advisory (Advisory): The advisory to be linked.
        """
        # Link to the overall package, if it doesn't exist yet, create it.
        self._driver.execute_query(
            'MATCH(advisory:Advisory {name: $advisory_name, advisory_id: $advisory_id})'
            + 'MERGE (package:Package {name: $advisory_name})'
            + 'ON CREATE SET package.history_analyzed= $package_history_analyzed '
            + 'MERGE(advisory)-[:advisory_affects_package]->(package)'
            + 'MERGE(package)-[:package_affected_by]->(advisory)',
            advisory_name=advisory.name,
            advisory_id=advisory.advisory_id,
            package_history_analyzed=0,
        )
        if not advisory.versions:
            LOG.debug(f'Neo4jHandler:link_to_package - No affected versions found for advisory {advisory.name}')
            # TODO identify what to do here.
            return
        for version in advisory.versions:
            # Link to the package version if it exists.
            self._driver.execute_query(
                'MATCH(advisory: Advisory {name: $advisory_name, advisory_id: $advisory_id})'
                + 'MATCH(packageVersion: PackageVersion {name: $advisory_name, version: $affects}) '
                + 'MERGE(advisory)-[:affects_package_version]->(packageVersion)'
                + 'MERGE(packageVersion)-[:affected_by_advisory]->(advisory)',
                advisory_name=advisory.name,
                affects=version,
                advisory_id=advisory.advisory_id,
            )

    def add_package(self, package: PackageVersion) -> None:
        """
        Add a package to the database.

        Args:
            package (PackageVersion): The package to be added.
        """
        # TODO fully implement
        LOG.debug(f'Neo4jHandler:add_package - Adding package {package.name} to database')
        self._driver.execute_query(
            'MERGE (advisory:Package {name: $package_name, version: $package_version})',
            package_name=package.name,
            package_version=package.version,
        )

    def close(self) -> None:
        """Close the driver."""
        LOG.debug('Neo4jHandler:close - Closing Neo4jHandler')
        if self._driver is not None:
            LOG.debug('Neo4jHandler:close - Connection exists, closing')
            self._driver.close()
