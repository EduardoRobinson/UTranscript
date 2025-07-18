import tempfile
import os
from faster_whisper import WhisperModel
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from models.llmLoaded import llmLoaded
from models.transcriptionType import TranscriptionResponse
import torch
import gc

class Transcricao:
    def __init__(self,llm: llmLoaded):
        self.llm_pipeline = llm.llm_pipeline
        self.transcribe_model = llm.transcribe_model   

    async def transcrever(self, arquivo):
        """Transcreve um áudio e retorna texto bruto."""
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
            temp_file.write(await arquivo.read())
            temp_path = temp_file.name

        print(f"📁 Áudio salvo em: {temp_path}")

        try:
            segments, _ = self.transcribe_model.transcribe(temp_path)
            texto = " ".join([seg.text for seg in segments])
        except Exception as e:
            print(f"❌ Erro ao transcrever áudio: {e}")
            raise e 
        finally:
            os.remove(temp_path)

        print("✅ Transcrição concluída.")
        return await self.gerar_resumo(texto)

    async def gerar_resumo(self, texto):
        """Gera resumo com modelo local."""
        print("🧠 Gerando resumo...")

        prompt = (
        f"Resuma a transcrição abaixo feita da video aula como se fosse um relatório ,sem caracteres especiais , e com os temas abordados e trazendo da literatura da area referências quando possível:\n"
        f"{texto}\nResumo:"
         )

        
        output = self.llm_pipeline(prompt, do_sample=True, temperature=0.7,max_new_tokens=2048,truncation=True )
        resposta_completa = output[0]["generated_text"]
        if resposta_completa.startswith(prompt):
            resumo = resposta_completa[len(prompt):].strip()
        else:
            resumo = resposta_completa.strip()
        transcription=TranscriptionResponse(resumo=resumo,transcricao=texto)
        print("✅ Resumo gerado.")
        return transcription
