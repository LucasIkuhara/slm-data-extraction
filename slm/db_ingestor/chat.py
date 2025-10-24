import os
from langchain.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from yaml import safe_load


with open("db_ingestor/config.yml") as yml:
    cfg = safe_load(yml)
assert cfg


# ! Ollama
# embeddings = OllamaEmbeddings(model="llama3.2")
# llm = ChatOllama(model="llama3.2", num_ctx=131072)

# ! OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
embeddings = OpenAIEmbeddings(model="text-embedding-3-large", api_key=OPENAI_API_KEY)
llm = ChatOpenAI(model="gpt-5", api_key=OPENAI_API_KEY)

vector_store: InMemoryVectorStore = InMemoryVectorStore.load(
    "vec-stores/oai_3_large_vec_store.db", embeddings
)


db_size = len(vector_store.store.items())
print(f"Total db size: {db_size} items.")

retriever = vector_store.as_retriever(k=db_size)
prompt_template = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            {cfg["sys"]} + "\n{context}",
        ),
        ("human", "{input}"),
    ]
)

qa_chain = create_stuff_documents_chain(llm, prompt_template)
rag_chain = create_retrieval_chain(retriever, qa_chain)

if __name__ == "__main__":
    print("Chat with Document")
    while True:
        question = input("Your Question:\n > ")

        if question:
            response = rag_chain.invoke({"input": question})
            print(response["answer"])
