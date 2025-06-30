import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable, tap } from 'rxjs';
import { LoginRequest, LoginResponse } from '../types/User';
import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class LoginService {

  private apiUrl = `${environment.apiUrl}/auth/login`; // ajuste conforme sua API // ajuste conforme sua API

  constructor(private http: HttpClient) {}

  login(data: LoginRequest): Observable<LoginResponse> {
    return this.http.post<LoginResponse>(this.apiUrl, data).pipe(
      tap((response: LoginResponse) => {
        localStorage.setItem('token', response.token);
        this.http.get(`${environment.apiUrl}/auth/user`, {
          headers: new HttpHeaders({
          }).set('Authorization', `Bearer ${response.token}`)
        }).subscribe((user: any) => {
          localStorage.setItem('user', JSON.stringify(user));
        });
      })
    );
  }

  logout() {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
  }

  isLoggedIn(): boolean {
    return !!localStorage.getItem('token');
  }

  getToken(): string | null {
    return localStorage.getItem('token');
  }

  getUser(): any {
    const user = localStorage.getItem('user');
    return user ? JSON.parse(user) : null;
  }
}
