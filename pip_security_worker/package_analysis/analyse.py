"""Code to analyze the requirements of a package."""
import logging

from pip_security_worker.helpers.helpers import fetch_next
from pip_security_worker.models.package import Package

LOG = logging.getLogger(__name__)

class Analyse(object):
    """Class to analyze a package."""

    def __init__(self, package: Package | None = None) -> None:
        """
        Initialize the package analyzes class.

        Args:
            package (Package, optional): The package to be analyzed. Defaults to None.
        """
        LOG.debug('Initializing Analyse')
        package = package or fetch_next()
