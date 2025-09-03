from ollama import chat, ChatResponse
from prompter import PromptBuilder
from rag import Rag
from pgvector.psycopg2 import register_vector
from sqlalchemy import create_engine
from os import environ
from embedding_store import EmbeddingStore
from page_reader import PageReader
from json import loads
from slm_extractor.save_results import save_result


# Read config
conn_str = environ.get("DB_CONN_STRING")
PAGES_PATH = environ.get("PAGES_PATH")

with open("slm_extractor/extraction_options.json", "r") as f:
    cfg = loads(f.read())
    print("Starting with the following config:", cfg)

if not all([conn_str, PAGES_PATH]):
    raise Exception(
        "Missing environment variables. Please set DB_CONN_STRING, PAGES_PATH and try again."
    )

# Create db connection
engine = create_engine(conn_str)
with engine.connect() as conn:
    register_vector(conn, True)

    # Iterate through case studies and models
    for case in cfg["caseStudies"]:

        # Skip disabled cases
        if not case["enabled"]:
            continue

        for model in cfg["models"]:
            # Initialize components
            store = EmbeddingStore(conn)
            page_reader = PageReader(PAGES_PATH)
            rag = Rag(store, page_reader, model)
            prompter = PromptBuilder(case["files"], rag)

            # Prompt model
            rag_prompt = case["ragPrompt"]
            msg = prompter.make_prompt(rag_prompt, 45)
            response: ChatResponse = chat(
                model=model,
                messages=[
                    {
                        "role": "user",
                        "content": msg,
                    }
                ],
                options={"num_ctx": 45_000},
            )

            # Format and save results
            result = f"SLM Response:\n\n{response.message.content}\n\nSLM tokens used: {response.prompt_eval_count}"
            print(result)
            save_result(case["name"], model + "-45", case, msg, result)
