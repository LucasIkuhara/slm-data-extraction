from json import loads
import os
from langchain.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from slm_extractor.save_results import save_result


MODEL_NAME = "gpt-5-mini"
# ! Ollama
# embeddings = OllamaEmbeddings(model="llama3.2")
# llm = ChatOllama(model="llama3.2", num_ctx=131072)

# ! OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
embeddings = OpenAIEmbeddings(model="text-embedding-3-large", api_key=OPENAI_API_KEY)
llm = ChatOpenAI(model=MODEL_NAME, api_key=OPENAI_API_KEY)


with open("slm_extractor/extraction_options.json", "r") as f:
    cfg = loads(f.read())
    print("Starting with the following config:", cfg)

# Iterate through case studies and models
for case in cfg["caseStudies"]:

    # Skip disabled cases
    if not case["enabled"]:
        continue

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
    msg = """
    Dadas as informações de contexto acima, se possível, extraia diretamente ou calcule as
    variáveis: 
    Distância da Costa
    Comprimento Total do Duto em Km
    Número de Tramos
    Massa Linear de Aço em kg por Metro
    Massa Linear de Polímero em kg por Metro
    Massa Linear de Cobre em kg por Metro
    Massa Linear de Arama em kg por Metro
    Lâmina D'água em mt
    Total de Comprimento a ser Removido em KM
    Peso Total de Aço Removido em Ton
    Peso Total de Polímero Removido em Ton
    Peso Total de Cobre Removido em Ton
    Número de Desconexões
    Número de Recuperação de Extremidades
    Número de Cruzamentos por Baixo
    Número de Cortes
    Número de Navios
    Número de Viagens do Navio
    Número de Tripulantes
    Número de Dias de Uso dos Navios
    Peso Total de Aço em Ton
    Peso Total de Polimero em Ton
    Peso Total de Cobre em Ton

    para os equipamentos da FPSO Cidade de Santos no formato JSON 
    Caso algum dos valores não esteja disponível ou não possa ser calculado com as informações presentes, preencha-as com null.
    """

    response = rag_chain.invoke({"input": msg})
    print()

    # Format and save results
    result = f"SLM Response:\n\n{response["answer"]}\n\nSLM tokens used: {response.prompt_eval_count}"
    print(result)

    case_name = case["name"]
    print("Saving case as: ", case_name)

    save_result(case_name, MODEL_NAME, case, msg, result)
