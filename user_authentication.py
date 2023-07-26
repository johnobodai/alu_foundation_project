import mysql.connector
from passlib.hash import sha256_crypt
from database_setup import authenticate_user

# Data configuration (same as in database_setup.py)
db_config = {
    'host': 'localhost',
    'user': 'j0hn',
    'password': 'w14gs005.asdfghjkl',
    'database': 'digigirls_db',
}


def main():
    try:
        # Connect to the database
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Get the username and password from the user
        username = input("Enter your username: ")
        password = input("Enter your password: ")

        # Authenticate the user
        if authenticate_user(cursor, username, password):
            print("Authentication successful. Welcome, {}!".format(username))
        else:
            print("Authentication failed. Invalid username or password.")

        # Close the connection
        cursor.close()
        conn.close
    except mysql.connector.Error as err:
        print(f'Error: {err}')


if __name__ == '__main__':
    main()
