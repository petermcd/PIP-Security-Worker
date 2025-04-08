"""Code to analyse the requirements of a package."""

from pip_security_worker.models.package import Package
from pip_security_worker.package_analysis.helpers import fetch_next


class Analyse:
    """Class to analyse a package."""

    def __init__(self, package: Package | None = None):
        """
        Initialise the package analysis class.

        Args:
            package (Package, optional): The package to be analysed. Defaults to None.
        """
        package = package or fetch_next()
        print(package)
