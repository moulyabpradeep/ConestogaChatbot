# login_view.py
import flet as ft

class LoginView(ft.UserControl):
    def __init__(self, on_login_clicked, on_register_clicked):
        super().__init__()
        self.on_login_clicked = on_login_clicked
        self.on_register_clicked = on_register_clicked

    def build(self):
        self.username_entry = ft.TextField(label="Username")
        self.password_entry = ft.TextField(label="Password", password=True)
        self.error_text = ft.Text(value="", color="red")
        self.success_text = ft.Text(value="", color="green")  # Nuevo texto de éxito
        login_button = ft.ElevatedButton("Login", on_click=self.on_login_clicked)
        register_button = ft.ElevatedButton("Register", on_click=self.on_register_clicked)
        return ft.Column(controls=[self.username_entry, self.password_entry, login_button, register_button, self.success_text, self.error_text], width=600)

    def show_error_message(self, message):
        self.error_text.value = message
        self.update()  # Actualizar el UserControl

    def show_success_message(self):  # Nuevo método
        self.success_text.value = "Login successful!"
        self.update()  # Actualizar el UserControl