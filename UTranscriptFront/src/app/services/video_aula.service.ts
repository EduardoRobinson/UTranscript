import { HttpClient } from "@angular/common/http";
import { Injectable } from "@angular/core";
import { environment } from "src/environments/environment";
import { Curso, FormVideoAula, Tema, Universidade, VideoAula } from "../types/VideoAula";
import { Observable } from "rxjs";

@Injectable({
  providedIn: 'root'
})

export class VideoAulaService {
   private apiUrl = environment.apiUrl;


    constructor(private http: HttpClient) {}

    createVideoAula(data:FormData):Observable<VideoAula>{
        console.log("Enviando dados para o backend:", data);
        return this.http.post<VideoAula>(`${this.apiUrl}/video-aula`, data);
    }

    getAllCursos():Observable<Curso[]> {
        return this.http.get<Curso[]>(`${this.apiUrl}/cursos`);
    }

    getAllUniversidades():Observable<Universidade[]> {
        return this.http.get<Universidade[]>(`${this.apiUrl}/universidades`);
    }

    buscarTemaPorCurso(id:number):Observable<Tema[]>{
        return this.http.get<Tema[]>(`${this.apiUrl}/temas/${id}`);
    }

    getAllVideoAulas(): Observable<VideoAula[]> {
        return this.http.get<VideoAula[]>(`${this.apiUrl}/video-aulas`);
    }

    getVideoAulaById(id: number): Observable<VideoAula> {
        return this.http.get<VideoAula>(`${this.apiUrl}/video-aula/${id}`);
    }

    getVideoAulasByUserId(): Observable<VideoAula[]> {
        return this.http.get<VideoAula[]>(`${this.apiUrl}/video-aulas/user`);
    }

    exportarParaPDF(videoAula: VideoAula): Observable<Blob> {
        return this.http.post(`${this.apiUrl}/video-aula/pdf`, videoAula, { responseType: 'blob' });
    }

    deleteVideoAula(id: number): Observable<void> {
        return this.http.delete<void>(`${this.apiUrl}/video-aula/${id}`);
    }

  }