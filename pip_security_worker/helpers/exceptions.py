"""Application-specific exceptions."""


class DatabaseConnectionError(Exception):
    """NEO4j database connection error."""
    pass


class NoTasksException(Exception):
    """Kafka topic has no tasks."""
    pass
