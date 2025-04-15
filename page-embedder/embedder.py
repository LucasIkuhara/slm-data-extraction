from ollama import embed
from pgvector.psycopg2 import register_vector
from sqlalchemy import create_engine, text
from os import environ
import numpy as np


conn_str = environ.get("DB_CONN_STRING")

if conn_str is None:
	raise Exception("Missing database connection string. Please add the DB_CONN_STRING environment variable and try again.")
    
engine = create_engine(conn_str, echo=True)

with engine.connect() as conn:
    register_vector(conn, True)

    emb = embed(
        model="llama3",
        input=[
            "different test embed",
        ],
    )
    embedding = np.array(emb.embeddings[0])
    print(embedding)

    res = conn.execute(
        text("INSERT INTO EMBEDDING (source_file, page_num, embedding) VALUES (:some_file, :page_num, :emb)"),
        [{'some_file': "some.pdf", "page_num": 11, "emb": embedding}]
    )
    conn.commit()
    # res = conn.execute(
    # 	text('SELECT * FROM EMBEDDING ORDER BY embedding <-> :v LIMIT 5'),
    #     # "INSERT INTO EMBEDDINGS (source_file, page_num, embedding) VALUES ('some.pdf', 10, %s)",
    # 	  [(embedding,)]
    # )
    print(res)

