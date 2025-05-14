from ollama import chat, ChatResponse
from prompter import PromptBuilder
from rag import Rag
from pgvector.psycopg2 import register_vector
from sqlalchemy import create_engine
from os import environ
from embedding_store import EmbeddingStore
from page_reader import PageReader


conn_str = environ.get("DB_CONN_STRING")
model = environ.get("EMBEDDING_MODEL")
BASE_PATH = environ.get("BASE_PATH")
MODEL = "llama3"

if not all([conn_str, model, BASE_PATH]):
    raise Exception(
        "Missing environment variables. Please set DB_CONN_STRING, EMBEDDING_MODEL, BASE_PATH and try again."
    )

# Create db connection
engine = create_engine(conn_str)
with engine.connect() as conn:
    register_vector(conn, True)

    # Initialize components
    store = EmbeddingStore(conn)
    page_reader = PageReader(BASE_PATH)
    rag = Rag(store, page_reader, MODEL)
    prompter = PromptBuilder("pdi-fpso-p-32", rag, True)

    # Prompt model
    msg = prompter.make_prompt("A distância da costa medida em kilometros")
    response: ChatResponse = chat(
        model=MODEL,
        messages=[
            {
                "role": "user",
                "content": msg,
            }
        ],
        options={"num_ctx": 4096 * 2},
    )
    print("SLM Response:\n\n", response.message.content)
    print("SLM tokens used:\n\n", response.prompt_eval_count)
