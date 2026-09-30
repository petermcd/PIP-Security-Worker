"""Application-specific exceptions."""


class DatabaseConnectionError(Exception):
    """NEO4j database connection error."""


class GeneralError(Exception):
    """General error."""


class NoTasksError(Exception):
    """Kafka topic has no tasks."""
