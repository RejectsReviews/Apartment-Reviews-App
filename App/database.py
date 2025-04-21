from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import logging
import os
import time


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
        # Log database connection string (with password removed for security)
        db_uri = app.config.get('SQLALCHEMY_DATABASE_URI', '')
        if db_uri:
            # Hide password in logs
            sanitized_uri = db_uri.replace(db_uri.split('@')[0].split('://')[-1], '****:****')
            logging.info(f"Connecting to database: {sanitized_uri}")
        
        # Initialize the database
        db.init_app(app)
        
        # Try to create tables with retry logic
        with app.app_context():
            max_retries = 3
            retry_count = 0
            use_sqlite_fallback = os.environ.get('USE_SQLITE_FALLBACK', 'false').lower() == 'true'
            
            while retry_count < max_retries:
                try:
                    # Check connection before creating tables
                    db.engine.connect().close()
                    logging.info("Database connection successful")
                    
                    # Create all tables
                    db.create_all()
                    logging.info("Database tables created successfully")
                    
                    # Success - break out of retry loop
                    break
                    
                except Exception as e:
                    retry_count += 1
                    logging.error(f"Database connection error (attempt {retry_count}/{max_retries}): {str(e)}")
                    
                    if retry_count >= max_retries:
                        if use_sqlite_fallback:
                            logging.warning("Max retries reached. Falling back to SQLite database")
                            app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fallback.db'
                            
                            # Reinitialize with SQLite
                            db.init_app(app)
                            db.create_all()
                            logging.info("SQLite fallback database initialized")
                        else:
                            logging.error("Max retries reached. No fallback configured.")
                            raise
                    
                    # Wait before retrying
                    time.sleep(2)
                    
    except Exception as e:
        logging.error(f"Error initializing database: {str(e)}")
        raise