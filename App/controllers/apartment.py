from App.models import Apartment, Amenity
from App.database import db

def create_apartment(landlord_id, title, description, address, city, price, bedrooms, bathrooms):
    try:
        new_apartment = Apartment(
            landlord_id=landlord_id,
            title=title,
            description=description,
            address=address,
            city=city,
            price=price,
            bedrooms=bedrooms,
            bathrooms=bathrooms
        )
        db.session.add(new_apartment)
        db.session.commit()
        return new_apartment
    except Exception as e:
        db.session.rollback()
        return None

def get_apartment(id):
    return Apartment.query.get(id)

def get_all_apartments():
    return Apartment.query.all()

def get_all_apartments_json():
    apartments = Apartment.query.all()
    if not apartments:
        return []
    return [apartment.get_json() for apartment in apartments]

def add_amenity_to_apartment(apartment_id, amenity_id):
    try:
        apartment = Apartment.query.get(apartment_id)
        amenity = Amenity.query.get(amenity_id)
        
        if apartment and amenity:
            apartment.amenities.append(amenity)
            db.session.commit()
            return True
        return False
    except Exception as e:
        db.session.rollback()
        return False

def remove_amenity_from_apartment(apartment_id, amenity_id):
    try:
        apartment = Apartment.query.get(apartment_id)
        amenity = Amenity.query.get(amenity_id)
        
        if apartment and amenity and amenity in apartment.amenities:
            apartment.amenities.remove(amenity)
            db.session.commit()
            return True
        return False
    except Exception as e:
        db.session.rollback()
        return False

def get_apartment_amenities(apartment_id):
    apartment = Apartment.query.get(apartment_id)
    if apartment:
        return apartment.amenities
    return [] 