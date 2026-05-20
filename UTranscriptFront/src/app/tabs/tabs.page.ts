import { Component } from '@angular/core';
import { LoginService } from '../services/login.service';
import { User } from '../types/User';
import { Router } from '@angular/router';

@Component({
  selector: 'app-tabs',
  templateUrl: 'tabs.page.html',
  styleUrls: ['tabs.page.scss'],
  standalone: false,
})
export class TabsPage {

  user:User | null = null;


  constructor(private loginService: LoginService,private router: Router) {
 
  }

  async ngOnInit() {
    this.user = await this.loginService.getUser();// Redireciona para a página inicial
  }

 


 logout() {
    this.loginService.logout().subscribe({
      next: () => {
        console.log('Logout com sucesso, redirecionando...');
        this.executarRedirecionamento();
      },
      error: (err: any) => {
        console.error('Erro na API de logout, mas limpamos o front mesmo assim. Redirecionando...', err);
        this.executarRedirecionamento();
      }
    });
  }

  private executarRedirecionamento() {
    this.router.navigate(['/login']);
  }

}
