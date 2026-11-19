from pydantic import BaseModel, Field, field_validator, model_validator


class ParAvaliacao(BaseModel):
    predicao: str
    referencia: str

    @field_validator("predicao", "referencia")
    @classmethod
    def texto_preenchido(cls, valor: str) -> str:
        texto = valor.strip()
        if not texto:
            raise ValueError("Informe um texto não vazio.")
        return texto


class AvaliacaoAderencia(BaseModel):
    prompt: str
    resultado: str

    @field_validator("prompt", "resultado")
    @classmethod
    def texto_preenchido(cls, valor: str) -> str:
        texto = valor.strip()
        if not texto:
            raise ValueError("Informe um texto não vazio.")
        return texto


class AvaliacaoRequest(BaseModel):
    resumos: list[ParAvaliacao] = Field(default_factory=list)
    transcricoes: list[ParAvaliacao] = Field(default_factory=list)
    aderencia: list[AvaliacaoAderencia] = Field(default_factory=list)

    @model_validator(mode="after")
    def ao_menos_um_par(self):
        if not self.resumos and not self.transcricoes and not self.aderencia:
            raise ValueError(
                "Informe resumos, transcrições ou a avaliação de adesão ao prompt."
            )
        return self
