# routes/courses.py

from flask import Blueprint, redirect, url_for, flash, render_template
from flask_login import current_user, login_required
from app import db
from app.models import Course

courses_bp = Blueprint('courses', __name__, url_prefix='/courses')

@courses_bp.route('/enroll/<int:course_id>', methods=['POST'])
@login_required
def enroll(course_id):
    course = Course.query.get(course_id)
    if course:
        if course not in current_user.courses:
            current_user.courses.append(course)
            db.session.commit()
            flash('You have successfully enrolled in the course!', 'success')
        else:
            flash('You are already enrolled in this course.', 'warning')
    else:
        flash('Course not found.', 'danger')

    return redirect(url_for('courses.course_list'))


@login_required
def course_details(course_id):
    course = Course.query.get(course_id)
    if course:
        return render_template('course_details.html', course=course)
    else:
        flash('Course not found.', 'danger')
        return redirect(url_for('courses.course_list'))


@courses_bp.route('/payment', methods=['GET'])
def payment():
    return render_template('payment.html', stripe_public_key=app.config['STRIPE_PUBLIC_KEY'])

@courses_bp.route('/process_payment', methods=['POST'])
def process_payment():
    stripe.api_key = app.config['STRIPE_SECRET_KEY']

    # Get the payment token from the form submission
    token = request.form['stripeToken']

    # Create a charge with the token
    try:
        charge = stripe.Charge.create(
            amount=1000,  # Replace with the actual amount in cents
            currency='usd',
            source=token,
            description='Payment for Course Access'
        )

        # TODO: Add logic to update the user's access to premium content or courses in the database
        # For example, update the 'premium_access' field in the User model to True.

        flash('Payment successful!', 'success')
        return redirect(url_for('courses.course_list'))
    except stripe.error.CardError as e:
        # Display error to the user
        flash(f'Error: {e.error.message}', 'danger')
        return redirect(url_for('courses.payment'))
