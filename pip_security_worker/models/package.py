"""Dataclass for package information."""

import logging
from dataclasses import dataclass, field
from functools import cached_property

LOG = logging.getLogger(__name__)


@dataclass
class Package(object):
    """Package dataclass."""

    name: str
    description: str = ''
    description_type: str = ''
    author: str = ''
    author_email: str = ''
    license: str = ''
    package_url: str = ''
    project_urls: dict[str, str] = field(default_factory=dict)
    raw: str = ''

    @cached_property
    def releases_url(self) -> str:
        """
        Return the releases url.

        Returns:
            URL of the release XML page.
        """
        LOG.debug(f'Calculating the releases XML URL for {self.name}')
        url_parts = self.package_url.strip().split('/')
        url_parts.insert(3, 'rss')
        url = '/'.join(url_parts)
        return f'{url}releases.xml' if url.endswith('/') else f'{url}/releases.xml'

    def __str__(self) -> str:
        """Return the string representation of the package."""
        return f'{self.name}'
