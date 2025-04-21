from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app
from flask_jwt_extended import jwt_required, current_user
from flask_wtf import FlaskForm
from App.controllers.apartment import get_apartment
from App.controllers.review import create_review
from App.models import Review, db

review_views = Blueprint('review_views', __name__, template_folder='../templates')

class ReviewForm(FlaskForm):
    pass

@review_views.route('/apartments/<int:apartment_id>/review', methods=['GET'])
@jwt_required()
def leave_review(apartment_id):
    if current_user.user_type != 'Tenant':
        flash('Only tenants can leave reviews')
        return redirect(url_for('apartment_views.apartment_details', apartment_id=apartment_id))
    
    apartment = get_apartment(apartment_id)
    if not apartment:
        flash('Apartment not found')
        return redirect(url_for('apartment_views.apartments_listing'))
    
    form = ReviewForm()
    return render_template('Html/LeaveReview.html', apartment=apartment, form=form)

@review_views.route('/apartments/<int:apartment_id>/review', methods=['POST'])
@jwt_required()
def submit_review(apartment_id):
    if current_user.user_type != 'Tenant':
        flash('Only tenants can leave reviews')
        return redirect(url_for('apartment_views.apartment_details', apartment_id=apartment_id))
    
    form = ReviewForm()
    if not form.validate_on_submit():
        flash('Invalid form submission')
        return redirect(url_for('review_views.leave_review', apartment_id=apartment_id))
        
    apartment = get_apartment(apartment_id)
    if not apartment:
        flash('Apartment not found')
        return redirect(url_for('apartment_views.apartments_listing'))

    data = request.form
    rating = int(data.get('rating', 0))
    comment = data.get('content', '')
    title = data.get('title', '')

    if not (1 <= rating <= 5):
        flash('Rating must be between 1 and 5')
        return redirect(url_for('review_views.leave_review', apartment_id=apartment_id))

    try:
        review = create_review(
            apartment_id=apartment_id,
            tenant_id=current_user.id,
            rating=rating,
            comment=f"{title}\n\n{comment}",
            landlord_id=apartment.landlord_id
        )
        flash('Review submitted successfully!')
        return redirect(url_for('apartment_views.apartment_details', apartment_id=apartment_id))
    except Exception as e:
        flash(f'Error submitting review: {str(e)}')
        return redirect(url_for('review_views.leave_review', apartment_id=apartment_id))