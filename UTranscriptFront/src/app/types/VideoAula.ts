import { User } from "./User";

export type FormVideoAula = {

  titulo: string;
  cursoId:number;
  professor:string;
  universidadeId:number;
  temaId: number;
  data:Date;
}

export type StatusTranscription = {
    id?: number;
    descricao: string;
}

export type Transcript = {
    id?: number;
    conteudo: string;
    status: StatusTranscription;
}

export type Universidade = {
    id?: number;
    nome: string;
    sigla: string;
}

export type Curso = {
    id?: number;
    nome: string;
}

export type Tema = {
    id?: number;
    descricao: string;
    curso: Curso;
}

export type VideoAula = {
    id?: number;
    titulo: string;
    cursoId: number;
    universidadeId: number;
    temaId: number;
    professor: string;
    data: Date;
    curso?: Curso;
    universidade?: Universidade;
    tema?: Tema;
    transcricoes?: Transcript;
    icone?: string;
    corIcone?: string;
    usuario:User;
}

