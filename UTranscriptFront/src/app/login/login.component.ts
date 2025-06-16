import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { LoginService } from '../services/login.service';
import { LoginRequest } from '../types/User';

@Component({
  standalone: false,
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss'],
})
export class LoginComponent  implements OnInit {
  loginForm!: FormGroup;
  constructor(private fb: FormBuilder,  private loginService: LoginService,
    private router: Router) {}

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
          this.router.navigate(['/']); // redirecionar após login
        },
        error: (err) => {
          console.error('Erro ao logar', err);
          alert('Usuário ou senha inválidos');
        }
      });
    }

  }
}
