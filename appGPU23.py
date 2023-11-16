from langchain import PromptTemplate, LLMChain
from langchain.llms import CTransformers
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.embeddings import HuggingFaceBgeEmbeddings
from langchain.document_loaders import PyPDFLoader
import gradio as gr
from getpass import getpass
import os
from UserManager import UserManager
# Asegúrate de que la clase UserManager esté definida en otro lugar del código

# Initialize the LLM
local_llm = "zephyr-7b-beta.Q5_K_S.gguf"

config = {
    'max_new_tokens': 2048,
    'repetition_penalty': 1.1,
    'temperature': 0.1,
    'top_k': 50,
    'top_p': 0.9,
    'stream': True,
    'threads': int(os.cpu_count() / 2),
    'gpu_layers': 1000
}

llm = CTransformers(
    model=local_llm,
    model_type="mistral",
    lib="avx2",  # for CPU use, consider changing if a GPU library is available
    **config
)

print("LLM Initialized...")

prompt_template = """Your prompt template here"""

model_name = "BAAI/bge-large-en"
model_kwargs = {'device': 'cuda'}
encode_kwargs = {'normalize_embeddings': False}
embeddings = HuggingFaceBgeEmbeddings(
    model_name=model_name,
    model_kwargs=model_kwargs,
    encode_kwargs=encode_kwargs
)

prompt = PromptTemplate(template=prompt_template, input_variables=['context', 'question'])
load_vector_store = Chroma(persist_directory="stores/pet_cosine", embedding_function=embeddings)
retriever = load_vector_store.as_retriever(search_kwargs={"k":1})

def get_response(input):
    query = input
    chain_type_kwargs = {"prompt": prompt}
    qa = RetrievalQA.from_chain_type(
        llm=llm, 
        chain_type="stuff", 
        retriever=retriever, 
        return_source_documents=True, 
        chain_type_kwargs=chain_type_kwargs, 
        verbose=True
    )
    response = qa(query)
    return response

sample_prompts = [
    "what is the fastest speed for a greyhound dog?",
    "Why should we not feed chocolates to the dogs?",
    "Name two factors which might contribute to why some dogs might get scared?"
]

input = gr.Text(
    label="Prompt",
    show_label=False,
    max_lines=1,
    placeholder="Enter your prompt",
    container=False,
)

# User Manager for authentication (Asegúrate de que esta clase esté definida e importada)
user_manager = UserManager()

# User authentication
username = input("Username: ")
password = getpass("Password: ")

if user_manager.verify_user(username, password):
    iface = gr.Interface(
        fn=get_response, 
        inputs=input, 
        outputs="text",
        title="CONESTOGA BOT",
        description="This is a RAG implementation based on Zephyr 7B Beta LLM. for CONESTOGA",
        examples=sample_prompts,
        allow_flagging=False
    )
    iface.launch()
else:
    print("Invalid credentials. Access denied.")

# Close the database connection
user_manager.close()
