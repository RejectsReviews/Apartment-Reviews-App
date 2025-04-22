# gunicorn_config.py
import multiprocessing
import os
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)

# The socket to bind.
bind = "0.0.0.0:10000"  # Render uses port 10000 by default

# The number of worker processes for handling requests.
workers = 4

# Use the 'gevent' worker type for async performance.
worker_class = 'gevent'

# Log level
loglevel = 'info'

# Where to log to
accesslog = '-'  # '-' means log to stdout
errorlog = '-'  # '-' means log to stderr

# Render automatically provides DATABASE_URL environment variable
# for connected PostgreSQL databases
if 'DATABASE_URL' in os.environ:
    db_url = os.environ['DATABASE_URL']
    # Ensure SSL mode is set for PostgreSQL
    if 'postgresql' in db_url and '?' not in db_url:
        db_url += '?sslmode=require'
    elif 'postgresql' in db_url and 'sslmode=' not in db_url:
        db_url += '&sslmode=require'
    
    os.environ['DATABASE_URL'] = db_url
    logging.info("Using DATABASE_URL from environment")