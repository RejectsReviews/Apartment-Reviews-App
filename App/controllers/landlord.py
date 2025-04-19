from App.models import Landlord
from App.database import db

def create_landlord(username, password, name, email):
    try:
        new_landlord = Landlord(username=username, password=password, name=name, email=email)
        db.session.add(new_landlord)
        db.session.commit()
        return new_landlord
    except Exception as e:
        db.session.rollback()
        return None

def get_landlord_by_username(username):
    return Landlord.query.filter_by(username=username).first()

def get_landlord(id):
    return Landlord.query.get(id)

def get_all_landlords():
    return Landlord.query.all()

def get_all_landlords_json():
    landlords = Landlord.query.all()
    if not landlords:
        return []
    return [landlord.get_json() for landlord in landlords] 