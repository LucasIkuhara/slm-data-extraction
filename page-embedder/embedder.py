from ollama import embed
from pgvector.psycopg2 import register_vector
from sqlalchemy import create_engine
from os import environ
from embed_exporter import EmbedExporter
import numpy as np


conn_str = environ.get("DB_CONN_STRING")
if conn_str is None:
	raise Exception("Missing database connection string. Please add the DB_CONN_STRING environment variable and try again.")

engine = create_engine(conn_str, echo=True)

with engine.connect() as conn:
    register_vector(conn, True)
    exporter = EmbedExporter(conn)


    emb = embed(
        model="llama3",
        input=[
            "different test embed",
        ],
    )
    embedding = np.array(emb.embeddings[0])
