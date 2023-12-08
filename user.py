# user.py
class User:
    def __init__(self, username, password, email, role):  # Added password
        self.username = username
        self.password = password  # Added self.password
        self.email = email
        self.role = role