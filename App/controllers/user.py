from App.models import User, Tenant, Landlord
from App.database import db

def create_user(username, password, email, first_name, last_name, user_type):
    newuser = User(username=username, password=password, email=email, 
                  first_name=first_name, last_name=last_name, user_type=user_type)
    db.session.add(newuser)
    db.session.commit()
    return newuser

def signup_tenant(username, password, email, first_name, last_name, phone, address, city, state):
    tenant = Tenant(
        username=username, 
        password=password, 
        email=email, 
        first_name=first_name, 
        last_name=last_name, 
        phone=phone,
        address=address,
        city=city,
        state=state
    )
    db.session.add(tenant)
    db.session.commit()
    return tenant

def signup_landlord(username, password, email, first_name, last_name):
    landlord = Landlord(
        username=username, 
        password=password, 
        email=email, 
        first_name=first_name, 
        last_name=last_name
    )
    db.session.add(landlord)
    db.session.commit()
    return landlord

def get_user_by_username(username):
    return User.query.filter_by(username=username).first()

def get_user(id):
    return User.query.get(id)

def get_all_users():
    return User.query.all()

def get_all_users_json():
    users = User.query.all()
    if not users:
        return []
    users = [user.get_json() for user in users]
    return users

def update_user(id, username):
    user = get_user(id)
    if user:
        user.username = username
        db.session.add(user)
        return db.session.commit()
    return None
    