from .user import create_user, signup_tenant, signup_landlord
from App.database import db


def initialize():
    db.drop_all()
    db.create_all()
    #Createing the user bob 
    create_user('bob', 'bobpass', 'bob@gmail.com', 'Bob', 'Smith', 'Tenant')
    
    #Test users
    signup_landlord('landlord', '123', 'landlord@example.com', 'John', 'Smith')
    signup_tenant('tenant', '123', 'tenant@example.com', 'Jane', 'Doe', 
                 '555-123-4567', '123 Main St', 'Anytown', 'State')
