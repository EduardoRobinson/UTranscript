export type FormVideoAula = {

  titulo: string;
  cursoId:number;
  professor:string;
  universidadeId:number;
  temasId: number[];
  data:Date;
}

export type Transcript = {
    id?: number;
    videoAulaId?: number;
    conteudo: string;
    dataCriacao: Date;
}

export type Universidade = {
    id?: number;
    nome: string;
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
    temasId: string[];
    data: Date;
    curso?: Curso;
    universidade?: Universidade;
    temas?: Tema[];
}

