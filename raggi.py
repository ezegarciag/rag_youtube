import os
import shutil
from langchain.llms import Ollama
from langchain.vectorstores import Chroma
from langchain.embeddings import OllamaEmbeddings
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from ollama import chat
from langchain.docstore.document import Document

import warnings




# Desactivar DeprecationWarnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

USER_COLOR = "\033[94m"  # Azul para el usuario

# Función para borrar la base de datos de Chroma
def borrar_chroma_db():
    chroma_db_dir = "./chroma_db"
    if os.path.exists(chroma_db_dir):
        shutil.rmtree(chroma_db_dir)  # Eliminar la carpeta y su contenido

def rag_chat(texto):
    import os
    os.system('cls')
    print("Cargando chat...")
    # Borrar la base de datos de Chroma antes de procesar nuevos datos
    borrar_chroma_db()

    # Crear un objeto Document a partir del texto
    doc = Document(page_content=texto)
    
    # Dividir el texto en chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,  # Tamaño del fragmento (en caracteres)
        chunk_overlap=200  # Solapamiento para mantener contexto
    )
    chunks = text_splitter.split_documents([doc])

    # Inicializar embeddings con Ollama (ej. modelo "nomic-embed-text")
    embeddings = OllamaEmbeddings(model="all-minilm:latest")

    # Almacenar embeddings en una base de datos vectorial (Chroma)
    vector_db = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory="./chroma_db"
    )
    vector_db.persist()

    
    os.system('cls')

    while True:

        # Consulta que se desea realizar
        query = input(" \nUsuario: ")

        # Obtener los 4 trozos más relevantes por similitud coseno
        results = vector_db.similarity_search(query, k=4)

        # Concatenar los 4 fragmentos más relevantes
        context = "\n".join([result.page_content for result in results])

        # Crear el histórico de mensajes
        messages = [
            {'role': 'system', 'content': 'vas a contestar preguntas sobre un video.'},  # Contexto general (opcional)
            {'role': 'user', 'content': context},  # Contexto obtenido de los fragmentos relevantes
            {'role': 'user', 'content': query}  # La consulta del usuario
        ]

        # Llamada de chat con streaming
        stream = chat(
            model='llama3.1:latest',
            messages=messages,
            stream=True,
        )

        for chunk in stream:
            print(f"{USER_COLOR}{chunk['message']['content']}", end='', flush=True)
