from db_ingestor.chains import make_rag_chain
from db_ingestor.config import cfg


print(cfg)
document = ["pdis-conceituais-marlim-voador"]
chain = make_rag_chain(cfg["system-prompt"], document)

for quest in cfg["questions"]:
    print(quest)

x = chain.invoke({"input": "Sobre quais bacias o texto fala?"})
print(x)
