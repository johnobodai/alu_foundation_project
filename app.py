from flask import Flask, render_template, request, redirect, url_for, session, g
from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo
import pymysql
import bcrypt
import secrets
from flask_login import LoginManager, UserMixin
import pymysql.cursors


# csrf = CSRFProtect(app)
app = Flask(__name__, template_folder='templates')
login_manager = LoginManager(app)
login_manager.init_app(app)
app.secret_key = 'your_secret_key'


# Configuration for MySQL database
db_config = {
    'host': 'localhost',
    'user': 'j0hn',
    'password': 'w14gs005.asdfghjkl',
    'database': 'digigirls_db',
}


def get_db():
    if 'db' not in g:
        g.db = pymysql.connect(**db_config, autocommit=True)
    return g.db

def create_tables():
    with pymysql.connect(**db_config, autocommit=True) as conn:
        with conn.cursor() as cursor:
            # Create the users table
            cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                                id INT AUTO_INCREMENT PRIMARY KEY,
                                email VARCHAR(255) NOT NULL,
                                password VARCHAR(255) NOT NULL,
                                title VARCHAR(255),
                                first_name VARCHAR(255),
                                last_name VARCHAR(255),
                                age INT,
                                gender VARCHAR(50),
                                country VARCHAR(100)
                            )''')

            # Create the password_reset_tokens table
            cursor.execute('''CREATE TABLE IF NOT EXISTS password_reset_tokens (
                                email VARCHAR(255) NOT NULL,
                                token VARCHAR(255) NOT NULL,
                                expiration TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                                PRIMARY KEY (email, token),
                                FOREIGN KEY (email) REFERENCES users (email) ON DELETE CASCADE
                            )''')

            # Create the courses table
            cursor.execute('''CREATE TABLE IF NOT EXISTS courses (
                                id INT AUTO_INCREMENT PRIMARY KEY,
                                course_name VARCHAR(255) NOT NULL,
                                instructor VARCHAR(255),
                                description TEXT,
                                start_date DATE,
                                end_date DATE
                            )''')

            # Create the course_resources table
            cursor.execute('''CREATE TABLE IF NOT EXISTS course_resources (
                                id INT AUTO_INCREMENT PRIMARY KEY,
                                course_id INT NOT NULL,
                                resource_name VARCHAR(255) NOT NULL,
                                resource_url VARCHAR(255) NOT NULL,
                                FOREIGN KEY (course_id) REFERENCES courses (id) ON DELETE CASCADE
                            )''')

            # Create the enrollments table
            cursor.execute('''CREATE TABLE IF NOT EXISTS enrollments (
                                id INT AUTO_INCREMENT PRIMARY KEY,
                                user_id INT NOT NULL,
                                course_id INT NOT NULL,
                                enrollment_date DATE NOT NULL,
                                FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
                                FOREIGN KEY (course_id) REFERENCES courses (id) ON DELETE CASCADE
                            )''')
            conn.commit()


def get_user_by_email(email):
    # Fetch user data from the database based on the email
    conn = get_db()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
    user = cursor.fetchone()
    conn.close()
    return user


class User(UserMixin):
    def __init__(self, user_id):
        self.id = user_id

#class RegistrationForm(FlaskForm):
#    email = StringField('Email', validators=[DataRequired(), Email()])
#    password = PasswordField('Password', validators=[DataRequired()])
#    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
#    submit = SubmitField('Register')


@login_manager.user_loader
def load_user(user_id):
    # Replace this with your actual user loading code, e.g., fetching from a database
    return User(user_id)


@app.route('/')
def index():
    # Render the 'index.html' template as the landing page
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Process the registration form data when it's submitted
        title = request.form['title']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        age = int(request.form['age'])
        gender = request.form['gender']
        country = request.form['country']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        # Insert the new user data into the 'users' table in the database
        conn = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, db=DB_NAME)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO users (title, first_name, last_name, age, gender, country, email, password)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ''', (title, first_name, last_name, age, gender, country, email, hashed_password))
        conn.commit()
        conn.close()

        # Redirect to the login page after successful registration
        return redirect(url_for('login'))

    # Render the 'register.html' template for GET requests (displaying the registration form)
    return render_template('register')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Process the login form data when it's submitted
        email = request.form['email']
        password = request.form['password']

        # Connect to the database
        conn = get_db()
        cursor = conn.cursor()

        try:
            # Query the database for a user with the provided email
            cursor.execute('SELECT id, password FROM users WHERE email=%s', (email,))
            user = cursor.fetchone()

            if user and bcrypt.checkpw(password.encode('utf-8'), user[1].encode('utf-8')):
                # User with the provided credentials exists and password matches, set the user_id in the session
                session['user_id'] = user[0]

                # Redirect to the dashboard after successful login
                return redirect(url_for('dashboard'))
            else:
                # If the login credentials are incorrect, show an error message
                error_message = 'Invalid email or password. Please try again.'
                return render_template('login.html', error_message=error_message)

        except Exception as e:
            # Handle any database errors or exceptions
            print("Database Error:", str(e))

        finally:
            # Close the database connection
            conn.close()

    # If the request method is 'GET', render the login form
    return render_template('login.html', error_message=None)


@app.route('/dashboard')
def dashboard():
    # Check if the user is logged in
    if 'user_id' in session:
        # Get the user_id from the session
        user_id = session['user_id']

        # Query the database to get the user's details
        conn = get_db()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE id = %s', (user_id,))
        user = cursor.fetchone()
        conn.close()

        # Pass the user details to the 'dashboard.html' template
        return render_template('dashboard.html', current_user=user)
    else:
        # If the user is not logged in, redirect to the login page
        return redirect(url_for('login'))


@app.route('/about')
def about():
    # Render the 'about.html' template for the About Us page
    return render_template('about.html')


@app.route('/contact')
def contact():
    # Render the 'contact.html' template for the Contact Us page
    return render_template('contact.html')


@app.route('/courses')
def courses():
    # Render the 'courses.html' template for the Courses page
    return render_template('courses.html')


@app.route('/logout', methods=['POST'])
def logout():
    # Clear the user's session to log them out
    session.clear()
    return redirect(url_for('index'))


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        return redirect(url_for('dashboard'))
    return render_template('signup.html')  # Replace 'signup.html' with the actual template for signup page


@app.route('/profile')
def profile():
    # Check if the user is logged in (i.e., their user_id is in the session)
    if 'user_id' in session:
        # Get the user_id from the session
        user_id = session['user_id']

        # Query the database to get the user's details
        conn = get_db()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE id = %s', (user_id,))
        user = cursor.fetchone()
        conn.close()

        # Pass the user details to the 'profile.html' template
        return render_template('profile.html', user=user)
    else:
        # If the user is not logged in, redirect to the login page
        return redirect(url_for('login'))


@app.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    if 'user_id' in session:
        # Get the user_id from the session
        user_id = session['user_id']

        if request.method == 'POST':
            # Process the form data when it's submitted for profile update
            title = request.form['title']
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            age = int(request.form['age'])
            gender = request.form['gender']
            country = request.form['country']

            # Update the user's profile in the database
            conn = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, db=DB_NAME)
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE users
                SET title = %s, first_name = %s, last_name = %s, age = %s, gender = %s, country = %s
                WHERE id = %s
            ''', (title, first_name, last_name, age, gender, country, user_id))
            conn.commit()
            conn.close()

            # Redirect to the dashboard after profile update
            return redirect(url_for('dashboard'))

        else:
            # Fetch the user's details from the database for displaying the current profile
            conn = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, db=DB_NAME)
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute('SELECT * FROM users WHERE id = %s', (user_id,))
            user = cursor.fetchone()
            conn.close()

            # Pass the user details to the 'edit_profile.html' template for editing
            return render_template('edit_profile.html', current_user=user)

    else:
        # If the user is not logged in, redirect to the login page
        return redirect(url_for('login'))


def save_reset_token(email, token):
    # Save the password reset token in the database
    conn = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, db=DB_NAME)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO password_reset_tokens (email, token) VALUES (%s, %s)', (email, token))
    conn.commit()
    conn.close()

def get_reset_token(email):
    # Fetch the password reset token from the database based on the email
    conn = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, db=DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT token, timestamp FROM password_reset_tokens WHERE email = %s', (email,))
    token_data = cursor.fetchone()
    conn.close()
    return token_data

def is_token_expired(token_data):
    # Check if the password reset token is expired (valid for 1 hour)
    if not token_data:
        return True
    timestamp = token_data[1]
    expiration_time = datetime.datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S') + datetime.timedelta(hours=1)
    return datetime.datetime.now() > expiration_time

def update_user_password(email, new_password):
    # Update the user's password in the database
    conn = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, db=DB_NAME)
    cursor = conn.cursor()
    cursor.execute('UPDATE users SET password = %s WHERE email = %s', (new_password, email))
    conn.commit()
    conn.close()

def remove_reset_token(email):
    # Remove the password reset token from the database after it's used or expired
    conn = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, db=DB_NAME)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM password_reset_tokens WHERE email = %s', (email,))
    conn.commit()
    conn.close()

@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        # Process the forgot password form data when it's submitted
        email = request.form['email']

        # Check if the email exists in the database
        user = get_user_by_email(email)
        if not user:
            error_message = 'Email not found. Please enter a valid email address.'
            return render_template('forgot_password.html', error_message=error_message)

        # Generate a password reset token
        token = secrets.token_urlsafe(32)

        # Save the password reset token in the database
        save_reset_token(email, token)

        # Send the password reset link to the user's email (you need to implement this part)

        # Render the 'forgot_password_success.html' template
        return render_template('forgot_password_success.html', email=email)

    # Render the 'forgot_password.html' template for GET requests (displaying the forgot password form)
    return render_template('forgot_password.html', error_message=None)

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    # Fetch the password reset token from the database based on the provided token
    token_data = get_reset_token(token)

    # Check if the token is valid and not expired
    if is_token_expired(token_data):
        return render_template('reset_password_expired.html')

    if request.method == 'POST':
        # Process the reset password form data when it's submitted
        new_password = request.form['new_password']

        # Get the email associated with the password reset token
        email = token_data[0]

        # Update the user's password in the database
        hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
        update_user_password(email, hashed_password)

        # Remove the password reset token from the database
        remove_reset_token(email)

        # Render the 'reset_password_success.html' template
        return render_template('reset_password_success.html')

    # Render the 'reset_password.html' template for GET requests (displaying the reset password form)
    return render_template('reset_password.html', token=token)


@app.route('/faq')
def faq():
    # Add the logic for your FAQ page here
    return render_template('faq.html')

@app.route('/progress')
def progress():
    # Add any logic or data fetching related to the progress page here (if needed)
    # For now, we'll just render the 'progress.html' template.
    return render_template('progress.html')


@app.route('/enroll/<int:course_id>', methods=['GET', 'POST'])
def enroll(course_id):
    conn = get_db()
    cursor = conn.cursor()

    # Fetch course details from the database based on the provided course_id
    course_info_query = """
        SELECT id, course_name, course_description, course_duration, prerequisites
        FROM courses
        WHERE id = %s
    """
    cursor.execute(course_info_query, (course_id,))
    course_info = cursor.fetchone()
    conn.close()

    if course_info is None:
        # Course not found, you can handle this case as per your requirement (e.g., redirect to an error page)
        return render_template('course_not_found.html')

    # Pass the course_info and course_id to the 'enroll.html' template
    return render_template('enroll.html', course_info=course_info, course_id=course_id)


def get_total_lessons(course_id):
    # Your code to fetch the total number of lessons from the database or any other source
    # For this example, I'll assume you have a function that fetches the total count
    # of lessons from the database based on the provided course_id.
    # Replace this with the actual implementation.
    return 3  # Replace 10 with the actual total number of lessons


@app.route('/course/<int:course_id>', methods=['GET', 'POST'])
def course_details(course_id):
    conn = get_db()
    cursor = conn.cursor()

    # Fetch course details from the database based on the provided course_id
    course_details_query = """
        SELECT course_name, course_image_url, course_description, course_duration, prerequisites,
               lesson_1_title, lesson_1_content, lesson_1_duration, lesson_1_instructor,
               lesson_2_title, lesson_2_content, lesson_2_duration, lesson_2_instructor,
               lesson_3_title, lesson_3_content, lesson_3_duration, lesson_3_instructor
        FROM courses
        WHERE id = %s
    """
    cursor.execute(course_details_query, (course_id,))
    course_details = cursor.fetchone()
    conn.close()

    if course_details is None:
        # Course not found, you can handle this case as per your requirement (e.g., redirect to an error page)
        return render_template('course_not_found.html')

    # Print the course_details for debugging
    print(course_details)

    # Pass the course details to the 'course_details.html' template
    return render_template('course_details.html', course_details=course_details, course_id=course_id)


@app.route('/lesson/<int:course_id>/lesson_<int:lesson_number>')
def individual_lesson(course_id, lesson_number):
    conn = get_db()
    cursor = conn.cursor()

    # Construct the column names for the specified lesson_number
    lesson_title_col = f"lesson_{lesson_number}_title"
    lesson_content_col = f"lesson_{lesson_number}_content"
    lesson_duration_col = f"lesson_{lesson_number}_duration"
    lesson_instructor_col = f"lesson_{lesson_number}_instructor"

    # Fetch lesson details from the courses table
    lesson_details_query = f"""
        SELECT {lesson_title_col}, {lesson_content_col}, {lesson_duration_col}, {lesson_instructor_col}, course_name
        FROM courses
        WHERE id = %s
    """
    cursor.execute(lesson_details_query, (course_id,))
    lesson_details = cursor.fetchone()

    if lesson_details is None:
        # Handle the case where the lesson is not found
        # You may want to redirect to an error page or display an error message
        pass

    # Extract the column values from the fetched row
    lesson_title, lesson_content, lesson_duration, lesson_instructor, course_name = lesson_details

    # Create a dictionary for lesson details
    lesson_details_dict = {
        'title': lesson_title,
        'content': lesson_content,
        'duration': lesson_duration,
        'instructor': lesson_instructor,
        'course_name': course_name
    }

    # Fetch associated resources for the lesson
    resources_query = """
        SELECT resource_name, resource_url
        FROM course_resources
        WHERE course_id = %s
    """
    cursor.execute(resources_query, (course_id,))
    resources = cursor.fetchall()

    return render_template('individual_lesson.html', lesson_details=lesson_details_dict, resources=resources)



if __name__ == "__main__":
    with app.app_context():
        create_tables()
    app.run(debug=True)
