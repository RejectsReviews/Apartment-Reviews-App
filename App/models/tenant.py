from App.database import db
from App.models.user import User

class Tenant(User):
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    verified = db.Column(db.Boolean, default=False)
    phone = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    reviews = db.relationship('Review', backref='tenant', lazy=True)
    
    __mapper_args__ = {
        'polymorphic_identity': 'tenant',
    }

    def __init__(self, username, password, email, first_name, last_name, phone, address, city, state):
        super().__init__(username, password, email, first_name, last_name, 'Tenant')
        self.phone = phone
        self.address = address
        self.city = city
        self.state = state

    def get_json(self):
        return {**super().get_json(), 'phone': self.phone, 'address': self.address, 
                'city': self.city, 'state': self.state, 'verified': self.verified}
    
    @staticmethod
    def get_all_tenants():
        return Tenant.query.all()
    
    @staticmethod
    def get_all_tenants_json():
        return [tenant.get_json() for tenant in Tenant.query.all()]
    
    @staticmethod
    def get_tenant_by_id(id):
        return Tenant.query.get(id)
    
    @staticmethod
    def get_tenant_by_username(username):
        return Tenant.query.filter_by(username=username).first()
    
    
