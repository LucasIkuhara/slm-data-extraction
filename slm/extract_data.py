import json
from chains import make_json_rag_chain
from config import cfg
import pandas as pd
from datetime import datetime
from pathlib import Path
from metadata_db import query_metadata
from pathlib import Path

# Get candidate Basin - Field pairs
targets = list(
    query_metadata(
        "SELECT DISTINCT basin, field, name, title FROM DESCOM.DOC_BASIN_FIELDS WHERE ENABLED = TRUE"
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


def extract_col_by_field(field: str, basin: str, doc: str, title: str, k: int) -> tuple:

    print(f"Running [basin={basin}, field={field}]: {title}")

    # Create a chain with rag only containing these docs
    chain = make_json_rag_chain(cfg["system-prompt"], [doc], k=k)

    # Start with metadata variables
    extracted_vars = [basin, field, title, str(k)]

    for base_prompt in cfg["questions"]:

        prompt = enhance_prompt(base_prompt["prompt"], field, base_prompt["type"])
        var = base_prompt["var"]

        print(f"Extracting {var}: {prompt}")
        resp = chain.invoke({"input": prompt})
        resp_obj = json.loads(resp["answer"])

        # Append extraction
        extracted_vars += [resp_obj["valor"], resp_obj["fonte"]]
    return tuple(extracted_vars)


for k in [1, 2, 4, 8, 16]:
    for basin, field, doc, title in targets:
        try:
            field_cols = extract_col_by_field(field, basin, doc, title, k)
            extracted.append(field_cols)
        except Exception as err:
            print(f"Warning! Skipped {basin} - {field}. Results will be incomplete")
            print(err)
            continue

# Save results
today = datetime.now()
dir_name = f"results/{today.strftime('%Y-%m-%d')}"
Path(dir_name).mkdir(parents=True, exist_ok=True)
file_path = f"{dir_name}/out_{today.isoformat()}.xlsx"

cols = ["Bacia", "Campo", "Document", "K"]
for quest in cfg["questions"]:
    cols += [quest["var"], quest["var"] + "_src"]
df = pd.DataFrame(extracted, columns=cols)
df.to_excel(file_path, index=False)

# Update pointer to latest
symlink = Path("results/latest.xlsx")
if symlink.exists():
    symlink.unlink()
symlink.symlink_to(file_path)
