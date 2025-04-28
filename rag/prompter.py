from rag import Rag


class PromptBuilder:
    def __init__(self, context_file: str, rag: Rag):
        self.base_file = context_file
        self.rag = rag
        self.ctx = self.load_context()

    def load_context(self, prompt: str) -> str:
        ctx = self.rag.get_context_by_prompt(prompt, [self.base_file])
        ctx_txt = ""
        for page in ctx:
            tag = f"{page.source_document} - {page.page}"
            ctx_txt += f"<{tag}> {page.raw_text} <{tag}/>"

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

        return self.load_context(ctx_prompt) + template
