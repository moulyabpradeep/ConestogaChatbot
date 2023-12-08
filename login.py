import flet as ft
import subprocess
import sys
from UserManager import UserManager

def login_user(e, page):
    """
    Logs in a user and performs necessary actions based on the login result.

    Args:
        e: The event object.
        page: The page object.

    Returns:
        None
    """
    user_manager = UserManager()

    username = username_entry.value
    password = password_entry.value

    if not username or not password:
        error_text.value = "All fields are required."
        page.update()
        return

    if user_manager.validate_login(username, password):
        success_text.value = "Login successful"
        # Run the appGPU.py script
        subprocess.run([sys.executable, "appGPU.py"])
        # Clear the text fields
        username_entry.value = ""
        password_entry.value = ""
    else:
        error_text.value = "Invalid username or password."
        register_text.value = "If you don't have an account, please register..!"
        # Run the register.py script
        subprocess.run([sys.executable, "register.py"])

    page.update()

def register_user(e, page):
    # Run the register.py script
    subprocess.run([sys.executable, "register.py"])

def main(page: ft.Page):
    page.title = "User Login"

    global username_entry, password_entry, error_text, success_text, register_text

    username_entry = ft.TextField(label="Username")
    password_entry = ft.TextField(label="Password", password=True)

    error_text = ft.Text(value="", color="red")
    success_text = ft.Text(value="", color="green")
    register_text = ft.Text(value="")

    login_button = ft.ElevatedButton("Login", on_click=lambda e: login_user(e, page))
    register_button = ft.ElevatedButton("Register", on_click=lambda e: register_user(e, page))

    page.add(username_entry, password_entry, login_button, register_button, error_text, success_text, register_text)

ft.app(target=main)