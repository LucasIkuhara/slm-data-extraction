from ollama import embed
from pgvector.psycopg2 import register_vector
from sqlalchemy import create_engine
from os import environ
from embed_exporter import EmbedExporter
import numpy as np
from txt_reader import get_files


conn_str = environ.get("DB_CONN_STRING")
if conn_str is None:
	raise Exception("Missing database connection string. Please add the DB_CONN_STRING environment variable and try again.")

engine = create_engine(conn_str)
with engine.connect() as conn:

    # Register pg vector types
    register_vector(conn, True)

    exporter = EmbedExporter(conn)
    files = get_files()

    for file_name, page, raw_txt in files:
        emb = embed(
            model="llama3",
            input=[raw_txt],
        )
        print(f"Saving embedding for {file_name} page {page}")
        embedding_vec = np.array(emb.embeddings[0])
        exporter.save_embedding(file_name, page, embedding_vec)

    print("Done exporting data.")
