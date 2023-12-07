# pdf_processing_view.py
import threading
import flet as ft
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceBgeEmbeddings
from langchain.document_loaders import PyPDFLoader

class PDFProcessingView(ft.UserControl):
    def __init__(self, process_pdf_file, user_email, main_app_view, page):
        super().__init__()
        self.process_pdf_file = process_pdf_file
        self.user_email = user_email
        self.main_app_view = main_app_view
        self.page = page

    def build(self):
        self.status_text = ft.Text()
        self.project_name_input = ft.TextField(label="Enter project name")
        self.pick_files_dialog = ft.FilePicker(on_result=self.pick_files_result)
        select_button = ft.ElevatedButton("Select PDF File", on_click=lambda _: self.pick_files_dialog.pick_files(allowed_extensions=["pdf"]))
        process_button = ft.ElevatedButton("Process", on_click=self.on_process_clicked)
        back_button = ft.ElevatedButton("Back", on_click=self.on_back_clicked)  # New back button
        self.selected_file_text = ft.Text()  # New control to display the selected file
        return ft.Column([self.project_name_input, select_button, self.selected_file_text, process_button, back_button, self.status_text, self.pick_files_dialog], alignment=ft.MainAxisAlignment.CENTER)

    def pick_files_result(self, e: ft.FilePickerResultEvent):
        if e.files:
            self.file_path = e.files[0].path
            self.status_text.value = "File selected. Please click 'Process' to start processing the file."
            self.selected_file_text.value = f"Selected file: {self.file_path}"  # Update the selected file text
            self.selected_file_text.update()
        else:
            self.status_text.value = "File selection cancelled!"
            self.selected_file_text.value = ""  # Clear the selected file text
            self.selected_file_text.update()
        self.update()

    def on_process_clicked(self, _):
        if self.file_path is not None:
            self.status_text.value = "Processing..."
            self.status_text.update()
            threading.Thread(target=self.process_pdf_file, args=(self.file_path, self.project_name_input.value, self.user_email, self.status_text)).start()
        else:
            self.status_text.value = "No file selected!"
            self.status_text.update()

    def on_back_clicked(self, _):
        self.page.controls.clear()
        self.page.controls.append(self.main_app_view)
        self.page.update()