import json
from db_ingestor.chains import make_json_rag_chain
from db_ingestor.config import cfg
from metadata_db import query_metadata


query_metadata(
    """
CREATE TABLE IF NOT EXISTS descom.metadata
(
    id integer NOT NULL,
    bacia text COLLATE pg_catalog."default",
    campo text COLLATE pg_catalog."default",
    document text COLLATE pg_catalog."default",
    extracted boolean DEFAULT false,
    validated boolean DEFAULT false,
    enabled boolean DEFAULT false,
    title_name text COLLATE pg_catalog."default",
    is_executive boolean,
    CONSTRAINT "METADATA_pkey" PRIMARY KEY (id)
)
"""
)

# Avoid running on old docs
previous_docs = query_metadata(
    "SELECT DISTINCT DOCUMENT FROM descom.METADATA"
).fetchall()
previous_docs = [x[-1] for x in previous_docs]
print(previous_docs)
docs = [x for x in cfg["documents"] if x not in previous_docs]
print(f"Loaded {len(previous_docs)} previous docs. {len(docs)} outstanding.")
for doc in docs:
    sys = (
        "Descubra o nome da Bacia sobre a qual o documento fala e quais os seus campos"
    )
    rag_chain = make_json_rag_chain(sys, [doc], 500)
    question = """
    Extraia o nome da bacia e seus respectivos campos no formato json seguindo o padrão:
    {
        bacia: string,
        campos: string[]
    }
    """

    print("Evaluating:", doc)
    response = rag_chain.invoke({"input": question})
    obj = json.loads(response["answer"])

    print("Found:", obj)
    basin = obj["bacia"]
    fields = obj["campos"]

    for field in fields:
        query_metadata(
            """
        INSERT INTO descom.metadata (bacia, campo, document) values (?, ?, ?); COMMIT
        """,
            (basin, field, doc),
        )

print(
    len(list(query_metadata("SELECT * FROM descom.metadata"))),
    "docs loaded into metadata.",
)
