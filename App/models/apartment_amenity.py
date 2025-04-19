from App.database import db

# Association table for many-to-many relationship between Apartment and Amenity
apartment_amenity = db.Table('apartment_amenity',
    db.Column('apartment_id', db.Integer, db.ForeignKey('apartment.id'), primary_key=True),
    db.Column('amenity_id', db.Integer, db.ForeignKey('amenity.id'), primary_key=True)
) 