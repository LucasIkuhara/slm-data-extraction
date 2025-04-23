from pgvector.psycopg2 import register_vector
from sqlalchemy import create_engine, exc
from os import environ
from embedding_store import EmbeddingStore
from embed_fn import embed_str
from txt_reader import get_files


conn_str = environ.get("DB_CONN_STRING")
model = environ.get("EMBEDDING_MODEL")
if conn_str is None or conn_str is None:
    raise Exception(
        "Missing environment variables. Please set DB_CONN_STRING and EMBEDDING_MODEL and try again."
    )

engine = create_engine(conn_str)
with engine.connect() as conn:

    # Register pg vector types
    register_vector(conn, True)

    exporter = EmbeddingStore(conn)
    files = get_files()

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
