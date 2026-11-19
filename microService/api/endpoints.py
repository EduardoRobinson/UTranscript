
import asyncio
import shutil
import tempfile
from threading import Thread
from dto.videoAulaDTO import VideoAulaDTO
from models.llmLoaded import llmLoaded
from service.YoutubeService import YoutubeService
from service.TranscriptionService import Transcricao
from fastapi import APIRouter, Path,Request,File, UploadFile, Form
from fastapi.responses import FileResponse, JSONResponse
import os
from fastapi import Body,Request
from service.threadService import ThreadService
from service.EvaluationService import EvaluationService
from dto.avaliacaoDTO import AvaliacaoRequest

from service.pdfService import pdfService

avaliacao_service = EvaluationService()

router = APIRouter()


@router.get("/health")
async def health_check(request: Request):
    """Endpoint de verificação de saúde dos três modelos."""
    llm = getattr(request.app.state, "llm", None)
    juiz = getattr(request.app.state, "juiz", None)
    modelos = {
        "llama": llm is not None and getattr(llm, "llm_pipeline", None) is not None,
        "whisper": llm is not None and getattr(llm, "transcribe_model", None) is not None,
        "qwen": juiz is not None and getattr(juiz, "model", None) is not None,
    }
    pronto = all(modelos.values())
    corpo = {"status": "ok" if pronto else "indisponivel", "modelos": modelos}
    if not pronto:
        return JSONResponse(status_code=503, content=corpo)
    return corpo

@router.post("/transcricao/{id}")
async def create_transcricao(
    request: Request,
    id: int = Path(...), 
    file: UploadFile = File(...) ,
    prompt: str | None = Form(default=None),
):
    print(f"ID recebido: {id}")
    auth_header = request.headers.get("authorization") 
    print(f"Nome do arquivo recebido: {file.filename}")
    prompt_personalizado = prompt.strip() if prompt and prompt.strip() else None
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp:
        shutil.copyfileobj(file.file, temp)
        temp_path = temp.name
    llm = request.app.state.llm
    service = ThreadService()
    thread = Thread(target=service.transcrever_em_thread, args=(id, temp_path,llm,auth_header, prompt_personalizado))
    thread.start()
    
    return {"msg": "Recebido com sucesso", "id": id, "filename": file.filename}


@router.post("/avaliar/{id}")
def avaliar(id: int, pedido: AvaliacaoRequest, request: Request):
    """Aceita a avaliação e devolve a resposta antes do cálculo terminar."""
    auth_header = request.headers.get("authorization") or ""
    service = ThreadService()
    thread = Thread(
        target=service.avaliar_em_thread,
        args=(id, pedido, auth_header, avaliacao_service),
    )
    thread.start()
    return {"msg": "Recebido com sucesso", "id": id}


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
    
    # 🔥 Apontando para o volume compartilhado do Docker
    pasta = "shared-files"
    
    # Garante que a pasta existe
    if not os.path.exists(pasta):
        os.makedirs(pasta)
        print(f'Pasta criada: {pasta}')
    
    # Limpa os arquivos antigos (o 'else' foi removido para evitar falsos positivos)
    for arquivo in os.listdir(pasta):
        caminho_arquivo = os.path.join(pasta, arquivo)
        if os.path.isfile(caminho_arquivo):
            try:
                os.remove(caminho_arquivo)
                print(f'Deletado: {caminho_arquivo}')
            except Exception as e:
                print(f'Erro ao deletar {caminho_arquivo}: {e}')
                
    # Inicializa o serviço e inicia o download
    download = YoutubeService(video_url)
    return download.baixar_video()