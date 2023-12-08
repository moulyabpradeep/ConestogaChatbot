import sqlite3
from hashlib import sha256

import sqlite3
from hashlib import sha256

class UserManager:
    """
    A class that manages user registration and login functionality.

    Attributes:
        conn (sqlite3.Connection): The connection to the SQLite database.
    """

    def __init__(self):
        """
        Initializes a new instance of the UserManager class.

        Creates a connection to the 'users.db' database if it doesn't exist.
        Creates the 'users' table if it doesn't exist, with columns for username, password, name, and email.
        """
        self.conn = sqlite3.connect('users.db')
        self.conn.execute('CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT, name TEXT, email TEXT)')

    def add_user(self, username, password, name, email):
        """
        Adds a new user to the database.

        Args:
            username (str): The username of the user.
            password (str): The password of the user.
            name (str): The name of the user.
            email (str): The email address of the user.

        Returns:
            bool: True if the user was successfully added, False if the username already exists.
        """
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        if cursor.fetchone():
            return False
        password_hash = sha256(password.encode('utf-8')).hexdigest()
        self.conn.execute('INSERT INTO users VALUES (?, ?, ?, ?)', (username, password_hash, name, email))
        self.conn.commit()
        return True

    def validate_login(self, username, password):
        """
        Validates a user's login credentials here.

        Args:
            username (str): The username of the user.
            password (str): The password of the user.

        Returns:
            bool: True if the login credentials are valid, False otherwise.
        """
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()
        if user:
            password_hash = sha256(password.encode('utf-8')).hexdigest()
            if password_hash == user[1]:
                return True
        return False