from flask import Blueprint, render_template, jsonify, request, flash, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user, unset_jwt_cookies, set_access_cookies
from App.database import db
from App.models import User, Tenant
from.index import index_views
from.apartment import apartment_views

from App.controllers import (
    login,
    create_user,
    get_all_users,
    signup_tenant,
    signup_landlord
)

auth_views = Blueprint('auth_views', __name__, template_folder='../templates')




'''
Page/Action Routes
'''    
@auth_views.route('/users', methods=['GET'])
def get_user_page():
    users = get_all_users()
    return render_template('users.html', users=users)

@auth_views.route('/identify', methods=['GET'])
@jwt_required()
def identify_page():
    return render_template('message.html', title="Identify", message=f"You are logged in as {current_user.id} - {current_user.username}")
    
@auth_views.route('/login', methods=['GET'])
def login_page():
    return render_template('Html/login.html')

@auth_views.route('/signup', methods=['GET'])
def signup_page():
    return render_template('Html/signup.html')

@auth_views.route('/signup', methods=['POST'])
def signup_action():
    data = request.form
    
    if data['password'] != data['confirm_password']:
        flash('Passwords do not match'), 400
        return redirect(url_for('auth_views.signup_page'))
    
    # Validate phone number
    phone = data.get('phone', '').strip()
    if not phone.isdigit() or len(phone) != 10:
        flash('Phone number must be exactly 10 digits'), 400
        return redirect(url_for('auth_views.signup_page'))
    
    # Check for existing phone number
    if data['user_type'] == 'Tenant':
        existing_tenant = db.session.query(Tenant).filter(Tenant.phone == phone).first()
        if existing_tenant:
            flash('An account with this phone number already exists'), 400
            return redirect(url_for('auth_views.signup_page'))
    
    # Check for existing username or email
    user = User.query.filter((User.username == data['username']) | (User.email == data['email'])).first()
    if user:
        flash('Username or email already exists'), 400
        return redirect(url_for('auth_views.signup_page'))
    
    try:
        if data['user_type'] == 'Tenant':
            user = signup_tenant(
                username=data['username'],
                password=data['password'],
                email=data['email'],
                first_name=data['first_name'],
                last_name=data['last_name'],
                phone=phone,
                address=data.get('address', ''),
                city=data.get('city', ''),
                state=data.get('state', '')
            )
        else:
            user = signup_landlord(
                username=data['username'],
                password=data['password'],
                email=data['email'],
                first_name=data['first_name'],
                last_name=data['last_name']
            )
            
        if user:
            flash('Account created successfully!')
            return redirect(url_for('auth_views.login_page'))
        else:
            flash('Error creating account'), 400
            return redirect(url_for('auth_views.signup_page'))
    except Exception as e:
        flash(f'Error: {str(e)}'), 400
        return redirect(url_for('auth_views.signup_page'))

@auth_views.route('/login', methods=['POST'])
def login_action():
    data = request.form
    token = login(data['username'], data['password'])
    if not token:
        flash('Invalid username or password'), 401
        return redirect(url_for('auth_views.login_page'))
    else:
        response = redirect(url_for('apartment_views.public_apartments_listing'))
        set_access_cookies(response, token)
        flash('Logged in successfully!')
        return response

@auth_views.route('/logout', methods=['GET'])
def logout_action():
    response = redirect(url_for('apartment_views.public_apartments_listing'))
    flash("Logged Out!")
    unset_jwt_cookies(response)
    return response

'''
API Routes
'''

@auth_views.route('/api/login', methods=['POST'])
def user_login_api():
    data = request.json
    token = login(data['username'], data['password'])
    if not token:
        return jsonify({"error": "Invalid username or password"}), 401
    response = jsonify(access_token=token) 
    set_access_cookies(response, token)
    return response

@auth_views.route('/api/identify', methods=['GET'])
@jwt_required()
def identify_user():
    return jsonify({'message': f"username: {current_user.username}, id : {current_user.id}"})

@auth_views.route('/api/logout', methods=['GET'])
def logout_api():
    response = jsonify(message="Logged Out!")
    unset_jwt_cookies(response)
    return response