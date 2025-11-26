from db_ingestor.chains import make_rag_chain
from db_ingestor.config import cfg
import pandas as pd

extracted = []

for document in cfg["documents"]:

    # Create a chain with rag only containing this doc
    print("Current chain: ", document)
    chain = make_rag_chain(cfg["system-prompt"], [document])
    for quest in cfg["questions"]:

        prompt = quest["prompt"]
        eq = quest["equipment"]

        print(f"Extracting {document}: {prompt}")
        resp = chain.invoke({"input": prompt})
        ext = (document, eq, prompt, resp["answer"])
        extracted.append(ext)

df = pd.DataFrame(extracted, columns=["Document", "Equipment", "Question", "Response"])
df.to_csv("out2.csv", index=False)
