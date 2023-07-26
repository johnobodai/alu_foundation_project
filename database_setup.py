import mysql.connector
from passlib.hash import sha256_crypt

# Database configuration
db_config = {
    'host': 'localhost',
    'user': 'j0hn',
    'password': 'w14gs005.asdfghjkl',
    'database': 'digigirls_db',
}

# Function to create the necesaary tables
def create_tables(cursor):
    create_users_table = '''
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(255) NOT NULL UNIQUE,
            password VARCHAR(255) NOT NULL
            )
    '''

    # Ad more table creation queries here if needed

    cursor.execute(create_users_table)

# Function to add a new use with a hashed password
def add_user(cursor, username, password):
    # Hash the password using sha256_crypt
    hashed_password = sha256_crypt.hash(password)
    query = 'INSERT INTO users (username, password) VALUES (%s, %s)'
    cursor.execute(query, (username, hashed_password))


def authenticate_user(cursor, username, password):
    query = 'SELECT password from users WHERE username = %s'
    cursor.execute(query, (username,))
    row = cursor.fetchone()

    if row:
        hashed_password = row[0]
        return sha256_crypt.verify(password, hashed_password)

    return False


# Main function to set up the database
def main():
    try:
        # Connect to the database
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Create the nesessary tables
        create_tables(cursor)

        # Add a new user with a hashed password
        username = input("Enter the new username: ")
        password = input("Enter the new password: ")
        add_user(cursor, username, password)

        # Commit changes and close the connection
        conn.commit()
        cursor.close()
        conn.close()

        print('Database setup completed successfully.')

    except mysql.connector.Error as err:
        print(f'Error: {err}')

if __name__ == '__main__':
    main()
