from App.database import db
from App.models.user import User

class Landlord(User):
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    apartments = db.relationship('Apartment', backref='landlord', lazy=True)
    reviews = db.relationship('Review', backref='landlord', lazy=True)
    
    __mapper_args__ = {
        'polymorphic_identity': 'landlord',
    }
    
    def __init__(self, username, password, email, first_name, last_name):
        super().__init__(username, password, email, first_name, last_name, 'Landlord')

    def get_json(self):
        return super().get_json()
    
    @staticmethod
    def get_all_landlords():
        return Landlord.query.all()
    
    @staticmethod
    def get_all_landlords_json():
        return [landlord.get_json() for landlord in Landlord.query.all()]
    
    @staticmethod
    def get_landlord_by_id(id):
        return Landlord.query.get(id)
    
    @staticmethod
    def get_landlord_by_username(username):
        return Landlord.query.filter_by(username=username).first()
