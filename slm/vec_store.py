from os import environ
from langchain_postgres import PGEngine, PGVectorStore
from db_ingestor.chains import embeddings
from db_ingestor.config import cfg


pg_engine = PGEngine.from_connection_string(
    environ["DB_CONN_STRING"],
)
vector_store = PGVectorStore.create_sync(
    engine=pg_engine,
    table_name=cfg["vec-store-table"],
    metadata_columns=["source"],
    schema_name="descom",
    embedding_service=embeddings,
)
