from ollama import embed
from pgvector.psycopg2 import register_vector
from sqlalchemy import create_engine
from os import environ

conn_str = environ.get("DB_CONN_STRING")

if conn_str is None:
	raise Exception("Missing database connection string. Please add the DB_CONN_STRING environment variable and try again.")
    
engine = create_engine(conn_str, echo=True)
conn = engine.connect()

register_vector(conn, True)


emb = embed(
    model="llama3",
    input=[
        "test embed",
    ],
)
embedding = emb.embeddings[0]
conn.execute('INSERT INTO EMBEDDINGS (source_file, page_num, embedding) VALUES (%s, %s, %s)', ("a_true.pdf", 45, embedding))

