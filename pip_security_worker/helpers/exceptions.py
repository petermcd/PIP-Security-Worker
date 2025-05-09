"""Application-specific exceptions."""


class DatabaseConnectionError(Exception):
    """NEO4j database connection error."""

    pass


class GeneralError(Exception):
    """General error."""

    pass


class NoTasksError(Exception):
    """Kafka topic has no tasks."""

    pass
