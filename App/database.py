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
        # Handle SQLite configuration
        db_uri = app.config.get('SQLALCHEMY_DATABASE_URI', '')
        if 'sqlite' in db_uri:
            # Ensure SQLite URI is absolute path for Render
            if '///' in db_uri and not db_uri.startswith('sqlite:////'):
                # Convert relative path to absolute for production
                if os.environ.get('ENV') == 'production':
                    # Use a Render-specific directory
                    abs_path = os.path.join(os.getcwd(), 'App', 'app.db')
                    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{abs_path}"
                    logging.info(f"Using absolute SQLite path: {abs_path}")
        
        # Log database connection string
        logging.info(f"Database URI: {app.config.get('SQLALCHEMY_DATABASE_URI', '')}")
        
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