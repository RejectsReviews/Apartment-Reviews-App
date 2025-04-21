# gunicorn_config.py
import multiprocessing
import os
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)

# The socket to bind.
# "0.0.0.0" to bind to all interfaces. 8000 is the port number.
bind = "0.0.0.0:8080"

# The number of worker processes for handling requests.
workers = 4

# Use the 'gevent' worker type for async performance.
worker_class = 'gevent'

# Log level
loglevel = 'info'

# Where to log to
accesslog = '-'  # '-' means log to stdout
errorlog = '-'  # '-' means log to stderr

# Disable SSL certificate verification if in Render environment
os.environ['PGSSLMODE'] = 'disable'

# Set sqlite as fallback if postgres connection fails
os.environ['USE_SQLITE_FALLBACK'] = 'true'

# Construct PostgreSQL connection string from environment variables
pg_host = os.environ.get('POSTGRES_URL')
pg_user = os.environ.get('POSTGRES_USER')
pg_password = os.environ.get('POSTGRES_PASSWORD')
pg_db = os.environ.get('POSTGRES_DB')

if pg_host and pg_user and pg_password and pg_db:
    # Try with different SSL parameters to fix SSL connection issues
    DATABASE_URL = f"postgresql://{pg_user}:{pg_password}@{pg_host}/{pg_db}?sslmode=disable"
    os.environ['DATABASE_URL'] = DATABASE_URL
    logging.info(f"Database connection string created with host: {pg_host}")
else:
    logging.warning("PostgreSQL connection environment variables not found")