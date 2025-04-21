from .user import create_user, signup_tenant, signup_landlord
from App.database import db
from App.models import Tenant, Landlord
from App.controllers.amenity import create_amenity, get_amenity_by_name, get_or_create_amenity
from App.controllers.apartment import create_apartment, add_amenity_to_apartment
from App.controllers.review import create_review
import os
import shutil


def initialize():
    db.drop_all()
    db.create_all()
    #Creating the user bob 
    bob = signup_tenant('bob', 'bobpass', 'bob@gmail.com', 'Bob', 'Smith', '5555555555')
    
    # Create landlords
    landlord1 = signup_landlord('johnsmith', 'password123', 'john.smith@example.com', 'John', 'Smith')
    landlord2 = signup_landlord('sarahwilson', 'password123', 'sarah.wilson@example.com', 'Sarah', 'Wilson')
    landlord3 = signup_landlord('mikerodriguez', 'password123', 'mike.rodriguez@example.com', 'Mike', 'Rodriguez')
    
    # Create tenants
    tenant1 = signup_tenant('janedoe', 'password123', 'jane.doe@example.com', 'Jane', 'Doe', '5551234567')
    tenant2 = signup_tenant('bobthompson', 'password123', 'bob.thompson@example.com', 'Bob', 'Thompson', '5552345678')
    tenant3 = signup_tenant('emilywong', 'password123', 'emily.wong@example.com', 'Emily', 'Wong', '5553456789')
    tenant4 = signup_tenant('davidjones', 'password123', 'david.jones@example.com', 'David', 'Jones', '5554567890')
    
    # Add some amenities
    common_amenities = [
        "WiFi", "Air Conditioning", "Parking", "Laundry", "Pool", "Gym", "Security", "Furnished",
        "Balcony", "Dishwasher", "Walk-in Closet", "Central Heating", "Elevator", "Hardwood Floors",
        "Stainless Steel Appliances", "Ceiling Fan", "Patio/Deck", "Garbage Disposal", "Pets Allowed",
        "Storage", "Wheelchair Access", "Garden/Yard", "Smart Home Features", "Fire Alarm",
        "Gas Stove", "High Ceilings", "Concierge", "Microwave", "Cable Ready",

        "In-Unit Washer/Dryer", "Fitness Center", "Rooftop Terrace", "Business Center", 
        "Electric Vehicle Charging", "Tennis Court", "Basketball Court", "Playground",
        "Dog Park", "Bike Storage", "Package Lockers", "Doorman", "Waterfront View", 
        "Mountain View", "City View", "Open Floor Plan", "Quartz Countertops", 
        "Granite Countertops", "Energy Efficient Appliances", "Solar Panels", 
        "Walk-in Shower", "Jacuzzi Tub", "Double Vanity", "Heated Bathroom Floors",
        "Heated Pool", "Hot Tub", "Sauna", "Steam Room", "Movie Theater",
        "Game Room", "Clubhouse", "BBQ Area", "Outdoor Kitchen", "Fire Pit",
        "24/7 Maintenance", "On-site Management", "Gated Community", "Controlled Access", 
        "Key Fob Entry", "Video Surveillance", "Valet Trash", "Recycling", "Composting",
        "Guest Parking", "Covered Parking", "Underground Parking", "Guest Suite",
        "Co-working Space", "Yoga Studio", "Wine Cellar", "Pet Grooming Station",
        "Window Coverings", "Closet Organizers", "Built-in Bookshelves", "Fireplace"
    ]
    
    for amenity_name in common_amenities:
        if not get_amenity_by_name(amenity_name):
            create_amenity(amenity_name)
    
    # Create Bob's special apartment that he can review
    bob_apartment = create_apartment(
        landlord_id=landlord1.id,
        title="Bob's Apartment - DEMO UNIT",
        description="This is a special demo apartment for Bob to review. It features a spectacular view of the city, modern amenities, and a convenient location.",
        address="1 Saddle Road, Maraval",
        city="Port of Spain",
        price=1800,
        bedrooms=2,
        bathrooms=1,
        verified_tenants="5555555555"  # Bob is a verified tenant
    )
    
    # Add nice amenities to Bob's apartment
    bob_apt_amenities = ["WiFi", "Air Conditioning", "Furnished", "Balcony", "City View", "Pool", "Gym", "Hardwood Floors"]
    for amenity_name in bob_apt_amenities:
        amenity = get_amenity_by_name(amenity_name)
        if amenity:
            add_amenity_to_apartment(bob_apartment.id, amenity.id)
    
    # Create apartments for landlords with verified tenants
    # Landlord 1's apartments
    apt1 = create_apartment(
        landlord_id=landlord1.id,
        title="Luxurious 2BR Downtown Apartment",
        description="Beautiful apartment with stunning views of the city skyline. Modern appliances, spacious living areas, and a prime downtown location.",
        address="28 Victoria Avenue",
        city="Port of Spain",
        price=2500,
        bedrooms=2,
        bathrooms=2,
        verified_tenants="5551234567\n5552345678"  # Jane and Bob are verified tenants
    )
    
    apt2 = create_apartment(
        landlord_id=landlord1.id,
        title="Cozy 1BR Studio Near University",
        description="Perfect for students! This studio apartment is within walking distance to the university and all major amenities.",
        address="25 Cipero Street",
        city="San Fernando",
        price=1200,
        bedrooms=1,
        bathrooms=1,
        verified_tenants="5553456789"  # Emily is a verified tenant
    )
    
    # Landlord 2's apartments
    apt3 = create_apartment(
        landlord_id=landlord2.id,
        title="Family-Friendly 3BR House",
        description="Spacious family home in a quiet neighborhood. Large backyard, updated kitchen, and close to schools and parks.",
        address="22 Tumpuna Road",
        city="Arima",
        price=3200,
        bedrooms=3,
        bathrooms=2.5,
        verified_tenants="5554567890"  # David is a verified tenant
    )
    
    apt4 = create_apartment(
        landlord_id=landlord2.id,
        title="Modern 2BR Condo with Beach Access",
        description="Stunning beachfront condo with direct access to the sand. Fully furnished with high-end finishes and breathtaking ocean views.",
        address="Las Cuevas Beach Road",
        city="Las Cuevas",
        price=2800,
        bedrooms=2,
        bathrooms=2,
        verified_tenants=""  # No verified tenants yet
    )
    
    # Landlord 3's apartments
    apt5 = create_apartment(
        landlord_id=landlord3.id,
        title="Upscale 4BR Villa with Pool",
        description="Luxury villa with private pool and garden. Perfect for entertaining with a gourmet kitchen and spacious living areas.",
        address="#5 3rd Avenue, Oropune",
        city="Tunapuna-Piarco",
        price=4500,
        bedrooms=4,
        bathrooms=3.5,
        verified_tenants=""  # No verified tenants yet
    )
    
    # Add amenities to apartments
    # Apartment 1 amenities
    amenities1 = ["WiFi", "Air Conditioning", "Dishwasher", "Hardwood Floors", "Stainless Steel Appliances", "City View", "Elevator", "Security"]
    for amenity_name in amenities1:
        amenity = get_amenity_by_name(amenity_name)
        if amenity:
            add_amenity_to_apartment(apt1.id, amenity.id)
    
    # Apartment 2 amenities
    amenities2 = ["WiFi", "Air Conditioning", "Furnished", "Laundry", "Cable Ready", "Microwave", "Storage"]
    for amenity_name in amenities2:
        amenity = get_amenity_by_name(amenity_name)
        if amenity:
            add_amenity_to_apartment(apt2.id, amenity.id)
    
    # Apartment 3 amenities
    amenities3 = ["WiFi", "Air Conditioning", "Parking", "Garden/Yard", "Pets Allowed", "Dishwasher", "Patio/Deck"]
    for amenity_name in amenities3:
        amenity = get_amenity_by_name(amenity_name)
        if amenity:
            add_amenity_to_apartment(apt3.id, amenity.id)
    
    # Apartment 4 amenities
    amenities4 = ["WiFi", "Air Conditioning", "Furnished", "Balcony", "Waterfront View", "Pool", "Walk-in Closet", "Ceiling Fan"]
    for amenity_name in amenities4:
        amenity = get_amenity_by_name(amenity_name)
        if amenity:
            add_amenity_to_apartment(apt4.id, amenity.id)
    
    # Apartment 5 amenities
    amenities5 = ["WiFi", "Air Conditioning", "Pool", "Gym", "Furnished", "Fireplace", "Walk-in Shower", "Double Vanity", "Smart Home Features"]
    for amenity_name in amenities5:
        amenity = get_amenity_by_name(amenity_name)
        if amenity:
            add_amenity_to_apartment(apt5.id, amenity.id)
    
    # Add reviews
    # Reviews for Apartment 1
    create_review(
        apartment_id=apt1.id,
        tenant_id=tenant1.id,
        rating=5,
        comment="Perfect location in downtown. The apartment is spacious, modern, and the views are incredible! The landlord was very responsive and helpful.",
        landlord_id=landlord1.id
    )
    
    create_review(
        apartment_id=apt1.id,
        tenant_id=tenant2.id,
        rating=4,
        comment="Great apartment overall. Clean, well-maintained, and convenient location. The only downside is occasional noise from the street.",
        landlord_id=landlord1.id
    )
    
    # Reviews for Apartment 2
    create_review(
        apartment_id=apt2.id,
        tenant_id=tenant3.id,
        rating=5,
        comment="Perfect for students! Located right next to campus and has everything I need. The landlord addressed any issues promptly.",
        landlord_id=landlord1.id
    )
    
    # Reviews for Apartment 3
    create_review(
        apartment_id=apt3.id,
        tenant_id=tenant4.id,
        rating=3,
        comment="Nice neighborhood but the house needs some maintenance. The backyard is great but there are some plumbing issues that need attention.",
        landlord_id=landlord2.id
    )
    
    # Setup image directories and add sample images for apartments
    UPLOAD_FOLDER = 'App/static/images/apartments'
    
    # Create the base directory if it doesn't exist
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    
    # Function to set up apartment images
    def setup_apartment_images(apartment_id, cover_image, additional_images=[]):
        # Create directory for this apartment
        apartment_dir = os.path.join(UPLOAD_FOLDER, str(apartment_id))
        os.makedirs(apartment_dir, exist_ok=True)
        
        # Add cover image
        sample_path = f'App/static/images/sample/{cover_image}'
        if os.path.exists(sample_path):
            shutil.copy(sample_path, os.path.join(apartment_dir, f'cover_{cover_image}'))
        
        # Add additional images
        for idx, img in enumerate(additional_images):
            sample_path = f'App/static/images/sample/{img}'
            if os.path.exists(sample_path):
                shutil.copy(sample_path, os.path.join(apartment_dir, f'additional_{idx+1}_{img}'))
    
    # Ensure the sample directory exists
    sample_dir = 'App/static/images/sample'
    os.makedirs(sample_dir, exist_ok=True)
    
    # Create placeholder sample images if they don't exist
    # In a real app, you would have actual image files here
    # This is just to make sure the code doesn't break if images aren't available
    placeholder_images = [
        'apartment1_cover.jpg', 'apartment1_1.jpg', 'apartment1_2.jpg',
        'apartment2_cover.jpg', 'apartment2_1.jpg',
        'apartment3_cover.jpg', 'apartment3_1.jpg', 'apartment3_2.jpg',
        'apartment4_cover.jpg', 'apartment4_1.jpg',
        'apartment5_cover.jpg', 'apartment5_1.jpg', 'apartment5_2.jpg',
        'bob_apartment_cover.jpg', 'bob_apartment_1.jpg'
    ]
    
    # Try to setup the apartment images
    # Note: This will succeed only if sample images exist
    try:
        # Bob's apartment
        setup_apartment_images(
            bob_apartment.id, 
            'bob_apartment_cover.jpg',
            ['bob_apartment_1.jpg', 'bob_apartment_2.jpg']
        )
        
        # Apartment 1
        setup_apartment_images(
            apt1.id, 
            'apartment1_cover.jpg',
            ['apartment1_1.jpg', 'apartment1_2.jpg', 'apartment1_3.jpg']
        )
        
        # Apartment 2
        setup_apartment_images(
            apt2.id, 
            'apartment2_cover.jpg',
            ['apartment2_1.jpg', 'apartment2_2.jpg']
        )
        
        # Apartment 3
        setup_apartment_images(
            apt3.id, 
            'apartment3_cover.jpg',
            ['apartment3_1.jpg', 'apartment3_2.jpg']
        )
        
        # Apartment 4
        setup_apartment_images(
            apt4.id, 
            'apartment4_cover.jpg',
            ['apartment4_1.jpg', 'apartment4_2.jpg', 'apartment4_3.jpg']
        )
        
        # Apartment 5
        setup_apartment_images(
            apt5.id, 
            'apartment5_cover.jpg',
            ['apartment5_1.jpg', 'apartment5_2.jpg']
        )
    except Exception as e:
        print(f"Warning: Could not set up apartment images. Please ensure sample images exist in {sample_dir}. Error: {str(e)}")
        print("The app will still work, but apartments will not have images.")
    
    return db
