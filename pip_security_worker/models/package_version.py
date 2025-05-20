"""Dataclass for package information."""

import logging
from dataclasses import dataclass, field
from datetime import datetime
from functools import cached_property

from pip_security_worker.models.package import Package
from pip_security_worker.models.requirement import Requirement

LOG = logging.getLogger(__name__)


@dataclass
class PackageVersion(object):
    """Package dataclass."""

    name: str
    version: str
    url: str
    published: datetime
    python_version: str = ''
    requirements: dict[str, list[Requirement]] = field(default_factory=dict)
    for_package: Package | None = None

    @cached_property
    def release_json_url(self) -> str:
        """
        Return the release JSON information URL.

        Returns:
            URL of the release JSON information.
        """
        LOG.debug(
            f'PackageVersion:release_json_url - Calculating the release JSON URL for {self.name} version {self.version}'
        )
        return f'https://pypi.python.org/pypi/{self.name}/{self.version}/json'

    @cached_property
    def releases_url(self) -> str:
        """
        Return the releases url.

        Returns:
            URL of the release XML page.
        """
        LOG.debug(f'PackageVersion:releases_url - Calculating the releases XML URL for {self.name}')
        url_parts = self.url.strip().split('/')
        url_parts.insert(3, 'rss')
        if url_parts[-1] == '':
            url_parts[-2] = 'releases.xml'
            del url_parts[-1]
        else:
            url_parts[-1] = 'releases.xml'
        return '/'.join(url_parts)

    def __str__(self) -> str:
        """Return the string representation of the package."""
        LOG.debug(f'PackageVersion: __str__ - Calculating the string representation of the PackageVersion {self.name}')
        return f'{self.name} - {self.version}'
