import sqlite3
from hashlib import sha256

class UserManager:
    def __init__(self):
        self.conn = sqlite3.connect('users.db')
        self.conn.execute('CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT, name TEXT, email TEXT)')

    def add_user(self, username, password, name, email):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        if cursor.fetchone():
            return False
        password_hash = sha256(password.encode('utf-8')).hexdigest()
        self.conn.execute('INSERT INTO users VALUES (?, ?, ?, ?)', (username, password_hash, name, email))
        self.conn.commit()
        return True

    def validate_login(self, username, password):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()
        if user:
            password_hash = sha256(password.encode('utf-8')).hexdigest()
            if password_hash == user[1]:
                return True
        return False