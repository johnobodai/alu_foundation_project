from flask import Flask, render_template, request, redirect, url_for
import pymysql

app = Flask(__name__)

# Configuration for MySQL database
DB_HOST = 'localhost'
DB_USER = 'j0hn'
DB_PASSWORD = 'w14gs005.asdfghjkl'
DB_NAME = 'digigirls_db'

# Secret key for session management
app.secret_key = 'your_secret_key'


def create_tables():
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
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        title = request.form['title']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        age = int(request.form['age'])
        gender = request.form['gender']
        country = request.form['country']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        conn = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, db=DB_NAME)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO users (title, first_name, last_name, age, gender, country, email, password)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ''', (title, first_name, last_name, age, gender, country, email, password))
        conn.commit()
        conn.close()

        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, db=DB_NAME)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE email = %s AND password = %s', (email, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            # Set up a session here if you want to manage user authentication
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error='Invalid email or password')

    return render_template('login.html')


@app.route('/dashboard')
def dashboard():
    # Check if the user is authenticated and allowed to access the dashboard
    # You can manage user authentication using Flask's session or a user authentication library
    return render_template('dashboard.html')


if __name__ == '__main__':
    create_tables()
    app.run(debug=True)

