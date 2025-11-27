from db_ingestor.chains import make_json_rag_chain
from db_ingestor.config import cfg


rag_chain = make_json_rag_chain(
    cfg["system-prompt"], ["pdi-executivo-plataforma-biquara-01"], 2000
)


question = """
Extraia o nome da bacia e seus respectivos campos no formato json seguindo o padrão:
{
    bacia: string,
    campos: string[]
}
"""

response = rag_chain.invoke({"input": question})
print(response["answer"])
