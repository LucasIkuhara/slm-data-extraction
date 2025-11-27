import json
from db_ingestor.chains import make_json_rag_chain
from db_ingestor.config import cfg
import pandas as pd
from datetime import datetime
import sqlite3
from pathlib import Path


# Get candidate Basin - Field pairs
meta_db = sqlite3.connect("metadata.db")
targets = list(meta_db.execute("SELECT DISTINCT BACIA, CAMPO FROM METADATA"))
extracted = []


def enhance_prompt(base: str, field: str) -> str:
    json_template = """
    Caso a resposta seja verdadeiro ou falso, responda 1 para verdadeiro e 0 para falso.
    Responda em json seguindo o formato: 
    {
        valor: number,
        fonte: string
    }
    """
    return (base + json_template).replace("{campo}", field)


for basin, field in targets:

    # Get relevant documents by basin - field
    docs = meta_db.execute(
        "SELECT document FROM METADATA WHERE BACIA = ? AND CAMPO = ?",
        (basin, field),
    ).fetchall()
    docs = [x[0] for x in docs]

    print(f"Running [basin={basin}, field={field}]: {docs}")

    # Create a chain with rag only containing these docs
    chain = make_json_rag_chain(cfg["system-prompt"], docs)
    for quest in cfg["questions"]:

        prompt = enhance_prompt(quest["prompt"], field)
        var = quest["var"]

        print(f"Extracting {var}: {prompt}")
        resp = chain.invoke({"input": prompt})
        resp_obj = json.loads(resp["answer"])

        # Append extraction
        ext = (basin, field, var, prompt, resp_obj["valor"], resp_obj["fonte"])
        extracted.append(ext)

# Save results
today = datetime.now()
dir_name = f"results/{today.strftime('%Y-%m-%d')}"
Path(dir_name).mkdir(parents=True, exist_ok=True)
file_path = f"{dir_name}/raw_{today.isoformat()}.csv"
df = pd.DataFrame(
    extracted, columns=["Bacia", "Campo", "Coluna", "Prompt", "Valor", "Fonte"]
)
df.to_csv(file_path, index=False)
