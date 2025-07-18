
import asyncio
import shutil
import tempfile
from threading import Thread
from dto.videoAulaDTO import VideoAulaDTO
from models.llmLoaded import llmLoaded
from service.YoutubeService import YoutubeService
from service.TranscriptionService import Transcricao
from fastapi import APIRouter, Path,Request,File, UploadFile
from fastapi.responses import FileResponse
import os
from fastapi import Body,Request
from service.threadService import ThreadService

from service.pdfService import pdfService

router = APIRouter()


@router.get("/health")
async def health_check():
    """Endpoint de verificação de saúde."""
    return {"status": "ok"}

@router.post("/transcricao/{id}")
async def create_transcricao(
    request: Request,
    id: int = Path(...), 
    file: UploadFile = File(...) ,
):
    print(f"ID recebido: {id}")
    auth_header = request.headers.get("authorization") 
    print(f"Nome do arquivo recebido: {file.filename}")
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp:
        shutil.copyfileobj(file.file, temp)
        temp_path = temp.name
    llm = request.app.state.llm
    service = ThreadService()
    thread = Thread(target=service.transcrever_em_thread, args=(id, temp_path,llm,auth_header))
    thread.start()
    
    return {"msg": "Recebido com sucesso", "id": id, "filename": file.filename}


@router.post("/videoAula_pdf")
def create_pdf(videoAula:VideoAulaDTO):
    file_path = os.path.abspath("app/resumes/out.pdf")
    if os.path.exists(file_path):
        os.remove(file_path)
    pdf = pdfService()
    pdf.gerar_pdf(videoAula)
    return FileResponse(
        "resumes/out.pdf",
        media_type="application/pdf",
        filename="videoAula_transcription.pdf",
    )


@router.post("/youtube_download")
async def youtube_download(data: dict = Body(...)):
    video_url = data.get("video_url")
    if not video_url:
        return {"error": "Parâmetro 'video_url' é obrigatório."}
    pasta = "downloads"
    if not os.path.exists(pasta):
        os.makedirs(pasta)
        print(f'Pasta criada: {pasta}')
    if os.path.exists(pasta):
        for arquivo in os.listdir(pasta):
            caminho_arquivo = os.path.join(pasta, arquivo)
            if os.path.isfile(caminho_arquivo):
                os.remove(caminho_arquivo)
                print(f'Deletado: {caminho_arquivo}')
        else:
            print('Pasta não encontrada.')
    download = YoutubeService(video_url)
    return download.baixar_video()