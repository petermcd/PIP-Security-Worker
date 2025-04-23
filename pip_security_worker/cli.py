"""Code to capture imports and cli access."""

import logging

from pip_security_worker.package_analysis.analyse import Analyse

LOG = logging.getLogger(__name__)

def run_analyses() -> None:
    """Run the analysis application."""
    LOG.info('Running analyses')
    Analyse()

def run_update_db() -> None:
    """Entry point to the application."""
    LOG.info('Updating database')
    print('accessed')