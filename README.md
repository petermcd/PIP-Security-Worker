# PIP-Security-Worker
The application that populates the PIP Security Web application.

## Developer Notes

This project uses uv to manage the packages.

The following are the commands useful for this project:

```bash
# Check the package for linting and code formatting.
uvx ruff format
uvx ruff check
```

## Configuration

###

There are two environment variables used in this project:

PIP_ADVISORY_DB_URL - The URL for the advisory Git repository
PYPI_UPDATE_FEED - The URL for the package update feed or Pypi.org

### KAFKA

This package relies on access to a KAFKA queue. I have been developing using the `apache/kafka` docker image.

Once the image has been created, the following command is required to create the topic.:

```bash
./kafka-topics.sh --bootstrap-server localhost:9092 --create --topic analyse --partitions 10
```

For this to function, the following environment variables are required:

KAFKA_GROUP - To store the name of the Kafka group the application will use.
KAFKA_TIMEOUT - To store the request timeout for the consumer.
KAFKA_BOOTSTRAP_SERVERS - A list of bootstrap servers comma separated, each entry should be in the format localhost:9092.
KAFKA_TOPIC - The topic name to store tasks in.

### NEO4j

The resulting dependency tree is stored in a NEO4j database. This is using the standard neo4j docker image.

For this to function, the following environment variables are required:

NEO4J_URL - to store the NEO4j url in a format such as neo4j://localhost:7687.
NEO4J_USERNAME - to store the NEO4j username.
NEO4J_PASSWORD - to store the NEO4j password.

### Example Environment Variables

```bash
PIP_ADVISORY_DB_URL=https://github.com/pypa/advisory-database.git
PYPI_UPDATE_FEED=https://pypi.org/rss/updates.xml
KAFKA_GROUP=analyse
KAFKA_TIMEOUT=5000
KAFKA_BOOTSTRAP_SERVERS=localhost:9092
KAFKA_TOPIC=analyse
NEO4J_URL=neo4j://localhost:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=password
```

## Sentry

This package can also report errors to the Sentry service. To enable this, the following environment variable should be
populated:

SENTRY_DSN - The full DSN provided by Sentry.
