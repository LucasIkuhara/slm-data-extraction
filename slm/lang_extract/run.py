import os
import langextract as lx
from page_reader import PageReader

# 1. Define the prompt and extraction rules
prompt = """
Qual a extensão total da tubulação rígida instalada na bacia?
"""


# 2. Provide a high-quality example to guide the model
examples = [
    lx.data.ExampleData(
        text="""
Os principais equipamentos do sistema (sistema aquecimento) são:

| Equipamentos                             |   Quantidade | Capacidade   | Pressão        | Volume   | Vazão      | Temperatura   |
|------------------------------------------|--------------|--------------|----------------|----------|------------|---------------|
| Vaso de expansão de Alta Temperatura     |            1 | 22 m³        | 15,5 kgf/cm²   | 21,74 m³ | N/A        | 148-200 °C    |
| Bomba de circulação de Alta Temperatura  |            2 | N/A          | ΔP=4,5 kgf/cm² | N/A      | 597 m³/h   | 148,1 °C      |
| Vaso de expansão de Baixa Temperatura    |            1 | 22 m³        | 2,14 kgf/cm²   | 21,90 m³ | N/A        | 77-120 °C     |
| Bomba de circulação de Baixa Temperatura |            2 | N/A          | ΔP=3,5 kgf/cm² | N/A      | 504 m³/h   | 77-120 °C     |
| Recuperador de calor (WHRU)              |            3 | 13.7 MW cada | 19,37 kgf/cm²  | 0,6 m³   | 204,5 m³/h | 200 °C        |
""",
        extractions=[
            lx.data.Extraction(
                extraction_class="Pressão",
                extraction_text="15,5 kgf/cm²",
                attributes={"equipamento": "Vaso de expansão de Alta Temperatura"},
            ),
            lx.data.Extraction(
                extraction_class="Volume",
                extraction_text="21,90 m³",
                attributes={"equipamento": "Vaso de expansão de Baixa Temperatura"},
            ),
            lx.data.Extraction(
                extraction_class="Vazão",
                extraction_text="204,5 m³/h",
                attributes={"equipamento": "Recuperador de calor (WHRU)"},
            ),
        ],
    )
]

BASE_PATH: str = os.getenv("PAGES_PATH")
text_reader = PageReader(BASE_PATH)
files = text_reader.get_files(doc_filter=["pdf-fpso-cidade-de-santos"])
txt = "".join([t.raw_text for t in files])
print(len(files))

result = lx.extract(
    text_or_documents=txt,
    prompt_description=prompt,
    examples=examples,
    model_id="gpt-5-mini",  # Automatically selects OpenAI provider
    api_key=os.environ.get("OPENAI_API_KEY"),
    fence_output=True,
    use_schema_constraints=False,
)
print(result)
