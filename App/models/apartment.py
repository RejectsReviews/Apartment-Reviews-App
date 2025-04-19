from App.database import db

class Apartment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    landlord_id = db.Column(db.Integer, db.ForeignKey('landlord.id'), nullable=False)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=True)
    address = db.Column(db.String(200), nullable=False)
    city = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Float, nullable=False)
    bedrooms = db.Column(db.Integer, nullable=False)
    bathrooms = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())
    amenities = db.relationship('Amenity', secondary='apartment_amenity', backref=db.backref('apartments', lazy='dynamic'))
    tenant_id = db.Column(db.Integer, db.ForeignKey('tenant.id'), nullable=True)

    def __init__(self, landlord_id, title, description, address, city, price, bedrooms, bathrooms):
        self.landlord_id = landlord_id
        self.title = title
        self.description = description
        self.address = address
        self.city = city
        self.price = price
        self.bedrooms = bedrooms
        self.bathrooms = bathrooms

    def get_json(self):
        return {
            'id': self.id,
            'landlord_id': self.landlord_id,
            'title': self.title,
            'description': self.description,
            'address': self.address,
            'city': self.city,
            'price': self.price,
            'bedrooms': self.bedrooms,
            'bathrooms': self.bathrooms,
            'created_at': self.created_at,
            'tenant_id': self.tenant_id
        }
    
    def get_all_apartments():
        return Apartment.query.all()
    
    def get_all_apartments_json():
        return [apartment.get_json() for apartment in Apartment.query.all()]
    
    def get_apartment_by_id(id):
        return Apartment.query.get(id)
    
    def get_apartment_by_landlord_id(landlord_id):
        return Apartment.query.filter_by(landlord_id=landlord_id).all()
    
    def get_apartment_by_landlord_id_json(landlord_id):
        return [apartment.get_json() for apartment in Apartment.query.filter_by(landlord_id=landlord_id).all()]
    
    def get_apartment_by_tenant_id(tenant_id):
        return Apartment.query.filter_by(tenant_id=tenant_id).all()
    
    def get_apartment_by_tenant_id_json(tenant_id):
        return [apartment.get_json() for apartment in Apartment.query.filter_by(tenant_id=tenant_id).all()]
    
    def get_apartment_by_title(title):
        return Apartment.query.filter_by(title=title).all()
    
    def get_apartment_by_title_json(title):
        return [apartment.get_json() for apartment in Apartment.query.filter_by(title=title).all()]
    
    
    
    

