from App.database import db

class Amenity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)

    def __init__(self, name):
        self.name = name

    def get_json(self):
        return {
            'id': self.id,
            'name': self.name
        }
    
    def get_all_amenities():
        return Amenity.query.all()
    
    def get_all_amenities_json():
        return [amenity.get_json() for amenity in Amenity.query.all()]
    
    def get_amenity_by_id(id):
        return Amenity.query.get(id)
    
    def get_amenity_by_name(name):
        return Amenity.query.filter_by(name=name).first()
    
    def get_amenity_by_name_json(name):
        return [amenity.get_json() for amenity in Amenity.query.filter_by(name=name).all()]
    
    
    
    
