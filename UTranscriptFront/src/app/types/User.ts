import { Curso, Universidade } from "./VideoAula";

export interface LoginRequest {
  email: string;
  senha: string;
}

export interface LoginResponse {
  token: string;
  user: User;
}

export interface User  {
    id: number;
    nome: string;
    email: string;
    curso?: Curso;
    universidade?: Universidade;
}

export interface RegisterRequest {
  nome: string;
  email: string;
  senha: string;
  universidade_id:number;
  curso_id:number;
}
export interface RegisterResponse {
  message: string;
  user: User;
}