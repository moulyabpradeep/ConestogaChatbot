from langchain import PromptTemplate, LLMChain
from langchain.llms import CTransformers
import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.embeddings import HuggingFaceBgeEmbeddings
from io import BytesIO
from langchain.document_loaders import PyPDFLoader
import gradio as gr

local_llm = "zephyr-7b-beta.Q5_K_S.gguf"


llm = CTransformers(
    model=local_llm,
    model_type="mistral",
    lib="avx2",  # for CPU use, consider changing if a GPU library is available
    max_new_tokens=2048,  # Suggested fit
    context_length=4096,  # Suggested fit
    repetition_penalty=1.1,
    temperature=0.1,
    top_k=50,
    top_p=0.9,
    stream=True,
    threads=int(os.cpu_count() / 2),
    gpu_layers=1000  # Add this line
)


print("LLM Initialized...")

prompt_template = """Use the following pieces of information to answer the user's question.
If you don't know the answer, just say that you don't know, don't try to make up an answer.

Context: {context}
Question: {question}

Only return the helpful answer below and nothing else.
Helpful answer:
"""

model_name = "BAAI/bge-large-en"
model_kwargs = {'device': 'cuda'}  # Switch to 'cuda' for GPU
encode_kwargs = {'normalize_embeddings': False}
embeddings = HuggingFaceBgeEmbeddings(
    model_name=model_name,
    model_kwargs=model_kwargs,
    encode_kwargs=encode_kwargs
)

prompt = PromptTemplate(template=prompt_template, input_variables=['context', 'question'])
load_vector_store = Chroma(persist_directory="stores/conestoga", embedding_function=embeddings)
retriever = load_vector_store.as_retriever(search_kwargs={"k":1})

print("######################################################################")

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

sample_prompts = ["What is the description of the program in big data??", "College Hours?", "current program desing?"]

input = gr.Text(
                label="Prompt",
                show_label=False,
                max_lines=1,
                placeholder="Enter your prompt",
                container=False,
            )

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
