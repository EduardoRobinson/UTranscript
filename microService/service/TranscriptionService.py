import tempfile
import os
import logging
from faster_whisper import WhisperModel
from transformers import pipeline
from models.llmLoaded import llmLoaded
from models.transcriptionType import TranscriptionResponse

# Configuração do logger
logger = logging.getLogger("TranscricaoLogger")
logger.setLevel(logging.INFO)

handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

class Transcricao:
    def __init__(self, llm: llmLoaded):
        self.llm_pipeline = llm.llm_pipeline
        self.transcribe_model = llm.transcribe_model   

    def log_progresso(self, etapa_atual, total_etapas, mensagem):
        porcentagem = int((etapa_atual / total_etapas) * 100)
        logger.info(f"[{porcentagem}%] {mensagem}")

    async def transcrever(self, arquivo):
        total_etapas = 3
        etapa = 1

        self.log_progresso(etapa, total_etapas, "Salvando arquivo temporário...")
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
            temp_file.write(await arquivo.read())
            temp_path = temp_file.name

        logger.info(f"Arquivo temporário salvo em: {temp_path}")

        etapa += 1
        self.log_progresso(etapa, total_etapas, "Iniciando transcrição com modelo Whisper...")

        try:
            segments, _ = self.transcribe_model.transcribe(temp_path)
            texto = " ".join([seg.text for seg in segments])
        except Exception as e:
            logger.error(f"Erro ao transcrever áudio: {e}", exc_info=True)
            raise e 
        finally:
            os.remove(temp_path)
            logger.info(f"Arquivo temporário removido: {temp_path}")

        etapa += 1
        self.log_progresso(etapa, total_etapas, "Transcrição concluída com sucesso.")

        return await self.gerar_resumo(texto)

    async def gerar_resumo(self, texto):
        total_etapas = 2
        etapa = 1

        self.log_progresso(etapa, total_etapas, "Montando prompt para geração de resumo...")

        prompt = (
            "Resuma a transcrição abaixo feita da video aula como se fosse um relatório, "
            "sem caracteres especiais, e com os temas abordados, trazendo da literatura da área referências quando possível:\n"
            f"{texto}\nResumo:"
        )

        etapa += 1
        self.log_progresso(etapa, total_etapas, "Executando pipeline LLM para geração de resumo...")

        try:
            output = self.llm_pipeline(prompt, do_sample=True, temperature=0.7, max_new_tokens=2048, truncation=True)
            resposta_completa = output[0]["generated_text"]
            if resposta_completa.startswith(prompt):
                resumo = resposta_completa[len(prompt):].strip()
            else:
                resumo = resposta_completa.strip()

            logger.info("Resumo gerado com sucesso.")
        except Exception as e:
            logger.error(f"Erro ao gerar resumo: {e}", exc_info=True)
            raise e

        return TranscriptionResponse(resumo=resumo, transcricao=texto)
