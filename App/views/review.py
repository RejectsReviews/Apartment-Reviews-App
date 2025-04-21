from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app
from flask_jwt_extended import jwt_required, current_user, verify_jwt_in_request, get_jwt_identity
from flask_wtf import FlaskForm
from App.controllers.apartment import get_apartment
from App.controllers.review import create_review, get_tenant_reviews, update_review, delete_review
from App.models import Review, db

review_views = Blueprint('review_views', __name__, template_folder='../templates')

class ReviewForm(FlaskForm):
    pass

@review_views.route('/my-reviews', methods=['GET'])
@jwt_required()
def my_reviews():
    if current_user.user_type != 'Tenant':
        flash('Only tenants can access their reviews')
        return redirect(url_for('index_views.index_page'))
    
    return redirect(url_for('review_views.tenant_reviews'))

@review_views.route('/tenant-reviews', methods=['GET'])
def tenant_reviews():
    is_authenticated = False
    try:
        verify_jwt_in_request()
        user_id = get_jwt_identity()
        is_authenticated = True
        
        if not current_user:
            flash('Authentication error')
            return redirect(url_for('index_views.index_page'))
            
        if current_user.user_type != 'Tenant':
            flash('Only tenants can access their reviews')
            return redirect(url_for('index_views.index_page'))
        
        reviews = get_tenant_reviews(current_user.id)
        return render_template('Html/TenantReviews.html', reviews=reviews, is_authenticated=True, current_user=current_user)
    except Exception as e:
        flash('You must be logged in to access this page')
        return redirect(url_for('auth_views.login_page'))

@review_views.route('/review/<int:review_id>/edit', methods=['GET'])
@jwt_required()
def edit_review_page(review_id):
    review = Review.query.get_or_404(review_id)
    
    if review.tenant_id != current_user.id:
        flash('You can only edit your own reviews')
        return redirect(url_for('review_views.tenant_reviews'))
    
    comment_parts = review.comment.split('\n\n', 1)
    title = comment_parts[0]
    content = comment_parts[1] if len(comment_parts) > 1 else ""
    
    apartment = get_apartment(review.apartment_id)
    form = ReviewForm()
    return render_template('Html/LeaveReview.html', 
                          apartment=apartment, 
                          review=review,
                          edit_mode=True,
                          title=title,
                          content=content,
                          form=form,
                          is_tenant=current_user.user_type == 'Tenant')

@review_views.route('/review/<int:review_id>/edit', methods=['POST'])
@jwt_required()
def update_review_route(review_id):
    review = Review.query.get_or_404(review_id)
    
    if review.tenant_id != current_user.id:
        flash('You can only edit your own reviews')
        return redirect(url_for('review_views.tenant_reviews'))
    
    data = request.form
    rating = int(data.get('rating', 0))
    comment = data.get('content', '')
    title = data.get('title', '')
    apartment_id = data.get('apartment_id', review.apartment_id)
    
    if not (1 <= rating <= 5):
        flash('Rating must be between 1 and 5')
        return redirect(url_for('review_views.edit_review_page', review_id=review_id))
    
    try:
        updated_comment = f"{title}\n\n{comment}"
        result = update_review(review_id, rating, updated_comment)
        if result:
            flash('Review updated successfully!')
        else:
            flash('Error updating review')
        return redirect(url_for('apartment_views.apartment_details', apartment_id=apartment_id))
    except Exception as e:
        flash(f'Error updating review: {str(e)}')
        return redirect(url_for('review_views.edit_review_page', review_id=review_id))

@review_views.route('/review/<int:review_id>/delete', methods=['POST'])
@jwt_required()
def delete_review_route(review_id):
    review = Review.query.get_or_404(review_id)
    
    if review.tenant_id != current_user.id:
        flash('You can only delete your own reviews')
        return redirect(url_for('review_views.tenant_reviews'))
    
    try:
        result = delete_review(review_id)
        if result:
            flash('Review deleted successfully!')
        else:
            flash('Error deleting review')
    except Exception as e:
        flash(f'Error deleting review: {str(e)}')
        
    return redirect(url_for('review_views.tenant_reviews'))

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
    
    if apartment.verified_tenants:
        verified_numbers = [num.strip() for num in apartment.verified_tenants.split('\n')]
        if current_user.phone not in verified_numbers:
            flash('Only verified tenants can leave reviews for this apartment')
            return redirect(url_for('apartment_views.apartment_details', apartment_id=apartment_id))
    
    existing_review = Review.query.filter_by(apartment_id=apartment_id, tenant_id=current_user.id).first()
    if existing_review:
        flash('You have already reviewed this apartment')
        return redirect(url_for('apartment_views.apartment_details', apartment_id=apartment_id))
    
    form = ReviewForm()
    return render_template('Html/LeaveReview.html', apartment=apartment, form=form, is_tenant=True)

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

    if apartment.verified_tenants:
        verified_numbers = [num.strip() for num in apartment.verified_tenants.split('\n')]
        if current_user.phone not in verified_numbers:
            flash('Only verified tenants can leave reviews for this apartment')
            return redirect(url_for('apartment_views.apartment_details', apartment_id=apartment_id))
    
    existing_review = Review.query.filter_by(apartment_id=apartment_id, tenant_id=current_user.id).first()
    if existing_review:
        flash('You have already reviewed this apartment')
        return redirect(url_for('apartment_views.apartment_details', apartment_id=apartment_id))

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