from App.database import db
from App.models.user import User

class Landlord(User):
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    apartments = db.relationship('Apartment', backref='landlord', lazy=True)
    reviews = db.relationship('Review', backref='landlord', lazy=True)
    
    def __init__(self, username, password, name, email):
        super().__init__(username, password, email)
        self.name = name

    def get_json(self):
        return super().get_json()
    
    def get_all_landlords():
        return Landlord.query.all()
    
    def get_all_landlords_json():
        return [landlord.get_json() for landlord in Landlord.query.all()]
    
    def get_landlord_by_id(id):
        return Landlord.query.get(id)
    
    def get_landlord_by_username(username):
        return Landlord.query.filter_by(username=username).first()
