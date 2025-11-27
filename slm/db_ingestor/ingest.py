import os
from langchain_openai import OpenAIEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
from page_reader import PageReader
from db_ingestor.chains import vector_store
from db_ingestor.config import cfg
from datetime import datetime


# Collect all unique document tags
all_docs = vector_store.store.values()
curr_docs = set()
for doc in all_docs:
    src = doc["metadata"]["source"]
    curr_docs.add(src)
print(f"Current PDIs:", len(curr_docs))

# Only embed new documents
found_docs = cfg["documents"]
new_docs = [x for x in found_docs if x not in curr_docs]
print(
    f"Found {len(found_docs)} total documents, {len(new_docs)} are pending embedding.",
    end="\n\n",
)

# Start embedding
chunks = []
for doc in new_docs:
    print("Loading: ", doc)

    # Read text files
    text_reader = PageReader(cfg["txt-docs-dir"])
    files = text_reader.get_files([doc])
    print(f"Found {len(files)} files.")

    # Join and chunk text
    txt = "".join([t.raw_text for t in files])
    doc = Document(txt, metadata={"source": doc})
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks += text_splitter.split_documents([doc])

print(f"Embedding {len(chunks)} chunks...", end="\n\n")
vector_store.add_documents(chunks)

# File dumps
print("Starting file dumps")
fn = cfg["vec-store-path"].split("/")[-1]
bkp_name = f'{cfg["vec-store-bkp-path"]}/{fn}_{datetime.now().isoformat()}'
vector_store.dump(bkp_name)
vector_store.dump(cfg["vec-store-path"])
print("Successfully loaded Db:", cfg["vec-store-path"])
