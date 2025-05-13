from rag import Rag


class PromptBuilder:
    def __init__(self, context_file: str, rag: Rag, debug_mode: bool = False):
        self.base_file = context_file
        self.rag = rag
        self.debug = debug_mode

    def load_context(self, prompt: str) -> str:

        if self.debug:
            print("RAG Prompt:\n\n", prompt)

        ctx = self.rag.get_context_by_prompt(prompt, [self.base_file], 30)
        ctx_txt = ""
        for page in ctx:
            tag = f"{page.source_document}: pg. {page.page}"
            pg_txt = f"<{tag}>\n {page.raw_text} \n<{tag}/>\n"
            ctx_txt += pg_txt

        return ctx_txt

    def make_prompt(self, ctx_prompt: str) -> str:
        template = """
        Dadas as informações de contexto acima, retorne uma estimativa para as
        variáveis Distância da Costa (distCosta), Comprimento Total do Duto em Km (compTotalDuto), 
        Número de Tramos (numTramos), Massa Linear de Aço em kg por Metro (massaLinearAco), 
        Massa Linear de Polímero em kg por Metro (massaLinearPolimero); no formato JSON seguindo
        o exemplo {
            "distCosta": 12,
            "compTotalDuto": 10,
            "numTramos": 3,
            "massaLinearAco": 40,
            "massaLinearPolimero": 30,
        }
        """

        prompt = self.load_context(ctx_prompt) + template
        if self.debug:
            print("Final Prompt:\n\n", prompt)

        return prompt
