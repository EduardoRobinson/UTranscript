
from service.YoutubeService import YoutubeService
from service.TranscriptionService import Transcricao
from fastapi import APIRouter,Request,File, UploadFile
from fastapi.responses import FileResponse
import os
from fastapi import Body

router = APIRouter()

@router.get("/health")
async def health_check():
    """Endpoint de verificação de saúde."""
    return {"status": "ok"}

@router.post("/transcricao")
async def create_transcricao(file:UploadFile=File(...)):
    transcricao=Transcricao()
    return await transcricao.transcrever2(file)


@router.get("/meeting_pdf")
def create_pdf(transcricao: Request):
    file_path = os.path.abspath("app/resumes/out.pdf")
    if os.path.exists(file_path):
        os.remove(file_path)
    transcricao = Transcricao()
    transcricao.gerar_pdf(id)
    return FileResponse(
        "resumes/out.pdf",
        media_type="application/pdf",
        filename="meeting_summary.pdf",
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