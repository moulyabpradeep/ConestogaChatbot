import os
import sqlite3
from UserManager import UserManager

def test_database_creation():
    # Initialize UserManager, which should create the database if it doesn't exist
    manager = UserManager()

    # Check if the database file has been created
    assert os.path.isfile("users.db") == True

def test_database_not_empty():
    # Connect to the database
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    # Check if the 'users' table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
    table_exists = cursor.fetchone() is not None

    # Check if the 'users' table is not empty
    if table_exists:
        cursor.execute("SELECT COUNT(*) FROM users")
        count = cursor.fetchone()[0]

        # Assert that the count of rows in 'users' table is greater than 0
        assert count > 0

    conn.close()