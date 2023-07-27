from flask import Flask, render_template, request, redirect, url_for
import pymysql

app = Flask(__name__, template_folder='templates')

# Configuration for MySQL database
DB_HOST = 'localhost'
DB_USER = 'j0hn'
DB_PASSWORD = 'w14gs005.asdfghjkl'
DB_NAME = 'digigirls_db'

# Secret key for session management
app.secret_key = 'your_secret_key'


def create_tables():
    # Connect to the database and create the 'users' table if it doesn't exist
    conn = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, db=DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(10),
            first_name VARCHAR(100) NOT NULL,
            last_name VARCHAR(100) NOT NULL,
            age INT NOT NULL,
            gender VARCHAR(10) NOT NULL,
            country VARCHAR(100) NOT NULL,
            email VARCHAR(100) NOT NULL UNIQUE,
            password VARCHAR(100) NOT NULL
        )
    ''')
    conn.commit()
    conn.close()


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

        # Insert the new user data into the 'users' table in the database
        conn = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, db=DB_NAME)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO users (title, first_name, last_name, age, gender, country, email, password)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ''', (title, first_name, last_name, age, gender, country, email, password))
        conn.commit()
        conn.close()

        # Redirect to the login page after successful registration
        return redirect(url_for('login'))

    # Render the 'register.html' template for GET requests (displaying the registration form)
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Process the login form data when it's submitted
        email = request.form['email']
        password = request.form['password']

        # Check if the user exists in the database and the provided password is correct
        conn = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, db=DB_NAME)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE email = %s AND password = %s', (email, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            # Set up a session to manage user authentication
            session['user_id'] = user['id']

            # Redirect the user to the dashboard page after successful login
            return redirect(url_for('dashboard'))
        else:
            # Render the 'login.html' template with an error message for invalid login attempts
            return render_template('login.html', error='Invalid email or password')

    # Render the 'login.html' template for GET requests (displaying the login form)
    return render_template('login.html')


@app.route('/dashboard')
def dashboard():
    if 'user_id' in session:
        # User is logged in, render the dashboard template
        return render_template('dashboard.html')
    else:
        # User is not logged in, redirect to the login page
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


@app.route('/course-details')
def course_details():
    # Render the 'course-details.html' template for the Course Details page
    return render_template('course-details.html')


@app.route('/forgot-password')
def forgot_password():
    # Render the 'forgot_password.html' template for the Forgot Password page
    return render_template('forgot_password.html')


if __name__ == '__main__':
    # Create the necessary database tables and run the Flask app in debug mode
    create_tables()
    app.run(debug=True)

