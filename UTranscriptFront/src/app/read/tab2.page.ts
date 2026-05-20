import { Component, OnInit } from '@angular/core';
import { Curso, Tema, Universidade, VideoAula } from '../types/VideoAula';
import { VideoAulaService } from '../services/video_aula.service';
import { ToastController } from '@ionic/angular';
import { Router } from '@angular/router';

@Component({
  selector: 'app-tab2',
  templateUrl: 'tab2.page.html',
  styleUrls: ['tab2.page.scss'],
  standalone: false,
})
export class Tab2Page {
  busca: string = '';
  filtroUniversidade: string = '';
  filtroCurso: string = '';
  filtroTema: string = '';

  universidades: Universidade[] = [];
  cursos: Curso[] = [];
  temas: Tema[] = [];

  videoAulas: VideoAula[] = [];
  videoAulasFiltradas: VideoAula[] = [];

  isHovered: number | undefined = undefined;

  constructor(
    private videoAulaService: VideoAulaService,
    private toastController: ToastController,
    private router: Router  
  ) {
    this.carregarVideoAulas();
  }

  ionViewWillEnter() {
    this.carregarVideoAulas();
  }

  filtrarVideoAulas() {
    this.videoAulasFiltradas = this.videoAulas.filter((v) => {
      const tituloMatch = v.titulo
        .toLowerCase()
        .includes(this.busca.toLowerCase());
      const uniMatch = this.filtroUniversidade
        ? v.universidade?.nome === this.filtroUniversidade
        : true;
      const cursoMatch = this.filtroCurso
        ? v.curso?.nome === this.filtroCurso
        : true;
      const temaMatch = this.filtroTema
        ? v.tema?.descricao === this.filtroTema
        : true;

      return tituloMatch && uniMatch && cursoMatch && temaMatch;
    });
  }

  carregarUniversidades() {
    this.videoAulas.map((videoAula) => {
      if (videoAula.universidade) {
        this.universidades.push(videoAula.universidade);
      }
    });
    this.universidades = Array.from(
      new Set(this.universidades.map((u) => u.nome))
    )
      .map((nome) => this.universidades.find((u) => u.nome === nome)!)
      .sort((a, b) => a.nome.localeCompare(b.nome));
  }

  carregarCursos() {
    this.videoAulas.map((videoAula) => {
      if (videoAula.curso) {
        this.cursos.push(videoAula.curso);
      }
    });
    this.cursos = Array.from(new Set(this.cursos.map((c) => c.nome)))
      .map((nome) => this.cursos.find((c) => c.nome === nome)!)
      .sort((a, b) => a.nome.localeCompare(b.nome));
  }

  carregarTemas() {
    this.videoAulas.map((videoAula) => {
      if (videoAula.tema) {
        this.temas.push(videoAula.tema);
      }
    });
    this.temas = Array.from(new Set(this.temas.map((t) => t.descricao)))
      .map((descricao) => this.temas.find((t) => t.descricao === descricao)!)
      .sort((a, b) => a.descricao.localeCompare(b.descricao));
  }

  carregarVideoAulas() {
    this.videoAulaService.getAllVideoAulas().subscribe({
      next: (res) => {
        this.videoAulas = res;
        this.videoAulasFiltradas = res;
        console.log('Video aulas carregadas:', this.videoAulas);
        this.carregarUniversidades();
        this.carregarCursos();
        this.carregarTemas();
        this.videoAulas.map((videoAula) => {
          videoAula.icone = this.carregarIconsStatus(
            videoAula.transcricoes?.status?.descricao || 'Pendente'
          );
          videoAula.corIcone = this.carregarIconsStatusColor(
            videoAula.transcricoes?.status?.descricao || 'Pendente'
          );
        });
      },
      error: (err) => {
        console.error('Erro ao carregar video aulas:', err);
        this.presentToast('Erro ao carregar video aulas', 'danger');
      },
    });
  }

  carregarIconsStatusColor(status: string): string {
    switch (status) {
      case 'Pendente':
        return 'warning';
      case 'Em Andamento':
        return 'primary';
      case 'Concluído':
        return 'success';
      case 'Cancelado':
        return 'danger';
    }
    return 'medium'; // Default color
  }

  carregarIconsStatus(status: string): string {
    switch (status) {
      case 'Pendente':
        return 'hourglass';
      case 'Em Andamento':
        return 'create';
      case 'Concluído':
        return 'checkmark-circle';
      case 'Cancelado':
        return 'close-circle';
    }
    return 'help-circle';
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

  abrirVideoAula(id?: number) {
    this.router.navigate(['/videoaula', id]);
  }
}
