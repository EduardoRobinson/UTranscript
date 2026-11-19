class TranscriptionResponse:
    def __init__(self, transcricao: str, resumo: str, prompt: str):
        self.transcricao = transcricao
        self.resumo = resumo
        self.prompt = prompt
