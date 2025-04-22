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

# Enable SSL for PostgreSQL - this is crucial for Render's PostgreSQL
os.environ['PGSSLMODE'] = 'require'

# Set this before any other imports that might use psycopg2
os.environ['PGSSLROOTCERT'] = 'rds-ca-2019-root.pem'

# Use the direct DATABASE_URL from environment if available
if 'DATABASE_URL' in os.environ:
    # Make sure the URL is compatible with psycopg2's SSL requirements
    db_url = os.environ['DATABASE_URL']
    if '?' not in db_url:
        db_url += '?sslmode=require'
    elif 'sslmode=' not in db_url:
        db_url += '&sslmode=require'
    os.environ['DATABASE_URL'] = db_url
    logging.info("Using DATABASE_URL from environment with SSL enabled")
else:
    # Construct PostgreSQL connection string from environment variables
    pg_host = os.environ.get('POSTGRES_URL')
    pg_user = os.environ.get('POSTGRES_USER')
    pg_password = os.environ.get('POSTGRES_PASSWORD')
    pg_db = os.environ.get('POSTGRES_DB')

    if pg_host and pg_user and pg_password and pg_db:
        DATABASE_URL = f"postgresql://{pg_user}:{pg_password}@{pg_host}/{pg_db}?sslmode=require"
        os.environ['DATABASE_URL'] = DATABASE_URL
        logging.info(f"Created DATABASE_URL with host: {pg_host}")