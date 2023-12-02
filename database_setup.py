import sqlite3

# Create a connection to the database
conn = sqlite3.connect('users.db')

# Create a cursor object to execute SQL commands
cursor = conn.cursor()

# Create a table for users if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE,  -- Updated column name to 'email'
        password TEXT
    )
''')

# Sample user data
users = [
    ('john@example.com', 'password123'),  # Updated sample data
    ('emma@example.com', 'pass456')  # Updated sample data
]
# Insert sample users into the table
cursor.executemany('INSERT OR IGNORE INTO users (email, password) VALUES (?, ?)', users)

# Commit changes and close the connection
conn.commit()
conn.close()
