import os
from unittest.mock import MagicMock, patch
import pytest

from app import process_pdf_file  

@pytest.fixture
def mock_status_text():
    return MagicMock()

def test_process_pdf_file(mock_status_text):
    # Mocking necessary objects
    file_path = "test_file.pdf"
    project_name = "TestProject"
    user_email = "test@example.com"

    with patch('app.os.makedirs') as mock_makedirs, \
         patch('app.HuggingFaceBgeEmbeddings') as mock_embeddings, \
         patch('app.PyPDFLoader') as mock_loader, \
         patch('app.RecursiveCharacterTextSplitter') as mock_text_splitter, \
         patch('app.Chroma.from_documents') as mock_chroma:

        # Calling the function
        process_pdf_file(file_path, project_name, user_email, mock_status_text)

        # Assertions
        mock_status_text.update.assert_called_with()
        mock_makedirs.assert_called_once_with(f"stores/{user_email}/{project_name}")

        # Check that relevant objects and methods were called with the expected arguments
        mock_embeddings.assert_called_once_with(model_name="BAAI/bge-large-en", model_kwargs={'device': 'cpu'}, encode_kwargs={'normalize_embeddings': False})
        mock_loader.assert_called_once_with(file_path)
        mock_text_splitter.assert_called_once_with(chunk_size=1000, chunk_overlap=100)
        mock_chroma.assert_called_once_with(
            mock_text_splitter.return_value.split_documents.return_value,
            mock_embeddings.return_value,
            collection_metadata={"hnsw:space": "cosine"},
            persist_directory=f"stores/{user_email}/{project_name}"
        )

    # Additional assertions based on the specific behavior of your function
    assert mock_status_text.value == "Your database has been successfully created."
    mock_status_text.update.assert_called_with()
