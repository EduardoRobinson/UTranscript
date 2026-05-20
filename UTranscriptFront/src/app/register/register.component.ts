import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { ToastController } from '@ionic/angular';
import { RegisterService } from '../services/register.service';
import { Router } from '@angular/router';
import { RegisterRequest } from '../types/User';
import { VideoAulaService } from '../services/video_aula.service';
import { Curso, Universidade } from '../types/VideoAula';

@Component({
  standalone: false,
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.scss'],
})
export class RegisterComponent implements OnInit {
  cadastroForm: FormGroup;
  cursos: Curso[] = [];
  universidades: Universidade[] = [];

  constructor(
    private fb: FormBuilder,
    private toastController: ToastController,
    private registerService: RegisterService,
    private router: Router,
    private videoAulaService: VideoAulaService,
  ) {
    this.cadastroForm = this.fb.group({
      nome: ['', Validators.required],
      email: ['', [Validators.required, Validators.email]],
      senha: ['', [Validators.required, Validators.minLength(6)]],
      universidade_id: [null, Validators.required],
      curso_id: [null, Validators.required],
    });
  }
  ngOnInit() {
    this.carregarDadosIniciais();
  }



  carregarDadosIniciais() {
    this.registerService
      .getAllCursos()
      .subscribe((res) => (this.cursos = res));
    this.registerService
      .getAllUniversidades()
      .subscribe((res) => (this.universidades = res));
      console.log(this.cursos);
      console.log(this.universidades);
  }

  async onSubmit() {
    if (this.cadastroForm.invalid) {
      this.showToast('Preencha todos os campos corretamente!');
      return;
    }
    this.cadastroForm.value.curso_id = this.cadastroForm.value.curso_id.id;
    this.cadastroForm.value.universidade_id = this.cadastroForm.value.universidade_id.id;

    const registerData: RegisterRequest = this.cadastroForm.value;

    this.registerService.register(registerData).subscribe({
      next: () => {
        this.showToast('Cadastro realizado com sucesso!');
        this.cadastroForm.reset();
        this.router.navigate(['/login']); // redirecionar após login
      },
      error: (err: unknown) => {
        if (typeof err === 'object' && err !== null && 'error' in err) {
          const apiErr = err as { error: any };
          this.showToast(apiErr.error.message || 'Erro desconhecido');
        } else {
          this.showToast('Erro ao cadastrar usuário');
        }
      },
    });
  }

  async showToast(message: string) {
    const toast = await this.toastController.create({
      message,
      duration: 2000,
      color: 'primary',
    });
    toast.present();
  }
}
