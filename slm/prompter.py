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

        prompt = self.load_context(ctx_prompt, pages) + template
        if self.debug:
            print("Final Prompt:\n\n", prompt)

        return prompt
