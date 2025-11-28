import json
from db_ingestor.chains import make_json_rag_chain
from db_ingestor.config import cfg
import sqlite3


meta_db = sqlite3.connect("metadata.db", autocommit=True)
meta_db.execute(
    """
CREATE TABLE IF NOT EXISTS metadata (
    id INTEGER PRIMARY KEY,
    bacia TEXT,
    campo TEXT,
    document TEXT,
    extracted INTEGER DEFAULT 0,
    validated INTEGER DEFAULT 0
)
"""
)

# Avoid running on old docs
previous_docs = meta_db.execute("SELECT DISTINCT DOCUMENT FROM METADATA").fetchall()
previous_docs = [x[-1] for x in previous_docs]
print(previous_docs)
docs = [x for x in cfg["documents"] if x not in previous_docs]
print(f"Loaded {len(previous_docs)} previous docs. {len(docs)} outstanding.")

for doc in docs:
    rag_chain = make_json_rag_chain(cfg["system-prompt"], [doc])
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
        meta_db.execute(
            """
        INSERT INTO metadata (bacia, campo, document) values (?, ?, ?)
        """,
            (basin, field, doc),
        )
        meta_db.commit()

print(
    len(list(meta_db.execute("SELECT * FROM metadata"))), "docs loaded into metadata."
)
meta_db.close()
