import { Component } from '@angular/core';
import { Curso, FormVideoAula, Tema, Universidade } from '../types/VideoAula';
import { VideoAulaService } from '../services/video_aula.service';

@Component({
  selector: 'app-tab1',
  templateUrl: 'tab1.page.html',
  styleUrls: ['tab1.page.scss'],
  standalone: false,
})
export class Tab1Page {
  form: FormVideoAula = {
    titulo: '',
    cursoId: 0,
    universidadeId: 0,
    temasId: [],
    data: new Date(),
    professor: '',
  };

  cursos: Curso[] = [];
  universidades: Universidade[] = [];
  temasSugeridos: Tema[] = [];

  constructor(private videoAulaService: VideoAulaService) {}

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

  buscarTemasPorCurso() {
    const id = this.form.cursoId;
    if (id) {
      this.videoAulaService.buscarTemaPorCurso(id).subscribe((res) => {
        this.temasSugeridos = res;
      });
    }
  }

  salvarVideoaula() {
    console.log('Form a ser enviado:', this.form);
    this.videoAulaService.createVideoAula(this.form).subscribe((res) => {
      console.log('Videoaula salva com sucesso:', res);
    });
  }
}
