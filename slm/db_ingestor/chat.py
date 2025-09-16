from langchain.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_core.vectorstores import InMemoryVectorStore


embeddings = OllamaEmbeddings(model="llama3.2")
llm = ChatOllama(model="llama3.2")

vector_store = InMemoryVectorStore.load("vec_store.db", embeddings)

retriever = vector_store.as_retriever(k=20)
print(vector_store)
prompt_template = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """Você é um assistente que deverá responder perguntas baseadas no contexto.
            Caso não saiba a resposta, admita não sabê-la.
    {context}
    
    """,
        ),
        ("human", "{input}"),
    ]
)

qa_chain = create_stuff_documents_chain(llm, prompt_template)
rag_chain = create_retrieval_chain(retriever, qa_chain)

print("Chat with Document")

while True:
    question = input("Your Question:\n > ")

    if question:
        response = rag_chain.invoke({"input": question})
        print(response["answer"])
