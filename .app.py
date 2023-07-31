from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello, this is the home page!'

# Configure MySQL database connection
db_config = {
    'host': 'localhost',
    'user': 'j0hn',
    'password': 'w14gs005.asdfghjkl',
    'database': 'digigirls_db',
}


# Function to create a MySQL connection
def create_db_connection():
    return mysql.connector.connect(**db_config)


# Register route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = sha256_crypt.hash(request.form['password'])

        # Create a MySQL connection
        connection = create_db_connection()
        cursor = connection.cursor()

        # Insert user data into the users table
        query = 'INSERT INTO users (username, password) VALUES (%s, %s)'
        cursor.execute(query, (username, password))

        # Commit changes and close the connection
        connection.commit()
        cursor.close()
        connection.close()

        return redirect('/login')

    return render_template('register.html')

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Create a MySQL connection
        connection = create_db_connection()
        cursor = connection.cursor()

        # Retrieve user data from the users table
        query = 'SELECT password FROM users WHERE username = %s'
        cursor.execute(query, (username,))
        result = cursor.fetchone()

        # Check if the password matches
        if result and sha256_crypt.verify(password, result[0]):
            return 'Login successful'
        else:
            return 'Invalid credentials'

    return render_template('login.html')
