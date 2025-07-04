
from dto.videoAulaDTO import VideoAulaDTO
from service.YoutubeService import YoutubeService
from service.TranscriptionService import Transcricao
from fastapi import APIRouter, Path,Request,File, UploadFile
from fastapi.responses import FileResponse
import os
from fastapi import Body

from service.pdfService import pdfService

router = APIRouter()

@router.get("/health")
async def health_check():
    """Endpoint de verificação de saúde."""
    return {"status": "ok"}

@router.post("/transcricao/{id}")
async def create_transcricao(
    id: int = Path(...),  # <- id vem da URL
    file: UploadFile = File(...)  # <- file vem do corpo (multipart)
):
    print(f"ID recebido: {id}")
    print(f"Nome do arquivo recebido: {file.filename}")
    # Aqui você processa o arquivo
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