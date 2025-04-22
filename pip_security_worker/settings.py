"""Settings for pip_security_worker."""
import os

import sentry_sdk
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path)

# The location of the recently updated packages feed.
PYPI_RECENT_PACKAGE_UPDATE_FEED = os.getenv('PYPI_UPDATE_FEED', 'https://pypi.org/rss/updates.xml')

PIP_ADVISORY_DB_URL = os.getenv('PIP_ADVISORY_DB_URL', 'https://github.com/pypa/advisory-database.git')

# Kafka configuration
KAFKA_TOPIC = os.getenv('KAFKA_TOPIC', 'tasks')
KAFKA_BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')
KAFKA_GROUP = os.getenv('KAFKA_GROUP', 'processor')
KAFKA_TIMEOUT = os.getenv('KAFKA_TIMEOUT', 5000)

# NEO4j Configuration
NEO4J_URL = os.getenv('KAFKA_TOPIC', 'localhost:9092')
NEO4J_USERNAME = os.getenv('NEO4J_USERNAME', 'neo4j')
NEO4J_PASSWORD = os.getenv('NEO4J_PASSWORD', 'neo4j')

# GIT Configuration
GIT_STORAGE = os.getenv('GIT_STORAGE', '/tmp/advisory_database/')

#Sentry Configuration

if SENTRY_DSN:= os.getenv('SENTRY_DSN'):
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        send_default_pii=True,
    )
