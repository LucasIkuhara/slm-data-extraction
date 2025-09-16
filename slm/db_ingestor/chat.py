from langchain.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_core.vectorstores import InMemoryVectorStore


embeddings = OllamaEmbeddings(model="llama3")
llm = ChatOllama(model="llama3")

vector_store = InMemoryVectorStore(embeddings)
vector_store.load("vec_store.db", embeddings)

retriever = vector_store.as_retriever()
prompt_template = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are an assistant for answering questions.
    Use the provided context to respond.If the answer 
    isn't clear, acknowledge that you don't know. 
    Limit your response to three concise sentences.
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
