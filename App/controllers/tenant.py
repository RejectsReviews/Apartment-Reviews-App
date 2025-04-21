from App.models import Tenant
from App.database import db

def create_tenant(username, password, email, phone, address=None, city=None, state=None):
    try:
        new_tenant = Tenant(username=username, password=password, phone=phone, 
                          address=address, city=city, state=state, email=email)
        db.session.add(new_tenant)
        db.session.commit()
        return new_tenant
    except Exception as e:
        db.session.rollback()
        return None

def get_tenant_by_username(username):
    return Tenant.query.filter_by(username=username).first()

def get_tenant(id):
    return Tenant.query.get(id)

def get_all_tenants():
    return Tenant.query.all()

def get_all_tenants_json():
    tenants = Tenant.query.all()
    if not tenants:
        return []
    return [tenant.get_json() for tenant in tenants]

def verify_tenant(id):
    tenant = get_tenant(id)
    if tenant:
        tenant.verified = True
        db.session.add(tenant)
        db.session.commit()
        return tenant
    return None 