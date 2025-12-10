import json
from db_ingestor.chains import make_json_rag_chain
from db_ingestor.config import cfg
import pandas as pd
from datetime import datetime
from pathlib import Path
from metadata_db import query_metadata


# Get candidate Basin - Field pairs
targets = list(
    query_metadata(
        "SELECT DISTINCT BACIA, CAMPO, DOCUMENT, TITLE_NAME FROM DESCOM.METADATA WHERE ENABLED = TRUE"
    )
)
extracted = []


def enhance_prompt(base: str, field: str, dtype: str) -> str:
    if dtype == "boolean":
        json_template = cfg["prompt-suffix-boolean"]
    elif dtype == "number":
        json_template = cfg["prompt-suffix-number"]
    else:
        json_template = cfg["prompt-suffix-string"]

    return (base + " " + json_template).replace("{campo}", field)


def extract_col_by_field(field: str, basin: str, doc: str, title: str) -> tuple:

    print(f"Running [basin={basin}, field={field}]: {title}")

    # Create a chain with rag only containing these docs
    chain = make_json_rag_chain(cfg["system-prompt"], [doc])

    ext = [basin, field, title]
    for quest in cfg["questions"]:

        prompt = enhance_prompt(quest["prompt"], field, quest["type"])
        var = quest["var"]

        print(f"Extracting {var}: {prompt}")
        resp = chain.invoke({"input": prompt})
        resp_obj = json.loads(resp["answer"])

        # Append extraction
        ext += [resp_obj["valor"], resp_obj["fonte"]]
    return tuple(ext)


for basin, field, doc, title in targets:
    try:
        field_cols = extract_col_by_field(field, basin, doc, title)
        extracted.append(field_cols)
    except Exception as err:
        print(f"Warning! Skipped {basin} - {field}. Results will be incomplete")
        print(err)
        continue

# Save results
today = datetime.now()
dir_name = f"results/{today.strftime('%Y-%m-%d')}"
Path(dir_name).mkdir(parents=True, exist_ok=True)
file_path = f"{dir_name}/out_{today.isoformat()}.csv"

cols = ["Bacia", "Campo", "Document"]
for quest in cfg["questions"]:
    cols += [quest["var"], quest["var"] + "_src"]
df = pd.DataFrame(extracted, columns=cols)
df.to_csv(file_path, index=False)
