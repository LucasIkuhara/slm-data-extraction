from pgvector.psycopg2 import register_vector
from sqlalchemy import create_engine, exc
from os import environ
from embedding_store import EmbeddingStore
from embed_fn import embed_str
from page_reader import PageReader
from ollama import ResponseError


conn_str = environ.get("DB_CONN_STRING")
model = environ.get("EMBEDDING_MODEL")
BASE_PATH = environ.get("PAGES_PATH")

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

    for txt_file in files:

        print(f"Embedding page {txt_file.page} from {txt_file.source_document}")
        try:
            embedding_vec = embed_str(txt_file.raw_text, model)
            exporter.save_embedding(
                txt_file.source_document, txt_file.page, embedding_vec, model
            )
        except exc.IntegrityError:
            print(
                f"Page embedding for {txt_file.source_document} page {txt_file.page} already exists. Skipping..."
            )
            conn.rollback()
            continue
        except ResponseError as err:
            print(
                f"Page embedding for {txt_file.source_document} page {txt_file.page} failed:",
                err,
            )
            continue
    print("Done exporting data.")
