import { HttpClient } from "@angular/common/http";
import { environment } from "src/environments/environment";
import { RegisterRequest, RegisterResponse } from "../types/User";
import { Observable } from "rxjs";
import { Injectable } from "@angular/core";


@Injectable({
  providedIn: 'root'
})

export class RegisterService{
  private apiUrl = `${environment.apiUrl}/auth/registrar`; // ajuste conforme sua API // ajuste conforme sua API

  constructor(private http: HttpClient) {}

  register(data:RegisterRequest): Observable<RegisterResponse> {
    return this.http.post<RegisterResponse>(this.apiUrl, data);
  }
}