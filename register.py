import flet as ft
import re
from UserManager import UserManager

def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def register_user(e, page):
    user_manager = UserManager()

    username = username_entry.value
    password = password_entry.value
    name = name_entry.value
    email = email_entry.value

    if not username or not password or not name or not email:
        error_text.value = "All fields are required."
        page.update()
        return
    if not is_valid_email(email):
        error_text.value = "Invalid email address."
        page.update()
        return

    if user_manager.add_user(username, password, name, email):
        success_text.value = "User created successfully"
        # Clear the text fields
        username_entry.value = ""
        password_entry.value = ""
        name_entry.value = ""
        email_entry.value = ""
    else:
        error_text.value = "Username already exists"

    page.update()

def main(page: ft.Page):
    page.title = "User Registration"

    global username_entry, password_entry, name_entry, email_entry, error_text, success_text

    name_entry = ft.TextField(label="Name", autofocus=True)
    email_entry = ft.TextField(label="Email")
    username_entry = ft.TextField(label="Username")
    password_entry = ft.TextField(label="Password", password=True)

    error_text = ft.Text(value="", color="red")
    success_text = ft.Text(value="", color="green")

    register_button = ft.ElevatedButton("Register", on_click=lambda e: register_user(e, page))

    page.add(name_entry, email_entry, username_entry, password_entry, register_button, error_text, success_text)

ft.app(target=main)
