import os
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_postgres import PGEngine, PGVectorStore
from langchain_core.vectorstores import InMemoryVectorStore
from langchain.docstore.document import Document
from page_reader import PageReader


MODEL_TAG = "llama3.2"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
embedding = OllamaEmbeddings(model=MODEL_TAG)
llm = ChatOllama(model=MODEL_TAG)

# conn_str = os.getenv("DB_CONN_STRING")
# pg_engine = PGEngine.from_connection_string(url=conn_str)

# Read text files
BASE_PATH = os.getenv("PAGES_PATH")
text_reader = PageReader(BASE_PATH)
files = text_reader.get_files()
docs = [
    Document(f.raw_text, metadata={"source": f.source_document, "page": f.page})
    for f in files
]


# normalized_model_name = MODEL_TAG.replace(":", "_")
# table_name = f"lc_emb_{normalized_model_name}"

# pg_engine.init_vectorstore_table(
#     table_name=table_name, vector_size=4096, overwrite_existing=True
# )
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
chunks = text_splitter.split_documents(docs)
# store = PGVectorStore.create_sync(
#     engine=pg_engine,
#     table_name=table_name,
#     embedding_service=embedding,
# )
# store.add_documents(chunks)

vector_store = InMemoryVectorStore.from_documents(chunks, embedding)
vector_store.dump("vec_store.db")
print("Successfully loaded Db: vec_store.db")
