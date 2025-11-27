from langchain.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.runnables.base import Runnable
import os
from db_ingestor.config import cfg
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

# ! Ollama
# embeddings = OllamaEmbeddings(model="llama3.2")
# llm = ChatOllama(model="llama3.2", num_ctx=131072)

# ! OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
embeddings = OpenAIEmbeddings(model="text-embedding-3-large", api_key=OPENAI_API_KEY)
llm = ChatOpenAI(model="gpt-5", api_key=OPENAI_API_KEY)

vector_store: InMemoryVectorStore = InMemoryVectorStore.load(
    cfg["vec-store-path"], embeddings
)


db_size = len(vector_store.store.items())
print(f"Total db size: {db_size} items.")


def make_rag_chain(sys_prompt: str, docs: list[str] = [], llm=llm) -> Runnable:
    if docs:

        def filter_docs(x):
            src = x.metadata["source"]
            return src in docs

        retriever = vector_store.as_retriever(
            k=db_size,
            search_kwargs={"filter": filter_docs},
        )
    else:
        retriever = vector_store.as_retriever(k=db_size)

    prompt_template = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                sys_prompt + "\n{context}",
            ),
            ("human", "{input}"),
        ]
    )

    qa_chain = create_stuff_documents_chain(llm, prompt_template)
    rag_chain = create_retrieval_chain(retriever, qa_chain)
    return rag_chain


json_llm = ChatOpenAI(
    model="gpt-5",
    api_key=OPENAI_API_KEY,
    model_kwargs=dict(response_format=dict(type="object_json")),
)


def make_json_rag_chain(sys_prompt: str, docs: list[str] = []) -> Runnable:
    return make_rag_chain(sys_prompt, docs, json_llm)
