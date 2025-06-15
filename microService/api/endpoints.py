
from service.TranscriptionService import Transcricao
from fastapi import APIRouter,Request,File, UploadFile
from fastapi.responses import FileResponse
import os

router = APIRouter()

@router.get("/health")
async def health_check():
    """Endpoint de verificação de saúde."""
    return {"status": "ok"}

@router.post("/transcricao")
async def create_transcricao(file:UploadFile=File(...)):
    transcricao=Transcricao()
    return await transcricao.transcrever2(file)


@router.get("/meeting_pdf/")
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