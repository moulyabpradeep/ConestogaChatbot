# register_view.py
import flet as ft

class RegisterView(ft.UserControl):
    def __init__(self, on_register_clicked, on_back_clicked):
        super().__init__()
        self.on_register_clicked = on_register_clicked
        self.on_back_clicked = on_back_clicked

    def build(self):
        self.name_entry = ft.TextField(label="Name")
        self.email_entry = ft.TextField(label="Email")
        self.username_entry = ft.TextField(label="Username")
        self.password_entry = ft.TextField(label="Password", password=True)
        self.error_text = ft.Text(value="", color="red")
        self.success_text = ft.Text(value="", color="green")
        register_button = ft.ElevatedButton("Register", on_click=self.on_register_clicked)
        back_button = ft.ElevatedButton("Back to login", on_click=self.on_back_clicked)
        return ft.Column(
            controls=[
                self.name_entry,
                self.email_entry,
                self.username_entry,
                self.password_entry,
                register_button,
                back_button,
                self.success_text,
                self.error_text
            ],
            width=600,
        )

    def show_success_message_and_clear_fields(self):
        self.success_text.value = "User created successfully!"
        self.name_entry.value = ""
        self.email_entry.value = ""
        self.username_entry.value = ""
        self.password_entry.value = ""
        self.update()  # Actualizar el UserControl

    def show_error_message(self, message):
        self.error_text.value = message
        self.update()  # Actualizar el UserControl

