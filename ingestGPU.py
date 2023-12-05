import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceBgeEmbeddings
from langchain.document_loaders import PyPDFLoader

def create_vector_store(filenames):
    """
    This function creates a vector store from multiple PDF documents using the Chroma algorithm.

    """
    # Define the model and its parameters
    model_name = "BAAI/bge-large-en"
    model_kwargs = {'device': 'cuda'}  # Use GPU
    encode_kwargs = {'normalize_embeddings': False}
    embeddings = HuggingFaceBgeEmbeddings(
        model_name=model_name,
        model_kwargs=model_kwargs,
        encode_kwargs=encode_kwargs
    )

    # Load the PDF documents
    documents = []
    for filename in filenames:
        loader = PyPDFLoader(filename)
        documents.extend(loader.load())  # Use extend to add all documents to the list

    # Split the document into smaller chunks of text
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    texts = text_splitter.split_documents(documents)

    # Create the vector store using the Chroma algorithm
    vector_store = Chroma.from_documents(texts, embeddings, collection_metadata={"hnsw:space": "cosine"}, persist_directory="stores/pet_cosine")

    
    print("Vector Store Created.......")

# Call the function with a list of filenames
#create_vector_store(["PH.pdf", "CO.pdf", "IP.pdf"])
create_vector_store(["perros.pdf"])