# llm_view.py
import os
import flet as ft
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain.llms import CTransformers
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceBgeEmbeddings
from transformers import GPT2Tokenizer


class LLMView(ft.UserControl):
    def __init__(self, user, page, main_app_view, directory):
        super().__init__()
        self.user = user
        self.page = page
        self.main_app_view = main_app_view
        self.directory = directory
        self.setup_language_model()

    def setup_language_model(self):
        self.local_llm = "zephyr-7b-beta.Q5_K_S.gguf"
        self.config = {
            'max_new_tokens': 2048,
            'repetition_penalty': 1.1,
            'temperature': 0.1,
            'top_k': 50,
            'top_p': 0.9,
            'stream': True,
            'threads': int(os.cpu_count() / 2),
            'gpu_layers': 1000
        }
        self.llm = CTransformers(
            model=self.local_llm,
            model_type="mistral",
            lib="avx2",
            **self.config
        )
        self.prompt_template = """
        Use the following pieces of information to answer the user's question.
        If you don't know the answer, just say that you don't know, don't try to make up an answer.

        Context: {context}
        Question: {question}

        Only return the helpful answer below and nothing else.
        Helpful answer:
        """
        self.embeddings = HuggingFaceBgeEmbeddings(
            model_name="BAAI/bge-large-en",
            model_kwargs={'device': 'cuda'},
            encode_kwargs={'normalize_embeddings': False}
        )
        self.prompt = PromptTemplate(template=self.prompt_template, input_variables=['context', 'question'])
        self.load_vector_store = Chroma(persist_directory=self.directory, embedding_function=self.embeddings)
        self.retriever = self.load_vector_store.as_retriever(search_kwargs={"k": 1})

    def build(self):
        self.input_prompt = ft.TextField(label="Prompt", max_lines=1)
        self.output_display = ft.Text()
        self.submit_button = ft.ElevatedButton(text="Submit", on_click=lambda e: self.submit_query())
        self.response_label = ft.Text()  # Nuevo control de texto para mostrar el mensaje
        #self.back_button = ft.ElevatedButton("Back", on_click=self.on_back_clicked)  # Nuevo botón de volver atrás
        #return ft.Column(controls=[self.input_prompt, self.submit_button, self.response_label, self.output_display, self.back_button])
        return ft.Column(controls=[self.input_prompt, self.submit_button, self.response_label, self.output_display])

    def get_response(self, input):
        tokenizer = GPT2Tokenizer.from_pretrained('gpt2')

        # Tokenize the input
        tokens = tokenizer.tokenize(input)

        # Divide the tokens into chunks of 512 tokens
        chunks = [tokens[i:i + 512] for i in range(0, len(tokens), 512)]
        
        responses = []
        for chunk in chunks:
            # Convert the chunk back into text
            query = tokenizer.convert_tokens_to_string(chunk)
            chain_type_kwargs = {"prompt": self.prompt}
            qa = RetrievalQA.from_chain_type(
                llm=self.llm,
                chain_type="stuff",
                retriever=self.retriever,
                return_source_documents=True,
                chain_type_kwargs=chain_type_kwargs,
                verbose=True
            )
            response = qa(query)
            print(response)  # Imprimir el diccionario response completo
            # Extraer y retornar solo la parte del resultado de la respuesta
            responses.append(response.get("result", "No response found."))
        
        # Join the responses together
        return " ".join(responses)

    def submit_query(self):
        response = self.get_response(self.input_prompt.value)
        self.output_display.value = response
        self.page.controls.append(self.output_display)  # Asegúrate de que output_display está en la página
        self.page.update()
        self.input_prompt.value = ""  # Limpiar el campo de entrada
        self.input_prompt.focus()  # Poner el foco en el campo de entrada


    """def on_back_clicked(self, _):
        try:
            if not self.page:
                print("Error: self.page es None")
                return

            # Primero, limpia todos los controles de la página
            self.page.controls.clear()

            # Añade los controles necesarios de nuevo a la página
            self.page.controls.append(self.main_app_view)
            self.page.controls.append(self.input_prompt)

            # Actualiza la página para reflejar los cambios
            self.page.update()

            # Enfoca el input_prompt
            self.page.after(100, lambda: self.input_prompt.focus())
        except Exception as e:
            print(f"Error en on_back_clicked: {e}")"""





    """def submit_query(self):
        response = self.get_response(self.input_prompt.value)
        self.output_display.value = response
        self.response_label.value = "Esta es tu respuesta:"  # Actualizar el valor del control de texto con el mensaje
        self.page.update()
        print(f"Prompt: {self.input_prompt.value}")
        print(f"Response: {response}")"""
