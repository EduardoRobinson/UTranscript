import { Component } from '@angular/core';
import { LoginService } from '../services/login.service';

@Component({
  selector: 'app-tabs',
  templateUrl: 'tabs.page.html',
  styleUrls: ['tabs.page.scss'],
  standalone: false,
})
export class TabsPage {

  constructor(private loginService: LoginService) {}


  logout() {
    try {
      this.loginService.logout();
      window.location.href = '/login'; // ou use o Router para redirecionar
    } catch (err) {
      console.error('Erro ao deslogar', err);
      alert('Erro ao deslogar. Tente novamente.');
    }
  }

}
