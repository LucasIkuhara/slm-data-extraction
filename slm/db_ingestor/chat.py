from db_ingestor.chains import make_rag_chain
from db_ingestor.config import cfg

rag_chain = make_rag_chain(
    cfg["system-prompt"],
    [
        "PDI_E_P_PAG_0",  # Agulha
        # "pdi-executivo-fpso-cidade-santos1"  # Tambau/Uruguá
    ],
    k=4,
)

if __name__ == "__main__":
    print("Chat with Document")
    while True:
        question = input("Your Question:\n > ")

        if question:
            response = rag_chain.invoke({"input": question})
            print(response["answer"])
