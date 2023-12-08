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

        # Verifica si la tabla 'users' existe
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
        if self.cursor.fetchone() is None:
            # Si la tabla 'users' no existe, créala
            self.cursor.execute("""
                CREATE TABLE users (
                    id INTEGER PRIMARY KEY,
                    username TEXT NOT NULL,
                    password TEXT NOT NULL,
                    email TEXT NOT NULL
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

    def add_user(self, username, password, email):  # Removed role parameter
        if self.is_email_registered(email) or self.is_username_registered(username):
            return False
        self.cursor.execute("INSERT INTO users (username, password, email) VALUES (?, ?, ?)", (username, password, email))  # Removed role from SQL query
        self.conn.commit()
        return True