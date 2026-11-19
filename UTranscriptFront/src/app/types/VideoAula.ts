import { User } from "./User";

export type FormVideoAula = {

  titulo: string;
  cursoId:number;
  professor:string;
  universidadeId:number;
  temaId: number;
  data:Date;
  promptPersonalizado?: string;
}

export type StatusTranscription = {
    id?: number;
    descricao: string;
}

export type Transcript = {
    id?: number;
    conteudo: string;
    status: StatusTranscription;
    tipoExtracao?: string;
    prompt?: string;
    promptPersonalizado?: string;
    statusAvaliacao?: string;
    avaliacao?: string;
}

export type AvaliacaoIniciada = {
    msg: string;
    id: number;
}

export type NotasAderencia = {
    adesao: number;
    fidelidade: number;
    cobertura: number;
    organizacao: number;
    nota: number;
    justificativa?: string;
}

export type AvaliacaoAderencia = {
    agregado: NotasAderencia;
    amostras: NotasAderencia[];
}

export type AvaliacaoAula = {
    aderencia: AvaliacaoAderencia;
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

