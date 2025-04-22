"""Code to analyse the requirements of a package."""

from pip_security_worker.helpers.helpers import fetch_next
from pip_security_worker.models.package import Package


class Analyse(object):
    """Class to analyse a package."""

    def __init__(self, package: Package | None = None) -> None:
        """
        Initialise the package analysis class.

        Args:
            package (Package, optional): The package to be analysed. Defaults to None.
        """
        package = package or fetch_next()
        print(package)
