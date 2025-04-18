class PromptBuilder:
    def __init__(self, context_file: str):
        self.base_file = context_file
        self.ctx = self.load_context()

    def load_context(self) -> str:
        with open(self.base_file, "r") as fd:
            return fd.read()

    def make_prompt(self) -> str:
        template = """Dadas as informações de contexto a abaixo, retorne uma estimativa para as
        variáveis Distância da Costa (distCosta), Comprimento Total do Duto em Km (compTotalDuto), 
        Número de Tramos (numTramos), Massa Linear de Aço em kg por Metro (massaLinearAco), 
        Massa Linear de Polímero em kg por Metro (massaLinearPolimero); no formato JSON seguindo
        o exemplo {
            "distCosta": number,
            "compTotalDuto": number,
            "numTramos": number,
            "massaLinearAco": number,
            "massaLinearPolimero": number,
        }

        Contexto:

        """

        return template + self.ctx
