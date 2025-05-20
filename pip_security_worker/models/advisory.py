"""Dataclass for package advisory information."""

import logging
from dataclasses import dataclass
from datetime import datetime
from functools import cache

LOG = logging.getLogger(__name__)


@dataclass
class Advisory(object):
    """Advisory dataclass."""

    name: str
    description: str
    published: datetime
    advisory_id: str
    raw: str
    url: str | None = None
    versions: list[str] | None = None
    security_type: str | None = None
    severity_score: str | None = None
    references: dict[str, str] | None = None

    def __str__(self) -> str:
        """Return the string representation of the advisory."""
        LOG.debug(f'Advisory: __str__ - Calculating the string representation of the advisory {self.name}')
        versions = ', '.join(self.versions) if self.versions else 'ANY'
        return f"{self.published.isoformat()} {self.advisory_id} {self.name} versions '{versions}'"
