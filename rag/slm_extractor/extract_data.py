from ollama import chat, ChatResponse
from prompter import PromptBuilder
from rag import Rag
from pgvector.psycopg2 import register_vector
from sqlalchemy import create_engine
from os import environ
from embedding_store import EmbeddingStore
from page_reader import PageReader


CONTEXT_DIR = "../pdi-txt"
msg = PromptBuilder(f"{CONTEXT_DIR}/pdi-fpso-p-32.txt").make_prompt()

response: ChatResponse = chat(
    model="llama3",
    messages=[
        {
            "role": "user",
            "content": msg,
        },
    ],
)
print(response.message.content)

conn_str = environ.get("DB_CONN_STRING")
model = environ.get("EMBEDDING_MODEL")
BASE_PATH = environ.get("BASE_PATH")

if not all([conn_str, model, BASE_PATH]):
    raise Exception(
        "Missing environment variables. Please set DB_CONN_STRING, EMBEDDING_MODEL, BASE_PATH and try again."
    )


engine = create_engine(conn_str)
with engine.connect() as conn:

    page_reader = PageReader(BASE_PATH)

    # Register pg vector types
    register_vector(conn, True)
    store = EmbeddingStore(conn)

    rag = Rag(store, page_reader, "llama3")
    ctx = rag.get_context_by_prompt("Animais marinhos", ["pdi-fpso-p-32"])
    print(ctx[0])
