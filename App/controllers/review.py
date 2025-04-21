from App.models import Review
from App.database import db
from App.models import Apartment, Tenant
from sqlalchemy.exc import SQLAlchemyError
from flask_login import current_user
from sqlalchemy import desc
import logging

def create_review(apartment_id, tenant_id, rating, comment, landlord_id=None):
    try:
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
    except SQLAlchemyError as e:
        logging.error(f"Error creating review: {str(e)}")
        db.session.rollback()
        return None

def update_review(review_id, rating, comment):
    try:
        review = Review.query.get(review_id)
        if not review:
            return None
            
        review.rating = rating
        review.comment = comment
        db.session.commit()
        return review
    except SQLAlchemyError as e:
        logging.error(f"Error updating review: {str(e)}")
        db.session.rollback()
        return None
        
def delete_review(review_id):
    try:
        review = Review.query.get(review_id)
        if not review:
            return False
            
        db.session.delete(review)
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        print(f"Error in delete_review: {e}")
        return False

def get_reviews_by_apartment(apartment_id):
    try:
        return Review.query.filter_by(apartment_id=apartment_id).order_by(desc(Review.created_at)).all()
    except SQLAlchemyError as e:
        logging.error(f"Error retrieving reviews: {str(e)}")
        return []

def get_reviews_by_user(user_id):
    """Get all reviews by a user"""
    return Review.query.filter_by(user_id=user_id).all()

def get_average_rating(apartment_id):
    try:
        reviews = Review.query.filter_by(apartment_id=apartment_id).all()
        if not reviews:
            return 0.0
        total = sum(review.rating for review in reviews)
        return round(total / len(reviews), 1)
    except SQLAlchemyError as e:
        logging.error(f"Error calculating average rating: {str(e)}")
        return 0.0

def get_reviews_count(apartment_id):
    try:
        return Review.query.filter_by(apartment_id=apartment_id).count()
    except SQLAlchemyError as e:
        logging.error(f"Error counting reviews: {str(e)}")
        return 0

def get_tenant_reviews(tenant_id):
    try:
        return Review.query.filter_by(tenant_id=tenant_id)\
                           .order_by(desc(Review.created_at))\
                           .all()
    except SQLAlchemyError as e:
        logging.error(f"Error retrieving tenant reviews: {str(e)}")
        return []