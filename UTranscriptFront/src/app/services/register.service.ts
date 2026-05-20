import { HttpClient } from "@angular/common/http";
import { environment } from "src/environments/environment";
import { RegisterRequest, RegisterResponse } from "../types/User";
import { Observable } from "rxjs";
import { Injectable } from "@angular/core";
import { Curso, Universidade } from "../types/VideoAula";


@Injectable({
  providedIn: 'root'
})

export class RegisterService{
  private apiUrl = `${environment.apiUrl}/auth`; // ajuste conforme sua API // ajuste conforme sua API

  constructor(private http: HttpClient) {}

  register(data:RegisterRequest): Observable<RegisterResponse> {
    return this.http.post<RegisterResponse>(`${this.apiUrl}/registrar`, data);
  }

   getAllCursos():Observable<Curso[]> {
          return this.http.get<Curso[]>(`${this.apiUrl}/cursos`);
      }
  
      getAllUniversidades():Observable<Universidade[]> {
          return this.http.get<Universidade[]>(`${this.apiUrl}/universidades`);
      }
}