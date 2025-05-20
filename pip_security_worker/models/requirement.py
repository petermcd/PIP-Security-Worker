"""Dataclass for package requirement."""

import logging
from dataclasses import dataclass

LOG = logging.getLogger(__name__)


@dataclass
class Requirement(object):
    """Requirement dataclass."""

    name: str
    version: str

    def __str__(self) -> str:
        """Return the string representation of the requirement."""
        LOG.debug(f'Requirement: __str__ - Calculating the string representation of the Requirement {self.name}')
        return f'{self.name} - {self.version}'
