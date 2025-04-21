from App.models import Review
from App.database import db

def create_review(apartment_id, tenant_id, rating, comment, landlord_id=None):
    """Creates a new review in the database"""
    review = Review(
        apartment_id=apartment_id,
        tenant_id=tenant_id,
        rating=rating,
        comment=comment,
        landlord_id=landlord_id
    )
    db.session.add(review)
    db.session.commit()
    return review

def get_reviews_by_apartment(apartment_id):
    """Gets all reviews for an apartment"""
    return Review.get_review_by_apartment_id(apartment_id)

def get_reviews_by_user(user_id):
    """Get all reviews by a user"""
    return Review.query.filter_by(user_id=user_id).all()

def get_average_rating(apartment_id):
    """Calculate the average rating for an apartment"""
    reviews = get_reviews_by_apartment(apartment_id)
    if not reviews or len(reviews) == 0:
        return 0
    
    total = sum(review.rating for review in reviews)
    return round(total / len(reviews), 1)

def get_reviews_count(apartment_id):
    """Get the number of reviews for an apartment"""
    reviews = get_reviews_by_apartment(apartment_id)
    return len(reviews) if reviews else 0