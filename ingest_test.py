from unittest.mock import MagicMock, patch
from ingest import process_pdf_file  # 

def test_process_pdf_file():
    # Mocking necessary objects
    file_path = "pet.pdf"
    status_text_mock = MagicMock()
    project_name_mock = MagicMock()
    user_email_mock = MagicMock()

    with patch('ingest.HuggingFaceBgeEmbeddings'), \
         patch('ingest.PyPDFLoader'), \
         patch('ingest.RecursiveCharacterTextSplitter'), \
         patch('ingest.Chroma.from_documents') as mock_chroma,\
         patch('ingest.os.makedirs') as mock_makedirs:

        # Mocking makedirs to avoid OSError
        mock_makedirs.side_effect = lambda directory, exist_ok=False: None

        # Calling the function
        process_pdf_file(file_path, status_text_mock)

        # Additional assertions based on the specific behavior of your function
        assert status_text_mock.value == "Vector Store Created and Saved!"
        status_text_mock.update.assert_called_once()

        # Check if Chroma.from_documents is called with the correct arguments
        mock_chroma.assert_called_once()