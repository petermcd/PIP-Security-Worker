"""Dataclass for package information."""

from dataclasses import dataclass
from datetime import datetime


@dataclass
class Package(object):
    """Package dataclass."""

    link: str
    name: str
    version: str
    published: datetime
