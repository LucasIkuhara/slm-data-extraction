from typing import List
from rag import Rag


class PromptBuilder:
    def __init__(self, context_files: List[str], rag: Rag, debug_mode: bool = False):
        self.context_files = context_files
        self.rag = rag
        self.debug = debug_mode

    def load_context(self, prompt: str, page_count: int) -> str:

        if self.debug:
            print("RAG Prompt:\n\n", prompt)

        ctx = self.rag.get_context_by_prompt(prompt, self.context_files, page_count)

        if len(ctx) == 0:
            print(f"Warning! no RAG pages found.")

        ctx_txt = ""
        for page in ctx:
            tag = f"{page.source_document}: pg. {page.page}"
            pg_txt = f"<{tag}>\n {page.raw_text} \n<{tag}/>\n"
            ctx_txt += pg_txt

        return ctx_txt

    def make_prompt(self, ctx_prompt: str, pages: int) -> str:
        template = """
        Dadas as informações de contexto acima, se possível, extraia diretamente ou calcule as
        variáveis Distância da Costa (distCosta), Comprimento Total do Duto em Km (compTotalDuto), 
        Número de Tramos (numTramos), Massa Linear de Aço em kg por Metro (massaLinearAco), 
        Massa Linear de Polímero em kg por Metro (massaLinearPolimero) para os equipamentos da FPSO Cidade de Santos no formato JSON seguindo
        o exemplo: {
            "distCosta": 12,
            "compTotalDuto": 10,
            "numTramos": 3,
            "massaLinearAco": 40,
            "massaLinearPolimero": 30,
        }

        Caso algum dos valores não esteja disponível ou não possa ser calculado com as informações presentes, preencha-as com null.
        """

        prompt = self.load_context(ctx_prompt, pages) + template
        if self.debug:
            print("Final Prompt:\n\n", prompt)

        return prompt
