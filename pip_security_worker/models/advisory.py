"""Dataclass for package advisory information."""

from dataclasses import dataclass
from datetime import datetime


@dataclass
class Advisory(object):
    """Advisory dataclass."""

    name: str
    description: str
    published: datetime
    advisory_id: str
    raw: str
    url: str | None
    versions: list[str] | None = None
    security_type: str | None = None
    severity_score: str | None = None
    references: dict[str, str] | None = None

    def __str__(self) -> str:
        """Return the string representation of the advisory."""
        return f'{self.name} {self.versions} {self.published} {self.advisory_id}'
