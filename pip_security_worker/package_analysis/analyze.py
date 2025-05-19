"""Code to analyze the requirements of a package."""

import json
import logging
from re import split

import requests

from pip_security_worker.helpers.helpers import fetch_next
from pip_security_worker.models.package import Package
from pip_security_worker.models.package_version import PackageVersion
from pip_security_worker.models.requirement import Requirement

LOG = logging.getLogger(__name__)


class Analyze(object):
    """Class to analyze a package."""

    __slots__ = ('_package',)

    def __init__(self, package: PackageVersion | None = None) -> None:
        """
        Initialize the package analyzes class.

        Args:
            package (PackageVersion, optional): The package to be analyzed. Defaults to None.
        """
        LOG.debug('Initializing Analyze')
        self._package = package or fetch_next()
        self._fetch_release_info()

    def _fetch_release_info(self):
        """Fetch the release information for the package version."""
        response = requests.get(self._package.release_json_url)
        details = json.loads(response.text)
        if 'info' in details:
            self._package.requirements = self._parse_requirements(
                extras_list=details['info'].get('provides_extra', []),
                requirements_list=details['info'].get('requires_dist', []),
            )
            self._package.python_version = details['info'].get('requires_python', '')

            self._package.for_package = Package(
                name=details['info'].get('name', ''),
                description=details['info'].get('description', ''),
                description_type=details['info'].get('description_content_type', ''),
                author=details['info'].get('author', ''),
                author_email=details['info'].get('author_email', ''),
                license=details['info'].get('license', ''),
                package_url=details['info'].get('package_url', ''),
                project_urls=details['info'].get('project_urls', ''),
                raw=response.text,
            )

    @staticmethod
    def _parse_requirements(extras_list: list[str], requirements_list: list[str]) -> dict[str, list[Requirement]]:
        """
        Parse the requirements for the package version.

        Args:
            extras_list: List of extras the package provides.
            requirements_list: List of requirements for the package.
        """
        LOG.debug('Parsing requirements for package')
        requirements: dict[str, list[Requirement]] = {'standard': []}
        for extra in extras_list:
            requirements[extra] = []

        for requirement in requirements_list:
            extra_name = 'standard'
            extra_detail = requirement
            if 'extra' in requirement:
                LOG.debug(f'Extra requirement found: {requirement}')
                req_split = requirement.split(';')
                extra_detail = req_split[0]
                extra_details = req_split[1].split('==')
                extra_name = extra_details[1].strip().replace('"', '')

            version_split = split(r'[<>=!]', requirement)
            version_details = extra_detail.replace(version_split[0], '')
            req = Requirement(
                name=version_split[0],
                version=version_details or 'any',
            )
            requirements[extra_name].append(req)

        return requirements


Analyze()
