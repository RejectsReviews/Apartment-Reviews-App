from App.models import Apartment, Amenity
from App.database import db

def create_apartment(landlord_id, title, description, address, city, price, bedrooms, bathrooms, verified_tenants=None):
    try:
        new_apartment = Apartment(
            landlord_id=landlord_id,
            title=title,
            description=description,
            address=address,
            city=city,
            price=price,
            bedrooms=bedrooms,
            bathrooms=bathrooms,
            verified_tenants=verified_tenants
        )
        db.session.add(new_apartment)
        db.session.commit()
        return new_apartment
    except Exception as e:
        db.session.rollback()
        return None

def get_apartment(apartment_id):
    """Get apartment by ID"""
    return Apartment.query.get(apartment_id)

def get_all_apartments():
    """Get all apartments"""
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

def save_apartment_for_tenant(apartment_id, tenant):
    """Save an apartment for a tenant"""
    try:
        apartment = Apartment.query.get(apartment_id)
        if apartment and apartment not in tenant.saved_apartments:
            tenant.saved_apartments.append(apartment)
            db.session.commit()
            return True
        return False
    except Exception as e:
        db.session.rollback()
        return False

def unsave_apartment_for_tenant(apartment_id, tenant):
    """Remove an apartment from a tenant's saved list"""
    try:
        apartment = Apartment.query.get(apartment_id)
        if apartment and apartment in tenant.saved_apartments:
            tenant.saved_apartments.remove(apartment)
            db.session.commit()
            return True
        return False
    except Exception as e:
        db.session.rollback()
        return False