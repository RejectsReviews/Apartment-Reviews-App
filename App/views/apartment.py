from flask import Blueprint, render_template, jsonify, request, flash, redirect, url_for, current_app
from flask_jwt_extended import jwt_required, current_user, get_jwt_identity, verify_jwt_in_request
from App.database import db
import os
from werkzeug.utils import secure_filename
import shutil

from App.controllers import (
    get_all_apartments, 
    add_amenity_to_apartment,
    get_reviews_by_apartment,
    get_apartment,
    save_apartment_for_tenant,
    unsave_apartment_for_tenant,
    update_apartment,
    delete_apartment,
    get_apartments_by_landlord
)

from App.controllers.review import get_average_rating, get_reviews_count

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
    
    # Register rating controller functions as filters
    @app.template_filter('get_apartment_reviews')
    def get_apartment_reviews_filter(apartment_id):
        """Get all reviews for an apartment to use in templates"""
        from App.models.review import Review
        return Review.query.filter_by(apartment_id=apartment_id).all()
    
    @app.template_filter('get_average_rating')
    def get_average_rating_filter(apartment_id):
        """Get average rating for an apartment"""
        return get_average_rating(apartment_id)
    
    @app.template_filter('get_reviews_count')
    def get_reviews_count_filter(apartment_id):
        """Get number of reviews for an apartment"""
        return get_reviews_count(apartment_id)

@apartment_views.route('/public-apartments', methods=['GET'])
def public_apartments_listing():
    """Public apartments listing that doesn't require authentication"""
    amenity = request.args.get('amenity')
    location = request.args.get('location')
    
    apartments = get_all_apartments()
    
    if amenity:
        # Filter apartments that have the selected amenity
        filtered_apartments = []
        for apartment in apartments:
            if any(a.name == amenity for a in apartment.amenities):
                filtered_apartments.append(apartment)
        apartments = filtered_apartments
    
    if location:
        # Filter by location (city or address)
        location = location.lower()
        filtered_apartments = []
        for apartment in apartments:
            if (location in apartment.city.lower() or 
                location in apartment.address.lower()):
                filtered_apartments.append(apartment)
        apartments = filtered_apartments
    
    # Get authentication status and user type
    is_authenticated = False
    is_tenant = False
    
    # Try to verify JWT without raising exceptions
    try:
        verify_jwt_in_request(optional=True)
        # If user is authenticated, get_jwt_identity() will return the identity, otherwise None
        if get_jwt_identity() is not None:
            is_authenticated = True
            # If authenticated, we can safely access current_user
            is_tenant = current_user.user_type == 'Tenant'
    except Exception as e:
        # Just in case something goes wrong
        print(f"JWT verification error: {str(e)}")
        pass
    
    # Get all available amenities for the filter dropdown
    from App.controllers.amenity import get_all_amenities
    all_amenities = get_all_amenities()

    return render_template('Html/PublicApartmentsListing.html', 
                         apartments=apartments,
                         is_tenant=is_tenant,
                         is_authenticated=is_authenticated,
                         all_amenities=all_amenities)

@apartment_views.route('/apartments', methods=['GET'])
@jwt_required()
def apartments_listing():
    amenity = request.args.get('amenity')
    location = request.args.get('location')
    
    apartments = get_all_apartments()
    
    if amenity:
        # Filter apartments that have the selected amenity
        filtered_apartments = []
        for apartment in apartments:
            if any(a.name == amenity for a in apartment.amenities):
                filtered_apartments.append(apartment)
        apartments = filtered_apartments
    
    if location:
        # Filter by location (city or address)
        location = location.lower()
        filtered_apartments = []
        for apartment in apartments:
            if (location in apartment.city.lower() or 
                location in apartment.address.lower()):
                filtered_apartments.append(apartment)
        apartments = filtered_apartments
    
    # Get all available amenities for the filter dropdown
    from App.controllers.amenity import get_all_amenities
    all_amenities = get_all_amenities()

    return render_template('Html/ApartmentsListing.html', 
                         apartments=apartments,
                         is_tenant=(current_user.user_type == 'Tenant'),
                         all_amenities=all_amenities)

@apartment_views.route('/apartments/create', methods=['GET'])
@jwt_required()
def create_apartment_page():
    if current_user.user_type != 'Landlord':
        flash('Only landlords can create listings')
        return redirect(url_for('apartment_views.apartments_listing'))
    
    # Get all available amenities for the form
    from App.controllers.amenity import get_all_amenities
    all_amenities = get_all_amenities()
    
    return render_template('Html/ApartmentCreation.html', all_amenities=all_amenities)

@apartment_views.route('/apartments/create', methods=['POST'])
@jwt_required()
def create_apartment_action():
    if current_user.user_type != 'Landlord':
        flash('Only landlords can create listings', 'apartment_error')
        return redirect(url_for('apartment_views.apartments_listing'))
    
    try:
        data = request.form
        from App.controllers.apartment import create_apartment
        from App.controllers.amenity import get_or_create_amenity
        
        verified_tenants = data.get('verified_tenants', '').strip()
        
        new_apartment = create_apartment(
            landlord_id=current_user.id,
            title=data['title'],
            description=data['description'],
            address=data['address'],
            city=data['city'],
            price=float(data['price']),
            bedrooms=int(data['bedrooms']),
            bathrooms=float(data['bathrooms']),
            verified_tenants=verified_tenants
        )
        
        if not new_apartment:
            flash('Error creating apartment listing', 'apartment_error')
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
        
        flash('Apartment listing created successfully!', 'apartment_success')
        return redirect(url_for('apartment_views.apartments_listing'))
    except Exception as e:
        flash(f'Error: {str(e)}', 'apartment_error')
        return redirect(url_for('apartment_views.create_apartment_page'))

@apartment_views.route('/apartments/<int:apartment_id>', methods=['GET'])
def apartment_details(apartment_id):
    from App.controllers.apartment import get_apartment
    from App.controllers.landlord import get_landlord
    
    apartment = get_apartment(apartment_id)
    if not apartment:
        flash('Apartment not found')
        return redirect(url_for('apartment_views.public_apartments_listing'))
    
    cover_image = get_apartment_images(apartment_id, 'cover')
    additional_images = get_apartment_images(apartment_id, 'additional')
    
    landlord = get_landlord(apartment.landlord_id)
    reviews = get_reviews_by_apartment(apartment_id)
    
    # Get authentication status and user type
    is_authenticated = False
    is_tenant = False
    
    # Try to verify JWT without raising exceptions
    try:
        verify_jwt_in_request(optional=True)
        # If user is authenticated, get_jwt_identity() will return the identity, otherwise None
        if get_jwt_identity() is not None:
            is_authenticated = True
            # If authenticated, we can safely access current_user
            is_tenant = current_user.user_type == 'Tenant'
    except Exception as e:
        # Just in case something goes wrong
        print(f"JWT verification error: {str(e)}")
        pass
    
    return render_template('Html/ListingDetails.html', 
                          apartment=apartment,
                          cover_image=cover_image,
                          additional_images=additional_images,
                          landlord=landlord,
                          reviews=reviews,
                          is_tenant=is_tenant,
                          is_authenticated=is_authenticated)

@apartment_views.route('/api/locations', methods=['GET'])
@jwt_required()
def get_locations():
    query = request.args.get('query', '').lower()
    apartments = get_all_apartments()
    
    # Get unique locations (both cities and addresses)
    locations = set()
    for apartment in apartments:
        if apartment.city and query in apartment.city.lower():
            locations.add(apartment.city)
        if apartment.address and query in apartment.address.lower():
            locations.add(apartment.address)
    
    return jsonify(list(sorted(locations)))

@apartment_views.route('/apartments/<int:apartment_id>/save', methods=['POST'])
@jwt_required()
def save_apartment(apartment_id):
    if current_user.user_type != 'Tenant':
        return jsonify({'error': 'Only tenants can save apartments'}), 403
    
    apartment = get_apartment(apartment_id)
    if not apartment:
        return jsonify({'error': 'Apartment not found'}), 404
        
    if apartment not in current_user.saved_apartments:
        current_user.saved_apartments.append(apartment)
        db.session.commit()
    
    return jsonify({'message': 'Apartment saved successfully'})

@apartment_views.route('/apartments/<int:apartment_id>/unsave', methods=['POST'])
@jwt_required()
def unsave_apartment(apartment_id):
    if current_user.user_type != 'Tenant':
        return jsonify({'error': 'Only tenants can unsave apartments'}), 403
    
    apartment = get_apartment(apartment_id)
    if not apartment:
        return jsonify({'error': 'Apartment not found'}), 404
        
    if apartment in current_user.saved_apartments:
        current_user.saved_apartments.remove(apartment)
        db.session.commit()
    
    return jsonify({'message': 'Apartment removed from saved'})

@apartment_views.route('/saved-apartments', methods=['GET'])
@jwt_required()
def saved_apartments():
    if current_user.user_type != 'Tenant':
        flash('Only tenants can access saved apartments')
        return redirect(url_for('apartment_views.apartments_listing'))
        
    return render_template('Html/ApartmentsListing.html', 
                         apartments=current_user.saved_apartments,
                         is_tenant=True)

@apartment_views.route('/my-properties', methods=['GET'])
@jwt_required()
def my_properties():
    """Show landlord's properties"""
    if current_user.user_type != 'Landlord':
        flash('Only landlords can access their properties')
        return redirect(url_for('apartment_views.apartments_listing'))
    
    # Get all apartments by this landlord
    apartments = get_apartments_by_landlord(current_user.id)
    
    return render_template('Html/MyProperties.html', apartments=apartments)

@apartment_views.route('/apartments/<int:apartment_id>/edit', methods=['GET'])
@jwt_required()
def edit_apartment(apartment_id):
    """Show edit form for an apartment"""
    if current_user.user_type != 'Landlord':
        flash('Only landlords can edit listings')
        return redirect(url_for('apartment_views.apartments_listing'))
    
    apartment = get_apartment(apartment_id)
    if not apartment:
        flash('Apartment not found')
        return redirect(url_for('apartment_views.my_properties'))
    
    # Make sure this apartment belongs to the current landlord
    if apartment.landlord_id != current_user.id:
        flash('You can only edit your own listings')
        return redirect(url_for('apartment_views.my_properties'))
    
    # Get all available amenities for the form
    from App.controllers.amenity import get_all_amenities
    all_amenities = get_all_amenities()
    
    return render_template('Html/EditApartment.html', apartment=apartment, all_amenities=all_amenities)

@apartment_views.route('/apartments/<int:apartment_id>/edit', methods=['POST'])
@jwt_required()
def edit_apartment_action(apartment_id):
    """Process apartment edit form"""
    if current_user.user_type != 'Landlord':
        flash('Only landlords can edit listings', 'apartment_error')
        return redirect(url_for('apartment_views.apartments_listing'))
    
    apartment = get_apartment(apartment_id)
    if not apartment:
        flash('Apartment not found', 'apartment_error')
        return redirect(url_for('apartment_views.my_properties'))
    
    # Make sure this apartment belongs to the current landlord
    if apartment.landlord_id != current_user.id:
        flash('You can only edit your own listings', 'apartment_error')
        return redirect(url_for('apartment_views.my_properties'))
    
    try:
        from App.controllers.amenity import get_or_create_amenity
        
        data = request.form
        
        # Update apartment details
        updated_apartment = update_apartment(
            apartment_id=apartment_id,
            title=data['title'],
            description=data['description'],
            address=data['address'],
            city=data['city'],
            price=float(data['price']),
            bedrooms=int(data['bedrooms']),
            bathrooms=float(data['bathrooms']),
            verified_tenants=data.get('verified_tenants', '').strip()
        )
        
        if not updated_apartment:
            flash('Error updating apartment listing', 'apartment_error')
            return redirect(url_for('apartment_views.edit_apartment', apartment_id=apartment_id))
        
        # Clear existing amenities and add the new ones
        updated_apartment.amenities.clear()
        db.session.commit()
        
        amenities = request.form.getlist('amenities')
        for amenity_name in amenities:
            amenity = get_or_create_amenity(amenity_name)
            if amenity:
                add_amenity_to_apartment(apartment_id, amenity.id)
        
        # Handle image uploads
        apartment_dir = os.path.join(UPLOAD_FOLDER, str(apartment_id))
        os.makedirs(apartment_dir, exist_ok=True)
        
        # Check if we need to remove all existing images
        if 'remove_all_images' in request.form:
            # Remove all files in the apartment directory
            for file in os.listdir(apartment_dir):
                file_path = os.path.join(apartment_dir, file)
                if os.path.isfile(file_path):
                    os.remove(file_path)
        
        # Handle cover image upload
        if 'cover_image' in request.files:
            cover_file = request.files['cover_image']
            if cover_file and cover_file.filename and allowed_file(cover_file.filename):
                # Remove existing cover images
                for file in os.listdir(apartment_dir):
                    if file.startswith('cover_'):
                        os.remove(os.path.join(apartment_dir, file))
                
                # Save new cover image
                filename = secure_filename(cover_file.filename)
                cover_filename = f"cover_{filename}"
                cover_file.save(os.path.join(apartment_dir, cover_filename))
        
        # Handle additional images upload
        if 'additional_images' in request.files:
            additional_files = request.files.getlist('additional_images')
            for file in additional_files:
                if file and file.filename and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    if not filename.startswith('cover_'):  # Make sure we don't overwrite the cover image
                        file.save(os.path.join(apartment_dir, filename))
        
        flash('Apartment updated successfully!', 'apartment_success')
        return redirect(url_for('apartment_views.my_properties'))
    
    except Exception as e:
        flash(f'Error: {str(e)}', 'apartment_error')
        return redirect(url_for('apartment_views.edit_apartment', apartment_id=apartment_id))

@apartment_views.route('/apartments/<int:apartment_id>/delete', methods=['GET'])
@jwt_required()
def delete_apartment_route(apartment_id):
    """Delete an apartment listing"""
    if current_user.user_type != 'Landlord':
        flash('Only landlords can delete listings')
        return redirect(url_for('apartment_views.apartments_listing'))
    
    apartment = get_apartment(apartment_id)
    if not apartment:
        flash('Apartment not found')
        return redirect(url_for('apartment_views.my_properties'))
    
    # Make sure this apartment belongs to the current landlord
    if apartment.landlord_id != current_user.id:
        flash('You can only delete your own listings')
        return redirect(url_for('apartment_views.my_properties'))
    
    try:
        # Delete the apartment
        from App.controllers.apartment import delete_apartment as delete_apartment_func
        if delete_apartment_func(apartment_id):
            # Delete all images associated with this apartment
            apartment_dir = os.path.join(UPLOAD_FOLDER, str(apartment_id))
            if os.path.exists(apartment_dir):
                shutil.rmtree(apartment_dir)
            
            flash('Apartment listing deleted successfully')
        else:
            flash('Error deleting apartment listing')
        
        return redirect(url_for('apartment_views.my_properties'))
    
    except Exception as e:
        flash(f'Error: {str(e)}')
        return redirect(url_for('apartment_views.my_properties'))