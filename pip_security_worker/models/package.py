"""Dataclass for package information."""

from dataclasses import dataclass
from xmlrpc.client import DateTime


@dataclass
class Package(object):
    """Package dataclass."""

    link: str
    name: str
    version: str
    published: DateTime
