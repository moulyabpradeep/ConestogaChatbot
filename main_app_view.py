# main_app_view.py
import flet as ft
import os
from llm_view import LLMView

class MainAppView(ft.UserControl):
    def __init__(self, user, page, login_view, pdf_processing_view):
        super().__init__()
        self.user = user
        self.page = page
        self.login_view = login_view
        self.pdf_processing_view = pdf_processing_view
        self.selected_chatbot = None

    def build(self):
        email = self.user[2]
        welcome_text = ft.Text(f"Welcome back, {email}", size=24)
        logout_button = ft.ElevatedButton("Logout", on_click=self.logout)
        ingest_pdf_button = ft.ElevatedButton("Ingest PDF", on_click=self.ingest_pdf)
        llm_button = ft.ElevatedButton("Use Language Model", on_click=self.open_llm_view)

        user_chatbots = self.get_user_chatbots()
        dropdown_label = ft.Text("Choose your chatbot")
        self.user_chatbots_dropdown = ft.Dropdown(
            options=[ft.dropdown.Option(chatbot) for chatbot in user_chatbots],
            on_change=self.on_chatbot_selected
        )

        return ft.Column(controls=[
            welcome_text, logout_button, ingest_pdf_button, dropdown_label,
            self.user_chatbots_dropdown, llm_button
        ], width=600)

    def logout(self, event):
        self.page.controls.clear()
        self.page.controls.append(self.login_view)
        self.page.update()

    def ingest_pdf(self, event):
        self.page.controls.clear()
        self.page.controls.append(self.pdf_processing_view)
        self.page.update()

    def open_llm_view(self, event):
        if self.selected_chatbot:
            directory = f"stores/{self.user[2]}/{self.selected_chatbot}"
            llm_view = LLMView(self.user, self.page, self, directory)
            self.page.controls.clear()
            self.page.controls.append(llm_view)
            self.page.update()
        else:
            # Mensaje de error si no se selecciona un chatbot
            self.page.show_snackbar(ft.Snackbar("Please select a chatbot before proceeding.", open=True))

    def on_chatbot_selected(self, event):
        self.selected_chatbot = event.control.value
        directory = f"stores/{self.user[2]}/{self.selected_chatbot}"
        print(f"Selected chatbot: {self.selected_chatbot}, Directory: {directory}")

    def get_user_chatbots(self):
        user_email = self.user[2]
        user_dir = os.path.join("stores", user_email)
        if os.path.exists(user_dir):
            user_chatbots = os.listdir(user_dir)
            user_chatbots.sort(reverse=True)
        else:
            user_chatbots = []
        return user_chatbots
