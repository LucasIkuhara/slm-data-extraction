# %%import os
import asyncio
from os import environ
from langchain.docstore.document import Document

from langchain_postgres import PGEngine
from langchain_text_splitters import RecursiveCharacterTextSplitter
from db_ingestor.chains import embeddings, vector_store
from db_ingestor.config import cfg
from datetime import datetime
import psycopg
from pgvector.psycopg import register_vector
from psycopg.types.json import Jsonb

# Connect to your PostgreSQL database
conn = psycopg.connect(
    environ["DB_CONN_STRING"],
)
register_vector(conn)

# Register the vector type for Psycopg 3

# Create a table with a vector column


# Collect all unique document tags
store = vector_store.store
amt = len(store)
i = 0
print("store loaded")
for key in store:
    i += 1
    val = store[key]
    print("insert", i / amt)
    conn.execute(
        """
    INSERT INTO oai_3_large_vec_store (langchain_id, content, embedding, langchain_metadata) VALUES (%s, %s, %s, %s)
    """,
        (val["id"], val["text"], val["vector"], Jsonb(val["metadata"])),
    )
    conn.commit()


# Insert data with vector embeddings

# # %%
# from langchain_postgres import PGVectorStore

# table = "oai_3_large_vec_store"


# pg_engine = PGEngine.from_connection_string(
#     environ["DB_CONN_STRING"],
# )


# # pg_engine.init_vectorstore_table(
# #     table_name=table,
# #     vector_size=3072,
# #     exi
# # )
# async def main():
#     chunks = []
#     vector_store = await PGVectorStore.create(
#         engine=pg_engine,
#         table_name=table,
#         embedding_service=embeddings,
#     )
#     doc = Document("sime txt", metadata={"source": "doc.pdf"})
#     text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
#     chunks += text_splitter.split_documents([doc])
#     print("exporting", chunks)
#     # f6d7110c-07d7-4345-9c02-eec058691c42
#     vector_store.add_documents(chunks)
#     print("exported")


# asyncio.run(main())
