import { Injectable } from '@angular/core';
import { HttpInterceptor, HttpRequest, HttpHandler, HttpEvent, HttpErrorResponse } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError } from 'rxjs/operators';
import { Router } from '@angular/router';

@Injectable()
export class AuthInterceptor implements HttpInterceptor {

  // Injetamos o Router para poder redirecionar o usuário caso o cookie expire
  constructor(private router: Router) {}

  intercept(req: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
    
    // 1. Clona a requisição adicionando a permissão para enviar Cookies em TODAS as chamadas
    const authReq = req.clone({
      withCredentials: true 
    });

    // 2. Envia a requisição e intercepta possíveis erros de volta
    return next.handle(authReq).pipe(
      catchError((error: HttpErrorResponse) => {
        
        // Se o Spring Boot retornar 401 (Unauthorized), o cookie expirou ou é inválido
        if (error.status === 401) {
          sessionStorage.removeItem('user'); // Remove o usuário "falso" logado no front
          this.router.navigate(['/login']);  // Joga de volta para o login
        }
        
        // Repassa o erro para frente caso o componente queira tratá-lo
        return throwError(() => error);
      })
    );
  }
}