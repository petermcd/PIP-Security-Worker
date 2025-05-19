"""Dataclass for package requirement."""

from dataclasses import dataclass


@dataclass
class Requirement(object):
    """Requirement dataclass."""

    name: str
    version: str
