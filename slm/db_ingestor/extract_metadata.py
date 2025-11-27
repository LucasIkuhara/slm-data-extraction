import json
from db_ingestor.chains import make_json_rag_chain
from db_ingestor.config import cfg
import sqlite3


meta_db = sqlite3.connect("metadata.db")
meta_db.autocommit = True
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

for doc in cfg["documents"]:
    rag_chain = make_json_rag_chain(cfg["system-prompt"], [doc], 3000)
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
    basin = obj["bacia"]
    fields = obj["campos"]

    for field in fields:
        meta_db.execute(
            """
        INSERT INTO metadata (bacia, campo, document) values (?, ?, ?)
        """,
            (basin, field, doc),
        )

print(
    len(list(meta_db.execute("SELECT * FROM metadata"))), "docs loaded into metadata."
)
meta_db.close()
