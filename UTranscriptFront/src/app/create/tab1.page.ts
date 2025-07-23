import { Component, OnInit } from '@angular/core';
import { Curso, FormVideoAula, Tema, Universidade } from '../types/VideoAula';
import { VideoAulaService } from '../services/video_aula.service';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { ToastController } from '@ionic/angular';
import { Router } from '@angular/router';

@Component({
  selector: 'app-tab1',
  templateUrl: 'tab1.page.html',
  styleUrls: ['tab1.page.scss'],
  standalone: false,
})
export class Tab1Page implements OnInit {
  formVideoAula!: FormGroup;

  cursos: Curso[] = [];
  universidades: Universidade[] = [];
  temasSugeridos: Tema[] = [];

  constructor(
    private videoAulaService: VideoAulaService,
    private fb: FormBuilder,
    private toastController: ToastController,
    private router: Router
  ) {}

  ngOnInit() {
    this.formVideoAula = this.fb.group({
      titulo: [null, Validators.required],
      cursoId: [null, Validators.required],
      professor: [null, Validators.required],
      universidadeId: [null, Validators.required],
      temaId: [null, Validators.required],
      data: [null],
    });
  }

  ionViewWillEnter() {
    this.carregarDadosIniciais();
  }

  carregarDadosIniciais() {
    this.videoAulaService
      .getAllCursos()
      .subscribe((res) => (this.cursos = res));
    this.videoAulaService
      .getAllUniversidades()
      .subscribe((res) => (this.universidades = res));
  }

  buscarTemasPorCurso(cursoSelecionado: Curso) {
    if (cursoSelecionado?.id) {
      this.videoAulaService
        .buscarTemaPorCurso(cursoSelecionado.id)
        .subscribe((res) => {
          this.temasSugeridos = res;
        });
    }
  }
  arquivoSelecionado: File | null = null;

  onFileSelected(event: Event): void {
    const input = event.target as HTMLInputElement;
    if (input.files && input.files.length > 0) {
      this.arquivoSelecionado = input.files[0];
      console.log('Arquivo selecionado:', this.arquivoSelecionado);
    }
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

  salvarVideoaula() {
    console.log('Dados do formulário:', this.formVideoAula.value);
    if (this.formVideoAula.invalid) {
      this.formVideoAula.markAllAsTouched();
      this.presentToast(
        'Por favor, preencha todos os campos obrigatórios.',
        'danger'
      );
      return;
    }

    this.formVideoAula.value.data = new Date().toISOString().split('T')[0];
    this.formVideoAula.value.cursoId = this.formVideoAula.value.cursoId.id;
    this.formVideoAula.value.universidadeId = this.formVideoAula.value.universidadeId.id;
    this.formVideoAula.value.temaId = this.formVideoAula.value.temaId.id;
    if (!this.arquivoSelecionado) {
      alert('Nenhum arquivo selecionado.');
      return;
    }

    const payload = { ...this.formVideoAula.value };
    console.log('Payload enviado:', payload);
    const formData = new FormData();
    formData.append('file', this.arquivoSelecionado);
    formData.append(
      'dados',
      new Blob([JSON.stringify(payload)], { type: 'application/json' })
    );
    console.log('FormData criado:', formData.get('dados'));
    
    this.videoAulaService.createVideoAula(formData).subscribe((res) => {
      if (res) {
        console.log('Videoaula criada com sucesso:', res);
        this.presentToast('Videoaula criada com sucesso!', 'success');
        this.formVideoAula.reset();
        this.arquivoSelecionado = null;
        this.router.navigate(['/tabs/tab3']); // Redireciona para a aba de videoaulas cadastradas
      } else {
        console.error('Erro ao criar videoaula:', res);
        this.presentToast(
          'Erro ao criar videoaula. Tente novamente.',
          'danger'
        );
      }
    });
    
  }
}
