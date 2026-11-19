import asyncio
from threading import Thread
import os
from models import llmLoaded
from service.TranscriptionService import Transcricao
import requests
import dotenv

dotenv.load_dotenv()

class FakeUploadFile:
    """Simula um UploadFile assíncrono para uso posterior em thread."""
    def __init__(self, file_path):
        self.file_path = file_path

    async def read(self):
        with open(self.file_path, "rb") as f:
            return f.read()

class ThreadService:
    def __init__(self):
        pass

    @staticmethod
    def run_in_thread(target, *args):
        """
        Run a function in a separate thread.
        """
        thread = Thread(target=target, args=args)
        thread.start()
        return thread   
    
    def _headers(self, auth_header: str):
        token = auth_header[len("Bearer "):] if auth_header and auth_header.startswith("Bearer ") else (auth_header or "")
        return {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
        }

    def _salvar_prompt(self, id: int, auth_header: str, prompt_completo: str):
        spring_url = os.getenv("SPRING_API_URL") + f"/transcription/{id}/prompt"
        response = requests.put(
            spring_url,
            json={"prompt": prompt_completo},
            headers=self._headers(auth_header),
        )
        print(f"[{id}] Prompt salvo antes do resumo: {response.status_code}")

    def transcrever_em_thread(self,id: int, file_path: str,llm: llmLoaded,auth_header: str, prompt: str = None):
        transcricao = Transcricao(llm)
        fake_upload = FakeUploadFile(file_path)
        try:
            texto = asyncio.run(transcricao.transcrever(fake_upload))
            prompt_completo = transcricao._prompt_utilizado(texto, prompt)
            try:
                self._salvar_prompt(id, auth_header, prompt_completo)
            except Exception as prompt_erro:
                print(f"[{id}] Falha ao salvar o prompt antes do resumo: {prompt_erro}")
            result = asyncio.run(transcricao.gerar_resumo(texto, prompt))
            spring_url = os.getenv("SPRING_API_URL") + f"/transcription/{id}"
            if auth_header.startswith("Bearer "):
                token = auth_header[len("Bearer "):]
            else:
                token = auth_header

            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}"
            }
            payload = {
            "resumo": result.resumo,
            "transcricao": result.transcricao,
            "prompt": result.prompt,
            }
            response = requests.put(
                spring_url,
                json=payload,  # conteúdo textual direto
                headers=headers  # importante isso aqui!
            )
            print(f"[{id}] Status da requisição: {response.status_code}")
        except Exception as e:
            spring_url = os.getenv("SPRING_API_URL") + f"/transcription/{id}"
            if auth_header.startswith("Bearer "):
                token = auth_header[len("Bearer "):]
            else:
                token = auth_header

            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}"
            }
            payload = {
            "resumo": '',
            "transcricao": ''
            }
            response = requests.put(
                spring_url,
                json=payload,  # conteúdo textual direto
                headers=headers  # importante isso aqui!
            )
            print(f"[{id}] Erro na transcrição: {e}")
        finally:
            os.remove(file_path)

    def avaliar_em_thread(self, id: int, pedido, auth_header: str, avaliacao_service):
        spring_url = os.getenv("SPRING_API_URL") + f"/transcription/{id}/avaliacao"
        token = auth_header[len("Bearer "):] if auth_header and auth_header.startswith("Bearer ") else (auth_header or "")
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
        }
        try:
            resultado = avaliacao_service.avaliar(pedido)
            response = requests.put(spring_url, json=resultado, headers=headers)
            print(f"[{id}] Status da avaliação: {response.status_code}")
        except Exception as e:
            print(f"[{id}] Erro na avaliação: {e}")
            try:
                response = requests.put(spring_url, json={"erro": str(e)}, headers=headers)
                print(f"[{id}] Status do erro da avaliação: {response.status_code}")
            except Exception as callback_erro:
                print(f"[{id}] Falha ao registrar o erro da avaliação: {callback_erro}")