from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import logging
import os


db = SQLAlchemy()

def get_migrate(app):
    return Migrate(app, db)

def create_db():
    try:
        db.create_all()
        logging.info("Database tables created successfully")
    except Exception as e:
        logging.error(f"Error creating database tables: {str(e)}")
        
def init_db(app):
    try:
        db_uri = app.config.get('SQLALCHEMY_DATABASE_URI', '')
        if db_uri:
            sanitized_uri = db_uri.replace(db_uri.split('@')[0].split('://')[-1], '****:****')
            logging.info(f"Connecting to database: {sanitized_uri}")
        
        db.init_app(app)
        with app.app_context():
            try:
                db.engine.connect()
                logging.info("Database connection successful")
                db.create_all()
                logging.info("Database tables created successfully")
            except Exception as e:
                logging.error(f"Database connection or table creation error: {str(e)}")
                raise
    except Exception as e:
        logging.error(f"Error initializing database: {str(e)}")
        raise