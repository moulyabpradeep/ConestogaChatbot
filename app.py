import os
import flet as ft
from login_view import LoginView
from pdf_processing_view import PDFProcessingView
from register_view import RegisterView
from main_app_view import MainAppView
from pdf_processing_view import PDFProcessingView  # Change 'PdfProcessingView' a 'PDFProcessingView'
from user_manager import UserManager, is_valid_email
from user import User
# Additional imports for PDF processing
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceBgeEmbeddings
from langchain.document_loaders import PyPDFLoader



def change_route(page, route):
    page.route = route

def build_login_view(page):
    login_view = LoginView(
        on_login_clicked=lambda e: login_user(login_view, page),
        on_register_clicked=lambda e: build_register_view(page)
    )
    page.controls.clear()
    page.controls.append(login_view)
    page.update()


def login_user(view, page):
    user_manager = UserManager()
    username = view.username_entry.value
    password = view.password_entry.value

    if not username or not password:
        view.show_error_message("All fields are required.")
        return

    user = user_manager.validate_login(username, password)
    if user:
        # Define a function to handle the click event on the render button
        def on_process_clicked(file_path, project_name, user_email, status_text):
            process_pdf_file(file_path, project_name, user_email, status_text)  # Call the process_pdf_file function

        pdf_processing_view = PDFProcessingView(on_process_clicked, user[3], None, page)  # Create PDFProcessingView first
        main_app_view = MainAppView(user, page, view, pdf_processing_view)  # Pass PDFProcessingView to MainAppView
        pdf_processing_view.main_app_view = main_app_view  # Set main_app_view in PDFProcessingView
        build_main_app_view(page, main_app_view)
    else:
        view.show_error_message("Incorrect username or password.")

def build_register_view(page):
    register_view = RegisterView(
        on_register_clicked=lambda e: register_user(register_view, page),
        on_back_clicked=lambda e: build_login_view(page)
    )
    page.controls.clear()
    page.controls.append(register_view)
    page.update()

def register_user(view, page):
    user_manager = UserManager()
    username = view.username_entry.value
    password = view.password_entry.value
    email = view.email_entry.value

    if not username or not password or not email:
        view.show_error_message("All fields are required.")
        page.update()
        return

    if not is_valid_email(email):
        view.show_error_message("Invalid email address.")
        page.update()
        return

    if user_manager.add_user(username, password, email):
        view.show_success_message_and_clear_fields()
    else:
        view.show_error_message("Email already registered or username already exists")
    
    page.update()

def process_pdf_file(file_path, project_name, user_email, status_text):
    status_text.value = "Saving vector..."
    status_text.update()

    directory = f"stores/{user_email}/{project_name}"
    if not os.path.exists(directory):
        os.makedirs(directory)

    model_name = "BAAI/bge-large-en"
    model_kwargs = {'device': 'cpu'}
    encode_kwargs = {'normalize_embeddings': False}
    embeddings = HuggingFaceBgeEmbeddings(model_name=model_name, model_kwargs=model_kwargs, encode_kwargs=encode_kwargs)

    loader = PyPDFLoader(file_path)
    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    texts = text_splitter.split_documents(documents)

    vector_store = Chroma.from_documents(texts, embeddings, collection_metadata={"hnsw:space": "cosine"}, persist_directory=directory)
    
    status_text.value = "Your database has been successfully created."
    status_text.update()


def build_pdf_processing_view(page, user_email):
    pdf_processing_view = PDFProcessingView(
        on_process_clicked=process_pdf_file,
        user_email=user_email
    )
    page.controls.clear()
    page.controls.append(pdf_processing_view)
    page.update()

    

def build_main_app_view(page, main_app_view):
    page.controls.clear()
    page.controls.append(main_app_view)
    page.update()

def main(page: ft.Page):
    build_login_view(page)

if __name__ == "__main__":
    ft.app(target=main)