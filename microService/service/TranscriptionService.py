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

    # Seu arquivo de Transcricao
    async def gerar_resumo(self, texto):
        total_etapas = 2
        etapa = 1

        self.log_progresso(etapa, total_etapas, "Montando prompt estruturado...")

        messages = [
            {
                "role": "system", 
                "content": (
                    "Você é um assistente acadêmico especializado em síntese de conteúdo. "
                    "Crie um relatório objetivo da videoaula abaixo. Use linguagem formal, "
                    "cite conceitos da literatura de sistemas operacionais se aplicável. "
                    "IMPORTANTE: Não adicione avisos de tradução, notas de revisão ou repetições ao final. "
                    "Termine o texto assim que concluir o resumo dos temas."
                )
            },
            {
                "role": "user", 
                "content": f"Transfira esta transcrição em um resumo estruturado sem caracteres especiais:\n\n{texto}"
            },
        ]

        prompt = self.llm_pipeline.tokenizer.apply_chat_template(
            messages, 
            tokenize=False, 
            add_generation_prompt=True
        )

        etapa += 1
        self.log_progresso(etapa, total_etapas, "Gerando resumo sem repetições...")

        try:
            output = self.llm_pipeline(
                prompt, 
                max_new_tokens=1024, # 2048 era muito, facilitava o loop
                do_sample=True,
                temperature=0.6,
                eos_token_id=[
                    self.llm_pipeline.tokenizer.eos_token_id,
                    self.llm_pipeline.tokenizer.convert_tokens_to_ids("<|eot_id|>") # Token de parada do Llama 3
                ]
            )
            
            resposta_completa = output[0]["generated_text"]
            resumo = resposta_completa[len(prompt):].strip()
            logger.info("Resumo gerado com sucesso.")
        except Exception as e:
            logger.error(f"Erro ao gerar resumo: {e}", exc_info=True)
            raise e

        return TranscriptionResponse(resumo=resumo, transcricao=texto)
