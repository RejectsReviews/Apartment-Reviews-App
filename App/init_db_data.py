import logging
from .models.user import User
from .models.apartment import Apartment
from .models.review import Review
from werkzeug.security import generate_password_hash
from .database import db
import datetime

def init_sample_data():
    """Initialize sample data in the database for demonstration purposes"""
    try:
        # Check if we already have data
        if User.query.first() is not None:
            logging.info("Database already contains data, skipping initialization")
            return
            
        logging.info("Initializing sample data in the database")
        
        # Create sample users
        admin = User(
            username="admin",
            email="admin@example.com",
            password=generate_password_hash("admin123"),
            first_name="Admin",
            last_name="User",
            is_admin=True
        )
        
        landlord = User(
            username="landlord",
            email="landlord@example.com",
            password=generate_password_hash("landlord123"),
            first_name="Sample",
            last_name="Landlord",
            is_landlord=True
        )
        
        tenant = User(
            username="tenant",
            email="tenant@example.com",
            password=generate_password_hash("tenant123"),
            first_name="Sample",
            last_name="Tenant"
        )
        
        db.session.add_all([admin, landlord, tenant])
        db.session.commit()
        
        # Create sample apartment
        apartment = Apartment(
            landlord_id=landlord.id,
            title="Sample Apartment",
            description="A beautiful apartment in a great neighborhood",
            address="123 Main Street",
            city="Sample City",
            price=1500,
            bedrooms=2,
            bathrooms=1,
            verified_tenants=1
        )
        
        db.session.add(apartment)
        db.session.commit()
        
        # Create sample review
        review = Review(
            apartment_id=apartment.id,
            user_id=tenant.id,
            rating=4,
            title="Great place to live",
            content="I really enjoyed my time at this apartment. The location is perfect and the landlord is responsive.",
            created_at=datetime.datetime.now()
        )
        
        db.session.add(review)
        db.session.commit()
        
        logging.info("Sample data initialized successfully")
    except Exception as e:
        db.session.rollback()
        logging.error(f"Error initializing sample data: {str(e)}") 