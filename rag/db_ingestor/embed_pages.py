from pgvector.psycopg2 import register_vector
from sqlalchemy import create_engine, exc
from os import environ
from embedding_store import EmbeddingStore
from embed_fn import embed_str
from page_reader import PageReader


conn_str = environ.get("DB_CONN_STRING")
model = environ.get("EMBEDDING_MODEL")
BASE_PATH = environ.get("BASE_PATH")

if not all([conn_str, model, BASE_PATH]):
    raise Exception(
        "Missing environment variables. Please set DB_CONN_STRING, EMBEDDING_MODEL, BASE_PATH and try again."
    )


engine = create_engine(conn_str)
text_reader = PageReader(BASE_PATH)

with engine.connect() as conn:

    # Register pg vector types
    register_vector(conn, True)

    exporter = EmbeddingStore(conn)
    files = text_reader.get_files()

    for file_name, page, raw_txt in files:

        print(f"Embedding page {page} from {file_name}")
        embedding_vec = embed_str(raw_txt, model)

        try:
            exporter.save_embedding(file_name, page, embedding_vec, model)
        except exc.IntegrityError:
            print(
                f"Page embedding for {file_name} page {page} already exists. Skipping..."
            )
            conn.rollback()
            continue

    print("Done exporting data.")
