# routes/auth.py

from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models.user import User
from app.forms import LoginForm

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Logged in successfully!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password.', 'danger')

    return render_template('login.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully!', 'info')
    return redirect(url_for('index'))


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful. You can now log in.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('register.html', form=form)


@auth_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', user=current_user)


@auth_bp.route('/profile_settings', methods=['GET', 'POST'])
@login_required
def profile_settings():
    if request.method == 'POST':
        # Update the user's profile information
        current_user.email = request.form['email']
        current_user.first_name = request.form['first_name']
        current_user.last_name = request.form['last_name']

        # Add other fields to update user settings

        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('auth.profile_settings'))

    return render_template('profile_settings.html')


@app.route('/courses')
def courses():
    # Render the 'courses.html' template for the Courses page
    return render_template('courses.html')


if __name__ == '__main__':
    # Create the necessary database tables and run the Flask app in debug mode
    create_tables()
    app.run(debug=True
