import { HttpClient } from "@angular/common/http";
import { Injectable } from "@angular/core";
import { environment } from "src/environments/environment";
import { Curso, FormVideoAula, Tema, Universidade } from "../types/VideoAula";
import { Observable } from "rxjs";

@Injectable({
  providedIn: 'root'
})

export class VideoAulaService {
   private apiUrl = environment.apiUrl;


    constructor(private http: HttpClient) {}

    createVideoAula(data:FormVideoAula){
        return this.http.post<FormVideoAula>(`${this.apiUrl}/video-aula`, data);
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


  }