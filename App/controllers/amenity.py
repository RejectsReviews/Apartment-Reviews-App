from App.models import Amenity
from App.database import db

def create_amenity(name):
    try:
        new_amenity = Amenity(name=name)
        db.session.add(new_amenity)
        db.session.commit()
        return new_amenity
    except Exception as e:
        db.session.rollback()
        return None

def get_amenity(id):
    return Amenity.query.get(id)

def get_amenity_by_name(name):
    return Amenity.query.filter_by(name=name).first()

def get_all_amenities():
    return Amenity.query.all()

def get_all_amenities_json():
    amenities = Amenity.query.all()
    if not amenities:
        return []
    return [amenity.get_json() for amenity in amenities] 