import os
import flet as ft
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceBgeEmbeddings
from langchain.document_loaders import PyPDFLoader

def main(page: ft.Page):
    status_text = ft.Text()

    def pick_files_result(e: ft.FilePickerResultEvent):
        if e.files:
            process_pdf_file(e.files[0].path, status_text)
        else:
            status_text.value = "File selection cancelled!"
            status_text.update()

    pick_files_dialog = ft.FilePicker(on_result=pick_files_result)
    page.overlay.append(pick_files_dialog)

    select_button = ft.ElevatedButton("Select PDF File", on_click=lambda _: pick_files_dialog.pick_files(allowed_extensions=["pdf"]))
    
    # Center the elements in the Column
    page.add(ft.Column([
        select_button,
        status_text
    ], alignment=ft.MainAxisAlignment.CENTER))

def process_pdf_file(file_path, status_text):
    """
    Process a PDF file and create a vector store.

    Args:
        file_path (str): The path to the PDF file.
        status_text: An object representing the status text.

    Returns:
        None
    """
    model_name = "BAAI/bge-large-en"
    model_kwargs = {'device': 'cpu'}
    encode_kwargs = {'normalize_embeddings': False}
    embeddings = HuggingFaceBgeEmbeddings(
        model_name=model_name,
        model_kwargs=model_kwargs,
        encode_kwargs=encode_kwargs
    )

    loader = PyPDFLoader(file_path)
    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    texts = text_splitter.split_documents(documents)

    vector_store = Chroma.from_documents(texts, embeddings, collection_metadata={"hnsw:space": "cosine"}, persist_directory="stores/pet_cosine")
    
    status_text.value = "Vector Store Created and Saved!"
    status_text.update()

ft.app(target=main)