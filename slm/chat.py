from chains import make_rag_chain
from config import cfg

rag_chain = make_rag_chain(
    cfg["system-prompt"],
    [
        "PDI_E_P_PAG_01",  # Agulha
        # "pdi-executivo-fpso-cidade-santos1"  # Tambau/Uruguá
        # "pdi-conceitual-partei-petrobras-plataforma-p-47-viola"  # Marlim
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
