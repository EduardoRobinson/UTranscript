import { Injectable } from '@angular/core';
import { CanActivate, Router } from '@angular/router';
import { LoginService } from '../services/login.service';

@Injectable({
  providedIn: 'root'
})
export class AuthGuard implements CanActivate {

  constructor(private router: Router,private loginService: LoginService) {}

  canActivate(): boolean {
    const isLoggedIn = this.loginService.isLoggedIn(); // ou outro critério

    if (!isLoggedIn) {
      this.router.navigate(['/login']); // ou qualquer outra rota pública
      return false;
    }

    return true;
  }
}
