import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable, tap, switchMap, finalize } from 'rxjs';
import { LoginRequest, LoginResponse, User } from '../types/User';
import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class LoginService {

  private apiUrl = `${environment.apiUrl}/auth/login`; // ajuste conforme sua API // ajuste conforme sua API

  constructor(private http: HttpClient) {}

 login(data: LoginRequest): Observable<LoginResponse> {
 
  return this.http.post<LoginResponse>(this.apiUrl, data, { withCredentials: true }).pipe(
    switchMap(() => {
      return this.http.get(`${environment.apiUrl}/auth/user`, { withCredentials: true });
    }),
    tap((user: any) => {
      localStorage.setItem('user', JSON.stringify(user));
    })
  );
}

  logout(): Observable<any> {
    // Adicionei { withCredentials: true } caso sua API precise validar o cookie antes de apagar
    return this.http.post(`${environment.apiUrl}/auth/logout`, {}, { withCredentials: true }).pipe(
      finalize(() => {
        // O finalize SEMPRE roda, tanto em caso de sucesso (next) quanto de erro (error)
        this.limparSessao();
      })
    );
  }

limparSessao() {
  localStorage.removeItem('user');
}

 isLoggedIn(): boolean {
    return !!localStorage.getItem('user');
  }

  getUser(): any {
    const user = localStorage.getItem('user');
    return user ? JSON.parse(user) : null;
  }
}
