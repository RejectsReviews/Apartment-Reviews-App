from App.database import db

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    apartment_id = db.Column(db.Integer, db.ForeignKey('apartment.id'), nullable=False)
    tenant_id = db.Column(db.Integer, db.ForeignKey('tenant.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.now())

    def __init__(self, apartment_id, tenant_id, rating, comment):
        self.apartment_id = apartment_id
        self.tenant_id = tenant_id
        self.rating = rating
        self.comment = comment

    def get_json(self):
        return {
            'id': self.id,
            'apartment_id': self.apartment_id,
            'tenant_id': self.tenant_id,
            'rating': self.rating,
            'comment': self.comment,
            'created_at': self.created_at
        }
    
    def get_all_reviews():
        return Review.query.all()
    
    def get_all_reviews_json():
        return [review.get_json() for review in Review.query.all()]
    
    def get_review_by_id(id):
        return Review.query.get(id)
    
    def get_review_by_apartment_id(apartment_id):
        return Review.query.filter_by(apartment_id=apartment_id).all()
    
    def get_review_by_apartment_id_json(apartment_id):
        return [review.get_json() for review in Review.query.filter_by(apartment_id=apartment_id).all()]
    
    def get_review_by_tenant_id(tenant_id):
        return Review.query.filter_by(tenant_id=tenant_id).all()
    
    def get_review_by_tenant_id_json(tenant_id):
        return [review.get_json() for review in Review.query.filter_by(tenant_id=tenant_id).all()]
    
    
    
        
    
