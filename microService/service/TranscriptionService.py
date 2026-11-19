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
        self.llm = llm
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

        return texto

    def _montar_messages(self, texto, prompt_personalizado):
        if prompt_personalizado and prompt_personalizado.strip():
            return [
                {
                    "role": "system",
                    "content": (
                        "Você extrai informações da transcrição seguindo exatamente a instrução do usuário. "
                        "Não invente conteúdo que não esteja na transcrição. "
                        "Responda somente com o resultado da extração."
                    )
                },
                {
                    "role": "user",
                    "content": f"{prompt_personalizado.strip()}\n\nTranscrição:\n{texto}"
                },
            ]

        return [
            {
                "role": "system", 
                "content": (
                    "Você é um assistente acadêmico especializado em síntese de conteúdo. "
                    "Otimize a resposta para um texto curto. "
                    "Quando houver exercício, priorize a resolução: enunciado, passos e resultado, e reduza a explicação ao mínimo necessário para entender o passo. "
                    "Para cada tema central, registre o conceito em uma frase e, quando houver, o exemplo usado. "
                    "Relacione os temas entre si só quando isso for indispensável para a resolução. "
                    "Use linguagem formal e organize o texto em seções. "
                    "Não invente conteúdo que não esteja na transcrição, com uma única exceção: exercícios. "
                    "Se o professor enunciou um exercício ou exemplo e não o resolveu, resolva o enunciado com base no próprio enunciado e no conhecimento do tema, e inclua a resolução no resumo. "
                    "Se a resolução foi falada, mas a transcrição está incompleta ou ilegível a ponto de não recuperar os passos, reconstrua a resolução a partir do enunciado. "
                    "Coloque essa resolução em uma subseção intitulada Resolução complementar, deixando explícito que ela não foi concluída pelo professor na aula e foi elaborada pelo sistema. "
                    "Mantenha o enunciado original da aula. Fora desses exercícios, não acrescente nada que não esteja na transcrição. "
                    "Não adicione avisos de tradução, notas de revisão ou repetições ao final."
                )
            },
            {
                "role": "user", 
                "content": (
                    "Transforme esta transcrição em um resumo curto, sem caracteres especiais. "
                    "Priorize as resoluções dos exercícios e encurte as explicações textuais. "
                    "Se houver exercício de exemplo sem resolução, ou com resolução ilegível na transcrição, "
                    "inclua enunciado, passos e resultado na subseção Resolução complementar, marcada como elaborada pelo sistema:\n\n"
                    f"{texto}"
                )
            },
        ]

    def _prompt_utilizado(self, texto, prompt_personalizado):
        messages = self._montar_messages(texto, prompt_personalizado)
        partes = [message["content"].strip() for message in messages]
        return "\n\n".join(parte for parte in partes if parte)

    # Seu arquivo de Transcricao
    async def gerar_resumo(self, texto, prompt_personalizado=None):
        total_etapas = 2
        etapa = 1

        self.log_progresso(etapa, total_etapas, "Montando prompt estruturado...")

        messages = self._montar_messages(texto, prompt_personalizado)

        prompt = self.llm_pipeline.tokenizer.apply_chat_template(
            messages, 
            tokenize=False, 
            add_generation_prompt=True
        )

        etapa += 1
        self.log_progresso(etapa, total_etapas, "Gerando resumo sem repetições...")

        try:
            with self.llm.geracao_lock:
                output = self.llm_pipeline(
                    prompt,
                    max_new_tokens=1024,
                    do_sample=True,
                    temperature=0.6,
                    top_p=0.9,
                    repetition_penalty=1.15,
                    eos_token_id=[
                        self.llm_pipeline.tokenizer.eos_token_id,
                        self.llm_pipeline.tokenizer.convert_tokens_to_ids("<|eot_id|>")
                    ]
                )
            
            resposta_completa = output[0]["generated_text"]
            resumo = resposta_completa[len(prompt):].strip()
            logger.info("Resumo gerado com sucesso.")
        except Exception as e:
            logger.error(f"Erro ao gerar resumo: {e}", exc_info=True)
            raise e

        return TranscriptionResponse(
            resumo=resumo,
            transcricao=texto,
            prompt=self._prompt_utilizado(texto, prompt_personalizado),
        )
