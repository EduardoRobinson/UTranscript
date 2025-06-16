import { Injectable } from '@angular/core';
import { CanActivate, Router } from '@angular/router';

@Injectable({
  providedIn: 'root'
})
export class AuthGuard implements CanActivate {

  constructor(private router: Router) {}

  canActivate(): boolean {
    const isLoggedIn = !!localStorage.getItem('token'); // ou outro critério

    if (!isLoggedIn) {
      this.router.navigate(['/login']); // ou qualquer outra rota pública
      return false;
    }

    return true;
  }
}
