import os
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_core.vectorstores import InMemoryVectorStore
from langchain.docstore.document import Document

from page_reader import PageReader


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
embeddings = OllamaEmbeddings(model="llama3")
llm = ChatOllama(model="llama3")

# conn_str = os.getenv("DB_CONN_STRING")
# model_list = os.getenv("EMBEDDING_MODELS").split(";")
BASE_PATH = os.getenv("PAGES_PATH")

# if not all([conn_str, model_list, BASE_PATH]):
#     raise Exception(
#         "Missing environment variables. Please set DB_CONN_STRING, EMBEDDING_MODELS, BASE_PATH and try again."
#     )


text_reader = PageReader(BASE_PATH)
files = text_reader.get_files()
docs = [
    Document(f.raw_text, metadata={"source": f.source_document, "page": f.page})
    for f in files
]

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
chunks = text_splitter.split_documents(docs)

vector_store = InMemoryVectorStore(embeddings)
vector_store.add_documents(chunks)
vector_store.dump("vec_store.db")
print("Successfully loaded Db: vec_store.db")
