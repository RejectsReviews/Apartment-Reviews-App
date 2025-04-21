import os
import logging
from flask import Flask, render_template
from flask_uploads import DOCUMENTS, IMAGES, TEXT, UploadSet, configure_uploads
from flask_cors import CORS
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage

from App.database import init_db
from App.config import load_config

from App.controllers import (
    setup_jwt,
    add_auth_context
)

from App.views import views, setup_admin
from App.controllers.initialize import initialize

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('App.main')

def add_views(app):
    for view in views:
        app.register_blueprint(view)

def init_sample_data(app):
    try:
        with app.app_context():
            # The initialize function will check if data already exists
            logger.info("Initializing sample data...")
            initialize(force_reset=False)
            logger.info("Sample data initialization completed")
    except Exception as e:
        logger.error(f"Error initializing sample data: {str(e)}")

def create_app(overrides={}):
    app = Flask(__name__, static_url_path='/static')
    load_config(app, overrides)
    CORS(app)
    add_auth_context(app)
    
    try:
        photos = UploadSet('photos', TEXT + DOCUMENTS + IMAGES)
        configure_uploads(app, photos)
    except Exception as e:
        logger.error(f"Error configuring uploads: {str(e)}")
    
    add_views(app)
    
    try:
        init_db(app)
        logger.info("Database initialized successfully")
        
        if os.environ.get('ENV') == 'production' or os.environ.get('INIT_DATA') == 'true':
            init_sample_data(app)
    except Exception as e:
        logger.error(f"Error initializing database: {str(e)}")
        
    jwt = setup_jwt(app)
    setup_admin(app)
    
    @jwt.invalid_token_loader
    @jwt.unauthorized_loader
    def custom_unauthorized_response(error):
        return render_template('401.html', error=error), 401
    
    # Add error handling
    @app.errorhandler(500)
    def internal_error(error):
        logger.error(f"Internal server error: {str(error)}")
        return render_template('500.html', error=error), 500
    
    app.app_context().push()
    return app