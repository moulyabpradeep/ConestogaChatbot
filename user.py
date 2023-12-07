# user.py
class User:
    def __init__(self, username, password, email, role):  # Agregado password
        self.username = username
        self.password = password  # Agregado self.password
        self.email = email
        self.role = role