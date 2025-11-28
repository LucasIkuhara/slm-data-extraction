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
db_size = cfg["max-rag-ctx"]
from vec_store import vector_store


def make_rag_chain(sys_prompt: str, docs: list[str], llm=llm, k=None) -> Runnable:
    k_size = db_size if not k else k
    retriever = vector_store.as_retriever(
        k=k_size,
        search_kwargs={"filter": {"source": {"$in": docs}}},
    )

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
    model_kwargs=dict(response_format=dict(type="json_object")),
)


def make_json_rag_chain(sys_prompt: str, docs: list[str], k=None) -> Runnable:
    return make_rag_chain(sys_prompt, docs, json_llm, k=k)
