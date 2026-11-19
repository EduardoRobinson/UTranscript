import json
import logging
import re
import threading
import unicodedata

from dto.avaliacaoDTO import AvaliacaoAderencia, AvaliacaoRequest
from models.qwenJudge import QwenJudge

logger = logging.getLogger("AvaliacaoLogger")
logger.setLevel(logging.INFO)
logger.propagate = False
if not logger.handlers:
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("%(asctime)s | %(levelname)s | %(message)s"))
    logger.addHandler(handler)


def _numero(valor) -> float:
    return round(float(valor), 4)


_CRITERIOS = ("adesao", "fidelidade", "cobertura", "organizacao")

_JUIZ = (
    "Você avalia se o resultado gerado segue o prompt. "
    "Não reescreva o resultado. "
    "Responda exatamente com cinco linhas, nesta ordem, sem JSON e sem markdown. "
    "Nas quatro primeiras linhas, depois dos dois-pontos, escreva somente um número decimal de 0 a 1. "
    "Não omita nenhuma linha. "
    "adesao mede se o resultado cumpre as instruções do prompt. "
    "fidelidade mede se o resultado respeita os limites que o prompt impõe sobre o que pode ser incluído. "
    "cobertura mede se o resultado contempla o que o prompt pede. "
    "organizacao mede se a forma do texto segue o que o prompt pediu. "
    "justificativa traz uma ou duas frases sobre o que o resultado fez bem e o que faltou. "
    "A nota precisa concordar com a justificativa: critério elogiado fica perto de 1; critério criticado fica perto de 0; critério parcial fica no meio. "
    "Não repita 0 nos quatro critérios quando a justificativa não condenar todos. "
    "Formato da resposta:\n"
    "adesao:\n"
    "fidelidade:\n"
    "cobertura:\n"
    "organizacao:\n"
    "justificativa:"
)

_NOTA_LINHA = re.compile(
    r"(?i)\b(ades[aã]o|fidelidade|cobertura|organiza[cç][aã]o)\b\s*[:=]\s*"
    r"([0-9]+(?:[.,][0-9]+)?|[.,][0-9]+)"
)


def _chave(nome: str) -> str:
    base = unicodedata.normalize("NFD", str(nome).strip().lower())
    return "".join(caractere for caractere in base if unicodedata.category(caractere) != "Mn")


def _nota_de(valor) -> float:
    if isinstance(valor, str):
        valor = valor.strip().replace(",", ".")
    nota = float(valor)
    if nota > 1:
        nota = nota / 100 if nota > 5 else nota / 5
    return _numero(min(1.0, max(0.0, nota)))


def _montar(bruto: dict, justificativa: str) -> dict:
    notas = {chave: _nota_de(bruto[chave]) for chave in _CRITERIOS}
    notas["nota"] = _numero(sum(notas[chave] for chave in _CRITERIOS) / len(_CRITERIOS))
    notas["justificativa"] = justificativa.strip().strip('"').strip("'")
    return notas


def _do_json(texto: str) -> dict | None:
    candidatos = list(re.finditer(r"\{[^{}]*\}", texto, flags=re.DOTALL))
    for candidato in reversed(candidatos):
        try:
            bruto = json.loads(candidato.group(0))
        except json.JSONDecodeError:
            continue
        if not isinstance(bruto, dict):
            continue
        normalizado = {_chave(chave): valor for chave, valor in bruto.items()}
        if all(chave in normalizado for chave in _CRITERIOS):
            return _montar(normalizado, str(normalizado.get("justificativa", "")))
    return None


def _das_linhas(texto: str) -> dict | None:
    achados = {}
    for nome, valor in _NOTA_LINHA.findall(texto):
        achados[_chave(nome)] = valor
    if not all(chave in achados for chave in _CRITERIOS):
        return None
    justificativa = ""
    match = re.search(r"(?i)justificativa\s*[:=]\s*[\"']?(.*)", texto, flags=re.DOTALL)
    if match:
        justificativa = match.group(1).strip()
    return _montar(achados, justificativa)


def _extrair_avaliacao(texto: str) -> dict:
    extraido = _do_json(texto) or _das_linhas(texto)
    if extraido is None:
        raise ValueError("O juiz não devolveu as notas adesao, fidelidade, cobertura e organizacao.")
    return extraido


class EvaluationService:
    """Métricas da transcrição, do resumo e da adesão ao prompt.

    ROUGE compara o resumo gerado com um resumo de referência.
    WER e CER comparam a transcrição do Whisper com uma transcrição de referência.
    A adesão usa o Qwen3-0.6B para ler o prompt e o resultado, e devolve notas de 0 a 1.
    """

    def __init__(self):
        self._lock = threading.Lock()
        self._metricas = {}
        self._juiz_qwen = QwenJudge()

    def definir_juiz(self, juiz: QwenJudge):
        self._juiz_qwen = juiz

    def avaliar(self, pedido: AvaliacaoRequest, llm=None) -> dict:
        resultado = {}
        with self._lock:
            if pedido.resumos:
                resultado["resumo"] = self._avaliar_resumos(
                    [item.predicao for item in pedido.resumos],
                    [item.referencia for item in pedido.resumos],
                )
            if pedido.transcricoes:
                resultado["transcricao"] = self._avaliar_transcricoes(
                    [item.predicao for item in pedido.transcricoes],
                    [item.referencia for item in pedido.transcricoes],
                )
        if pedido.aderencia:
            resultado["aderencia"] = self._avaliar_aderencia(pedido.aderencia, llm)
        return resultado

    def _carregar(self, nome: str):
        if nome not in self._metricas:
            evaluate = self._importar_evaluate()
            self._compatibilizar_huggingface_hub()
            if nome == "rouge":
                self._garantir_nltk()
            logger.info("Carregando métrica do evaluate: %s", nome)
            self._metricas[nome] = evaluate.load(nome)
        return self._metricas[nome]

    def _compatibilizar_huggingface_hub(self):
        """evaluate 0.4.3 ainda lê o token por HfFolder, removido no huggingface_hub 1.x."""
        import huggingface_hub
        from huggingface_hub import hf_api

        if hasattr(hf_api, "HfFolder"):
            return

        class HfFolder:
            @staticmethod
            def get_token():
                return huggingface_hub.get_token()

        hf_api.HfFolder = HfFolder

    def _importar_evaluate(self):
        try:
            import evaluate
        except ImportError as e:
            raise RuntimeError(
                "A biblioteca evaluate não está instalada. Reconstrua a imagem do microsserviço."
            ) from e
        return evaluate

    def _garantir_nltk(self):
        try:
            import nltk
        except ImportError as e:
            raise RuntimeError(
                "O pacote nltk não está instalado. Reconstrua a imagem do microsserviço."
            ) from e
        for recurso in ("punkt_tab", "punkt"):
            try:
                nltk.data.find(f"tokenizers/{recurso}")
            except LookupError:
                nltk.download(recurso, quiet=True)

    def _avaliar_resumos(self, predicoes: list[str], referencias: list[str]) -> dict:
        rouge = self._carregar("rouge")
        agregado = rouge.compute(
            predictions=predicoes,
            references=referencias,
            use_stemmer=False,
            use_aggregator=True,
        )
        por_amostra = rouge.compute(
            predictions=predicoes,
            references=referencias,
            use_stemmer=False,
            use_aggregator=False,
        )
        amostras = []
        for indice in range(len(predicoes)):
            amostras.append({chave: _numero(valores[indice]) for chave, valores in por_amostra.items()})

        return {
            "agregado": {chave: _numero(valor) for chave, valor in agregado.items()},
            "amostras": amostras,
        }

    def _avaliar_transcricoes(self, predicoes: list[str], referencias: list[str]) -> dict:
        wer = self._carregar("wer")
        cer = self._carregar("cer")
        agregado = {
            "wer": _numero(wer.compute(predictions=predicoes, references=referencias)),
            "cer": _numero(cer.compute(predictions=predicoes, references=referencias)),
        }
        amostras = [
            {
                "wer": _numero(wer.compute(predictions=[predicao], references=[referencia])),
                "cer": _numero(cer.compute(predictions=[predicao], references=[referencia])),
            }
            for predicao, referencia in zip(predicoes, referencias)
        ]
        return {"agregado": agregado, "amostras": amostras}

    def _avaliar_aderencia(self, itens: list[AvaliacaoAderencia], llm=None) -> dict:
        amostras = [self._julgar(item) for item in itens]
        agregado = {
            chave: _numero(sum(amostra[chave] for amostra in amostras) / len(amostras))
            for chave in (*_CRITERIOS, "nota")
        }
        return {"agregado": agregado, "amostras": amostras}

    def _julgar(self, item: AvaliacaoAderencia) -> dict:
        messages = [
            {"role": "system", "content": _JUIZ},
            {
                "role": "user",
                "content": (
                    f"Prompt:\n{item.prompt}\n\n"
                    f"Resultado gerado:\n{item.resultado}"
                ),
            },
        ]
        logger.info("Avaliando adesão do resultado ao prompt com Qwen3-0.6B.")
        resposta = self._juiz_qwen.gerar(messages)
        resposta = re.sub(r"<think>.*?</think>", "", resposta, flags=re.DOTALL).strip()
        logger.info("Resposta do juiz: %s", resposta.replace("\n", " | "))
        try:
            return _extrair_avaliacao(resposta)
        except ValueError:
            logger.error("Resposta do juiz sem as quatro notas: %s", resposta.replace("\n", " | "))
            raise
