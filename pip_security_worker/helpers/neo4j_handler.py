""" "Neo4j handler."""

from json import dumps

from neo4j import GraphDatabase

from pip_security_worker import settings
from pip_security_worker.models.advisory import Advisory
from pip_security_worker.models.package import Package


class Neo4jHandler(object):
    __slots__ = ('_driver',)

    def __init__(self) -> None:
        """Initialize the Neo4jHandler."""
        self._driver = GraphDatabase.driver(settings.NEO4J_URL, auth=(settings.NEO4J_USERNAME, settings.NEO4J_PASSWORD))

    def add_advisory(self, advisory: Advisory) -> None:
        """
        Add an advisory to the database.

        Args:
            advisory (Advisory): The advisory to be added.
        """
        advisory_url: str = advisory.url or ""
        security_types: str = advisory.security_type or ""
        severity_score: str = advisory.severity_score or ""
        self._driver.execute_query(
            "MERGE (advisory:Advisory {{name: $advisory_name, advisory_id: $advisory_id}})" \
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
        self._driver.execute_query(
            "MERGE (advisory:Advisory {{name: $advisory_name, advisory_id: $advisory_id}})",
            advisory_id=advisory.advisory_id,
            advisory_name=advisory.name,
        )

    def link_to_package(self, advisory: Advisory) -> None:
        """
        Link an advisory to a package.

        Args:
            advisory (Advisory): The advisory to be linked.
        """
        # TODO implement

    def add_package(self, package: Package) -> None:
        """
        Add a package to the database.

        Args:
            package (Package): The package to be added.
        """
        # TODO implement

    def close(self) -> None:
        """Close the driver."""
        if self._driver is not None:
            self._driver.close()
