from dataclasses import dataclass, field
from typing import Optional
from datetime import date

@dataclass
class StatusTranscription:
    id: Optional[int] = None
    descricao: str = ""

@dataclass
class Transcript:
    id: Optional[int] = None
    conteudo: str = ""
    status: StatusTranscription = field(default_factory=StatusTranscription)

@dataclass
class Universidade:
    id: Optional[int] = None
    nome: str = ""
    sigla: str = ""

@dataclass
class Curso:
    id: Optional[int] = None
    nome: str = ""

@dataclass
class Tema:
    id: Optional[int] = None
    descricao: str = ""
    curso: Curso = field(default_factory=Curso)

@dataclass
class VideoAula:
    id: Optional[int] = None
    titulo: str = ""
    cursoId: int = 0
    universidadeId: int = 0
    temaId: int = 0
    professor: str = ""
    data: date = field(default_factory=date.today)
    curso: Optional[Curso] = None
    universidade: Optional[Universidade] = None
    tema: Optional[Tema] = None
    transcricoes: Optional[Transcript] = None
    icone: Optional[str] = None
    corIcone: Optional[str] = None
