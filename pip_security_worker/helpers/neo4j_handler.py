""" "Neo4j handler."""
import logging
from json import dumps

import neo4j
from neo4j import GraphDatabase

from pip_security_worker import settings
from pip_security_worker.helpers.exceptions import DatabaseConnectionError
from pip_security_worker.models.advisory import Advisory
from pip_security_worker.models.package import Package

LOG = logging.getLogger(__name__)

class Neo4jHandler(object):
    __slots__ = ('_driver',)

    def __init__(self) -> None:
        """Initialize the Neo4jHandler."""
        LOG.debug('Initializing Neo4jHandler')
        print(settings.NEO4J_URL)
        try:
            self._driver = GraphDatabase.driver(
                settings.NEO4J_URL,
                auth=(settings.NEO4J_USERNAME, settings.NEO4J_PASSWORD),
            )
        except neo4j.exceptions.ConfigurationError as exc:
            LOG.critical('Failed to connect to Neo4j database')
            raise DatabaseConnectionError('Failed to connect to Neo4j database') from exc


    def add_advisory(self, advisory: Advisory) -> None:
        """
        Add an advisory to the database.

        Args:
            advisory (Advisory): The advisory to be added.
        """
        LOG.debug(f'Adding advisory {advisory.name} to database')
        advisory_url: str = advisory.url or ""
        security_types: str = advisory.security_type or ""
        severity_score: str = advisory.severity_score or ""
        self._driver.execute_query(
            "MERGE (advisory:Advisory {name: $advisory_name, advisory_id: $advisory_id})" \
            + "ON CREATE SET advisory.description = $advisory_description, advisory.published = $advisory_published," \
            + "advisory.url = $advisory_url, advisory.raw = $advisory_raw," \
            + "advisory.security_type = $advisory_security_type, advisory.severity_score = $advisory_severity_score," \
            + "advisory.references = $advisory_references, advisory.versions = $advisory_versions",
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
        if not advisory.versions:
            # No versions to link to, so we don't need to do anything.
            #TODO identify what to do here.
            return
        for version in advisory.versions:
            self._driver.execute_query(
                "MATCH(a: Advisory {name: $advisory_name, advisory_id: $advisory_id})" \
                + "MATCH(p: Package {name: $advisory_name, version: $affects}) " \
                + "MERGE(a)-[:affects]->(p)" \
                + "MERGE(p)-[:affected_by]->(a)",
                advisory_name=advisory.name,
                affects=version,
                advisory_id=advisory.advisory_id,
            )

    def add_package(self, package: Package) -> None:
        """
        Add a package to the database.

        Args:
            package (Package): The package to be added.
        """
        # TODO implement
        LOG.debug(f'Adding package {package.name} to database')
        self._driver.execute_query(
            "MERGE (advisory:Package {name: $package_name, version: $package_version})",
            package_name=package.name,
            package_version=package.version,
        )

    def close(self) -> None:
        """Close the driver."""
        LOG.debug('Closing Neo4jHandler')
        if self._driver is not None:
            LOG.debug('Connection exists, closing')
            self._driver.close()
