import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { LoginService } from '../services/login.service';
import { LoginRequest } from '../types/User';
import { ToastController } from '@ionic/angular';

@Component({
  standalone: false,
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss'],
})
export class LoginComponent  implements OnInit {
  loginForm!: FormGroup;
  constructor(private fb: FormBuilder,  private loginService: LoginService,
    private router: Router,private toastController: ToastController) {}

  ngOnInit() {
      this.loginForm = this.fb.group({
      email: ['', [Validators.required, Validators.email]],
      senha: ['', Validators.required]
    });
  }


  onLogin(){
  if (this.loginForm.valid) {
      const credentials: LoginRequest = this.loginForm.value;

      this.loginService.login(credentials).subscribe({
        next: () => {
          this.presentToast('Login realizado com sucesso!', 'success');
          this.router.navigate(['/']); // redirecionar após login
        },
        error: (err) => {
          console.error('Erro ao logar', err);
          if (typeof err === 'object' && err !== null && 'error' in err) {
            const apiErr = err as { error: any };
            this.presentToast(apiErr.error.message || 'Erro desconhecido', 'danger');
          } else {
            this.presentToast('Erro ao realizar login', 'danger');
          }
        }
      });
    }

  }

  navigateToRegister(){
  setTimeout(() => {
    this.router.navigate(['/register']);
  }, 0);
  }

    async presentToast(
    message: string,
    color: 'success' | 'danger' | 'warning' = 'success'
  ) {
    const toast = await this.toastController.create({
      message,
      duration: 3000,
      position: 'bottom',
      color,
    });
    await toast.present();
  }

}
