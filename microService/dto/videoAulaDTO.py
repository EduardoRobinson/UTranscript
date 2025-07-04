from pydantic import BaseModel
from typing import Optional
from datetime import date


class StatusTranscriptionDTO(BaseModel):
    id: Optional[int]
    descricao: str
    
    
class TranscriptDTO(BaseModel):
    id: Optional[int]
    conteudo: str
    status: StatusTranscriptionDTO
    
    
class UniversidadeDTO(BaseModel):
    id: Optional[int]
    nome: str
    sigla: str
    
class CursoDTO(BaseModel):
    id: Optional[int]
    nome: str

class TemaDTO(BaseModel):
    id: Optional[int]
    descricao: str
    curso: CursoDTO

class VideoAulaDTO(BaseModel):
    id: Optional[int]
    titulo: str
    professor: str
    data: list
    curso: Optional[CursoDTO] = None
    universidade: Optional[UniversidadeDTO] = None
    tema: Optional[TemaDTO] = None
    transcricoes: Optional[TranscriptDTO] = None

