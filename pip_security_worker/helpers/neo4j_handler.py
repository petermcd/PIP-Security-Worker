""" "Neo4j handler."""

from neo4j import GraphDatabase

from pip_security_worker import settings
from pip_security_worker.models.advisory import Advisory
from pip_security_worker.models.package import Package


class Neo4jHandler(object):
    __slots__ = ('_driver',)

    def __init__(self, uri, user, password) -> None:
        """Initialize the Neo4jHandler."""
        self._driver = GraphDatabase.driver(settings.NEO4J_URL, auth=(settings.NEO4J_USERNAME, settings.NEO4J_PASSWORD))

    def add_advisory(self, advisory: Advisory) -> None:
        """
        Add an advisory to the database.

        Args:
            advisory (Advisory): The advisory to be added.
        """
        self._driver.execute_query(
            f"MERGE (advisory:Advisory {{name: '{advisory.name}', advisory_id: '{advisory.advisory_id}'}})"
            f"ON CREATE SET advisory.description = '{advisory.description}', advisory.published = '{advisory.published}',"
            f"advisory.url = '{advisory.url}', advisory.raw = '{advisory.raw}',"
            f"advisory.security_type = '{advisory.security_type}', advisory.severity_score = '{advisory.severity_score}',"
            f"advisory.references = '{advisory.references}', advisory.versions = '{advisory.versions}'"
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
