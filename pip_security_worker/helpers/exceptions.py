"""Application-specific exceptions."""


class NoTasksException(Exception):
    """Kafka topic has no tasks."""
    pass


class DatabaseConnectionError(Exception):
    """NEO4j database connection error."""
    pass
