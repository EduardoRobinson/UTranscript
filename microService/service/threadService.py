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
    
    def transcrever_em_thread(self,id: int, file_path: str,llm: llmLoaded,auth_header: str):
        transcricao = Transcricao(llm)
        fake_upload = FakeUploadFile(file_path)
        try:
            result = asyncio.run(transcricao.transcrever(fake_upload))
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
            "transcricao": result.transcricao
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