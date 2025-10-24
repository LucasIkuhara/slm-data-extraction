import os
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_postgres import PGEngine, PGVectorStore
from langchain_core.vectorstores import InMemoryVectorStore
from langchain.docstore.document import Document
from page_reader import PageReader
from db_ingestor.config import cfg


# ! Ollama embedding
# MODEL_TAG = "llama3.2"
# embedding = OllamaEmbeddings(model=MODEL_TAG)
# llm = ChatOllama(model=MODEL_TAG)

# ! Open AI Embedding
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
embedding = OpenAIEmbeddings(model="text-embedding-3-large", api_key=OPENAI_API_KEY)

chunks = []

for doc in cfg["documents"]:

    print("Loading: ", doc)
    # Read text files
    BASE_PATH: str = os.getenv("PAGES_PATH")
    text_reader = PageReader(BASE_PATH)
    files = text_reader.get_files([doc])
    print(f"Found {len(files)} files.")

    # Join and chunk text
    txt = "".join([t.raw_text for t in files])
    doc = Document(txt, metadata={"source": doc})
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks += text_splitter.split_documents([doc])

vector_store = InMemoryVectorStore.from_documents(chunks, embedding)
vector_store.dump("vec-stores/oai_3_large_vec_store.db")
print("Successfully loaded Db: vec_store.db")
