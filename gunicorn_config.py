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

# Set environment variables for SQLite
os.environ['ENV'] = 'production'
os.environ['INIT_DATA'] = 'true'
logging.info("Using SQLite database configuration")