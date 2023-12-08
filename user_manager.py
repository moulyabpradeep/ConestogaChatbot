# user_manager.py
import sqlite3
import re

def is_valid_email(email):
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(pattern, email) is not None

class UserManager:
    def __init__(self):
        self.conn = sqlite3.connect("users.db")
        self.cursor = self.conn.cursor()

        # Check if the 'users' table exists
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
        if self.cursor.fetchone() is None:
            # If the 'users' table does not exist, create it
            self.cursor.execute("""
                CREATE TABLE users (
                    id INTEGER PRIMARY KEY,
                    username TEXT NOT NULL,
                    password TEXT NOT NULL,
                    email TEXT NOT NULL,
                    role TEXT
                )
            """)
            self.conn.commit()

    def validate_login(self, username, password):
        self.cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = self.cursor.fetchone()
        return user

    def is_email_registered(self, email):
        self.cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        user = self.cursor.fetchone()
        return user is not None

    def is_username_registered(self, username):
        self.cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = self.cursor.fetchone()
        return user is not None

    def add_user(self, username, password, email, role):  # Corrected from name to password
        if self.is_email_registered(email) or self.is_username_registered(username):
            return False
        self.cursor.execute("INSERT INTO users (username, password, email, role) VALUES (?, ?, ?, ?)", (username, password, email, role))  # Corrected from name to password
        self.conn.commit()
        return True

    def get_user(self, username):
        self.cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = self.cursor.fetchone()
        return user