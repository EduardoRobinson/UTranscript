import { Injectable, Injector } from '@angular/core';
import { HttpInterceptor, HttpRequest, HttpHandler, HttpEvent, HttpErrorResponse } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError } from 'rxjs/operators';
import { Router } from '@angular/router';
import { LoginService } from '../services/login.service';

@Injectable()
export class AuthInterceptor implements HttpInterceptor {

  // Injector evita dependência circular: LoginService usa HttpClient, que passa por este interceptor
  constructor(private router: Router, private injector: Injector) {}

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
          this.injector.get(LoginService).limparSessao();
          this.router.navigate(['/login']);
        }
        
        // Repassa o erro para frente caso o componente queira tratá-lo
        return throwError(() => error);
      })
    );
  }
}