[![Quality Gate Status](http://57.128.159.138:9000/api/project_badges/measure?project=petermcd_PIP-Security-Worker_16d5bf2f-e512-4b2d-bb0c-454f82721f17&metric=alert_status&token=sqb_fe42ef646007b55c22ec2fb48b8637ac660f8422)](http://57.128.159.138:9000/dashboard?id=petermcd_PIP-Security-Worker_16d5bf2f-e512-4b2d-bb0c-454f82721f17)
[![Security Hotspots](http://57.128.159.138:9000/api/project_badges/measure?project=petermcd_PIP-Security-Worker_16d5bf2f-e512-4b2d-bb0c-454f82721f17&metric=security_hotspots&token=sqb_fe42ef646007b55c22ec2fb48b8637ac660f8422)](http://57.128.159.138:9000/dashboard?id=petermcd_PIP-Security-Worker_16d5bf2f-e512-4b2d-bb0c-454f82721f17)

# PIP-Security-Worker

This application populates a neo4j database with advisories from the pypi feed and associates them with packages in the
pypi index.

This database servers as a backend for a larger project that aims to provide a service that can be used to help identify
if your application is vulnerable.

## Developer Notes

This project uses uv to manage the packages. The tools being used at present are:

* isort
* mypy
* ruff

The following are the commands useful for this project:

```bash
# Check the package for linting and code formatting.
uvx ruff format
uvx ruff check
uvx isort .
uvx --with types-PyYAML --with types-requests --with types-defusedxml --with types-python-dateutil mypy pip_security_worker tests
```

## Configuration

The configuration for this application is stored in environment variables. These can also come from an `.env` file, the
location of which is shown in `settings.py`.

### PIP

There are two environment variables used in this project that relate to PIP:

#### PIP_ADVISORY_DB_URL

The URL for the advisory Git repository.

#### PYPI_UPDATE_FEED

The URL for the package update feed provided by Pypi.org.

### KAFKA

This package relies on access to a KAFKA queue. Development has been carried out using the `apache/kafka` docker image.

Once the image has been created, the following command is required to create the required topic on the docker container:

```bash
./kafka-topics.sh --bootstrap-server localhost:9092 --create --topic analyze --partitions 10
```

For this to function, the following environment variables are required:

#### KAFKA_GROUP

The name of the group that will be used to collect tasks. This is to ensure that we can run multiple analysis tasks at
the same time.

#### KAFKA_TIMEOUT

This is the timeout in ms that for the consumer when it retrieves a new task.

#### KAFKA_BOOTSTRAP_SERVERS

This is a list of Kafka bootstrap servers, this can be a singular server and should be in the format `localhost:9092`.
Multiple servers can be specified by providing a comma seperated list.

#### KAFKA_TOPIC

This is the name of the topic that is to be used for posting too and retrieving tasks from the Kafka server.

### NEO4j

The resulting dependency tree and links to advisories are stored in a NEO4j database. This is using the standard neo4j
docker image.

For this to function, the following environment variables are required:

#### NEO4J_URL

This is the URL for the neo4j database and should be in the format `neo4j://localhost:7687`.

#### NEO4J_USERNAME

This is the neo4j username.

#### NEO4J_PASSWORD

This is the neo4j password.

### Sentry

This package can also report errors to the Sentry service. To enable this, the following environment variable should be
populated:

#### SENTRY_DSN

This is the full DSN provided by Sentry when setting up a project and will be in the format:

`https://1234567890abcdef1234567890@o123456.ingest.us.sentry.io/1234567890123456`

### Example Environment Variables

The following is an example of how a complete `.env` file should look:

```bash
PIP_ADVISORY_DB_URL=https://github.com/pypa/advisory-database.git
PYPI_UPDATE_FEED=https://pypi.org/rss/updates.xml
KAFKA_GROUP=analyze
KAFKA_TIMEOUT=5000
KAFKA_BOOTSTRAP_SERVERS=localhost:9092
KAFKA_TOPIC=analyze
NEO4J_URL=neo4j://localhost:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=password
SENTRY_DSN=https://1234567890abcdef1234567890@o123456.ingest.us.sentry.io/1234567890123456
```
