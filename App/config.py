import os
import logging

def load_config(app, overrides):
    if os.path.exists(os.path.join('./App', 'custom_config.py')):
        app.config.from_object('App.custom_config')
    else:
        app.config.from_object('App.default_config')
    app.config.from_prefixed_env()
    
    # Prioritize DATABASE_URL from environment over config files
    database_url = os.environ.get('DATABASE_URL')
    use_sqlite_fallback = os.environ.get('USE_SQLITE_FALLBACK', 'false').lower() == 'true'
    
    if database_url:
        try:
            # Log database connection settings (without credentials)
            db_parts = database_url.split('@')
            if len(db_parts) > 1:
                masked_url = f"...@{db_parts[1]}"
                logging.info(f"Attempting to connect to database: {masked_url}")
            
            # Set the database URI from environment
            app.config['SQLALCHEMY_DATABASE_URI'] = database_url
            
            # If sqlite fallback is enabled, set a timeout and backup URI
            if use_sqlite_fallback:
                logging.info("SQLite fallback enabled")
                app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
                    'connect_args': {'connect_timeout': 5}
                }
                app.config['SQLALCHEMY_BINDS'] = {
                    'fallback': 'sqlite:///fallback.db'
                }
        except Exception as e:
            logging.error(f"Error configuring database: {str(e)}")
            if use_sqlite_fallback:
                logging.warning("Falling back to SQLite database")
                app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fallback.db'
        
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.config['PREFERRED_URL_SCHEME'] = 'https'
    app.config['UPLOADED_PHOTOS_DEST'] = "App/uploads"
    app.config['JWT_ACCESS_COOKIE_NAME'] = 'access_token'
    app.config["JWT_TOKEN_LOCATION"] = ["cookies", "headers"]
    app.config["JWT_COOKIE_SECURE"] = True
    app.config["JWT_COOKIE_CSRF_PROTECT"] = False
    app.config['FLASK_ADMIN_SWATCH'] = 'darkly'
    for key in overrides:
        app.config[key] = overrides[key]