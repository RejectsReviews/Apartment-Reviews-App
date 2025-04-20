# blue prints are imported 
# explicitly instead of using *
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from .index import index_views
from .user import user_views
from .auth import auth_views
from .apartment import apartment_views
from .admin import setup_admin

views = [index_views, user_views, auth_views, apartment_views] 
# blueprints must be added to this list