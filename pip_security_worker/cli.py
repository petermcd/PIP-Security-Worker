"""Code to capture imports and cli access."""

import logging
import sys

from pip_security_worker.helpers.exceptions import DatabaseConnectionError
from pip_security_worker.helpers.neo4j_handler import Neo4jHandler
from pip_security_worker.package_analysis.analyse import Analyse
from pip_security_worker.vulnerability_database.pip_advisory import PIPAdvisory

LOG = logging.getLogger(__name__)

def run_analyses() -> None:
    """Run the analysis application."""
    LOG.info('Running analyses')
    Analyse()

def run_update_db() -> None:
    """Entry point to the application."""
    LOG.info('Updating advisory database')

    try:
        neo4j_handler = Neo4jHandler()
    except DatabaseConnectionError as exc:
        print(f'Failed to connect to Neo4j database: {exc}')
        sys.exit(1)

    with PIPAdvisory() as pip_advisory:
        for advisory in pip_advisory.test():
            LOG.info(f'Adding advisory {advisory.advisory_id} for package {advisory.name} to the database')
            neo4j_handler.add_advisory(advisory=advisory)

