from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import logging
import os


db = SQLAlchemy()
_db_initialized = False

def get_migrate(app):
    return Migrate(app, db)

def create_db():
    try:
        db.create_all()
        logging.info("Database tables created successfully")
    except Exception as e:
        logging.error(f"Error creating database tables: {str(e)}")
        
def init_db(app):
    global _db_initialized
    
    if _db_initialized:
        logging.info("Database already initialized, skipping")
        return
        
    try:
        # Log database connection string (with password removed for security)
        db_uri = app.config.get('SQLALCHEMY_DATABASE_URI', '')
        if db_uri:
            # Hide password in logs
            parts = db_uri.split('@')
            if len(parts) > 1:
                sanitized_uri = f"...@{parts[1]}"
                logging.info(f"Connecting to database: {sanitized_uri}")
        
        # Initialize the database
        db.init_app(app)
        _db_initialized = True
        
        # Create tables
        with app.app_context():
            db.create_all()
            logging.info("Database tables created successfully")
                    
    except Exception as e:
        logging.error(f"Error initializing database: {str(e)}")
        raise