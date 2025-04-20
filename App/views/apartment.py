from flask import Blueprint, render_template, jsonify, request, flash, redirect, url_for, current_app
from flask_jwt_extended import jwt_required, current_user
import os
from werkzeug.utils import secure_filename

from App.controllers import get_all_apartments, add_amenity_to_apartment

apartment_views = Blueprint('apartment_views', __name__, template_folder='../templates')

# Configure image upload settings
UPLOAD_FOLDER = 'App/static/images/apartments'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#function to get apartment images
def get_apartment_images(apartment_id, image_type='all'):
    apartment_dir = os.path.join(UPLOAD_FOLDER, str(apartment_id))
    if not os.path.exists(apartment_dir):
        return []
    
    all_images = [f for f in os.listdir(apartment_dir) 
                if os.path.isfile(os.path.join(apartment_dir, f))
                and allowed_file(f)]
    
    if image_type == 'cover':
        cover_images = [img for img in all_images if img.startswith('cover_')]
        return cover_images[0] if cover_images else None
    elif image_type == 'additional':
        return [img for img in all_images if not img.startswith('cover_')]
    else:
        return all_images

@apartment_views.record_once
def register_template_utils(state):
    app = state.app
    app.jinja_env.globals['get_apartment_images'] = get_apartment_images

@apartment_views.route('/apartments', methods=['GET'])
@jwt_required()
def apartments_listing():
    apartments = get_all_apartments()
    return render_template('Html/ApartmentsListing.html', 
                          apartments=apartments,
                          is_tenant=(current_user.user_type == 'Tenant'))

@apartment_views.route('/apartments/create', methods=['GET'])
@jwt_required()
def create_apartment_page():
    if current_user.user_type != 'Landlord':
        flash('Only landlords can create listings')
        return redirect(url_for('apartment_views.apartments_listing'))
    return render_template('Html/ApartmentCreation.html')

@apartment_views.route('/apartments/create', methods=['POST'])
@jwt_required()
def create_apartment_action():
    if current_user.user_type != 'Landlord':
        flash('Only landlords can create listings')
        return redirect(url_for('apartment_views.apartments_listing'))
    
    try:
        data = request.form
        from App.controllers.apartment import create_apartment
        from App.controllers.amenity import get_or_create_amenity
        
        new_apartment = create_apartment(
            landlord_id=current_user.id,
            title=data['title'],
            description=data['description'],
            address=data['address'],
            city=data['city'],
            price=float(data['price']),
            bedrooms=int(data['bedrooms']),
            bathrooms=int(data['bathrooms'])
        )
        
        if not new_apartment:
            flash('Error creating apartment listing'), 400
            return redirect(url_for('apartment_views.create_apartment_page'))
        
        amenities = request.form.getlist('amenities')
        for amenity_name in amenities:
            amenity = get_or_create_amenity(amenity_name)
            if amenity:
                add_amenity_to_apartment(new_apartment.id, amenity.id)
        
        apartment_dir = os.path.join(UPLOAD_FOLDER, str(new_apartment.id))
        os.makedirs(apartment_dir, exist_ok=True)
        
        if 'cover_image' in request.files:
            cover_file = request.files['cover_image']
            if cover_file and allowed_file(cover_file.filename):
                filename = secure_filename(cover_file.filename)
                cover_filename = f"cover_{filename}"
                cover_file.save(os.path.join(apartment_dir, cover_filename))
        
        if 'additional_images' in request.files:
            additional_files = request.files.getlist('additional_images')
            for file in additional_files:
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(apartment_dir, filename))
        
        flash('Apartment listing created successfully!')
        return redirect(url_for('apartment_views.apartments_listing'))
    except Exception as e:
        flash(f'Error: {str(e)}'), 400
        return redirect(url_for('apartment_views.create_apartment_page'))

@apartment_views.route('/apartments/<int:apartment_id>', methods=['GET'])
@jwt_required()
def apartment_details(apartment_id):
    from App.controllers.apartment import get_apartment
    from App.controllers.landlord import get_landlord
    
    apartment = get_apartment(apartment_id)
    if not apartment:
        flash('Apartment not found')
        return redirect(url_for('apartment_views.apartments_listing'))
    
    cover_image = get_apartment_images(apartment_id, 'cover')
    additional_images = get_apartment_images(apartment_id, 'additional')
    
    landlord = get_landlord(apartment.landlord_id)
    
    return render_template('Html/ListingDetails.html', 
                          apartment=apartment,
                          cover_image=cover_image,
                          additional_images=additional_images,
                          landlord=landlord,
                          is_tenant=(current_user.user_type == 'Tenant')) 