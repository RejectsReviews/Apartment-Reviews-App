from .user import create_user, signup_tenant, signup_landlord
from App.database import db
from App.models import Tenant, Landlord
from App.controllers.amenity import create_amenity, get_amenity_by_name


def initialize():
    db.drop_all()
    db.create_all()
    #Createing the user bob 
    create_user('bob', 'bobpass', 'bob@gmail.com', 'Bob', 'Smith', 'Tenant')
    
    #Test users
    signup_landlord('landlord', '123', 'landlord@example.com', 'John', 'Smith')
    signup_tenant('tenant', '123', 'tenant@example.com', 'Jane', 'Doe', 
                 '555-123-4567', '123 Main St', 'Anytown', 'State')
    
    #Add some amenities
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
    
    return db
