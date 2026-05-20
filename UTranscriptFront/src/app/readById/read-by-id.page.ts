import { Component, OnInit } from '@angular/core';
import { LoadingController, ToastController } from '@ionic/angular';
import { VideoAulaService } from '../services/video_aula.service';
import { Router } from '@angular/router';
import { Curso, Tema, Universidade, VideoAula } from '../types/VideoAula';
import { Location } from '@angular/common';

@Component({
  selector: 'app-read-by-id',
  templateUrl: './read-by-id.page.html',
  styleUrls: ['./read-by-id.page.scss'],
  standalone: false,
})
export class ReadByIdPage implements OnInit {
  videoAula: VideoAula | undefined;
  isCreator: boolean = false;
  Editable: boolean = false;
  cursos: Curso[] = [];
  universidades: Universidade[] = [];
  temasSugeridos: Tema[] = [];
  videoAulaOriginal: any = null;
  constructor(
    private videoAulaService: VideoAulaService,
    private toastController: ToastController,
    private router: Router,
    private loadingCtrl: LoadingController,
    private location: Location
  ) {}

  ngOnInit() {
    // This method can be used to fetch the video by ID if needed
    // For example, you can use the router to get the ID from the URL
    const id = this.router.url.split('/').pop();
    if (id) {
      this.videoAulaService.getVideoAulaById(+id).subscribe(
        (videoAula) => {
          // Handle the videoAula data here
          if (!videoAula) {
            this.presentToast('Vídeo não encontrado.', 'danger');
            return;
          }
          this.videoAula = videoAula;
          const user = JSON.parse(sessionStorage.getItem('user') || '{}');

          this.isCreator = user.id === videoAula?.usuario?.id;
          this.carregarDadosIniciais();
        },
        (error) => {
          this.presentToast('Erro ao carregar vídeo: ' + error.message);
        }
      );
    } else {
      this.presentToast('ID do vídeo não encontrado.');
    }
  }

  carregarDadosIniciais() {
    this.videoAulaService
      .getAllCursos()
      .subscribe((res) => (this.cursos = res));
    this.videoAulaService
      .getAllUniversidades()
      .subscribe((res) => (this.universidades = res));
    if (this.videoAula && this.videoAula.curso) {
      this.buscarTemasPorCurso(this.videoAula.curso);
    }
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

  onBack() {
    this.location.back();
  }

  editarVideo() {
    this.videoAulaOriginal = JSON.parse(JSON.stringify(this.videoAula)); // clona
    this.Editable = true;
  }

  async exportarParaPDF() {
    if (!this.videoAula) {
      this.presentToast('Vídeo não carregado.', 'danger');
      return;
    }
    if (
      this.videoAula.transcricoes?.status.descricao === 'Cancelado' ||
      this.videoAula.transcricoes?.status.descricao === 'Pendente' ||
      this.videoAula.transcricoes?.status.descricao === 'Em Andamento'
    ) {
      this.presentToast('Transcrição não disponível.', 'warning');
      return;
    }

    const loading = await this.loadingCtrl.create({
      message: 'Exportando arquivo...',
      spinner: 'crescent',
      backdropDismiss: false,
    });
    await loading.present();

    this.videoAulaService.exportarParaPDF(this.videoAula).subscribe({
      next: (blob) => {
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `${this.videoAula?.titulo}_transcricao.pdf`; // nome do arquivo
        a.click();
        window.URL.revokeObjectURL(url);
        loading.dismiss();
        this.presentToast('PDF baixado com sucesso!', 'success');
      },
      error: (err) => {
        console.error('Erro ao baixar PDF:', err);
        loading.dismiss();
        this.presentToast('Erro ao baixar PDF: ' + err.message, 'danger');
      },
    });
  }

  async deleteVideoAula() {
    if (!this.videoAula) {
      this.presentToast('Vídeo não carregado.', 'danger');
      return;
    }

    const loading = await this.loadingCtrl.create({
      message: 'Apagando vídeo...',
      spinner: 'crescent',
      backdropDismiss: false,
    });
    await loading.present();

    this.videoAulaService.deleteVideoAula(this.videoAula.id!).subscribe({
      next: () => {
        loading.dismiss();
        this.presentToast('Vídeo apagado com sucesso!', 'success');
        this.router.navigate(['/tabs/tab3']);
      },
      error: (err) => {
        console.error('Erro ao apagar vídeo:', err);
        loading.dismiss();
        this.presentToast('Erro ao apagar vídeo: ' + err.message, 'danger');
      },
    });
  }

  async salvarEdicao() {
    this.Editable = false;
    const loading = await this.loadingCtrl.create({
      message: 'Apagando vídeo...',
      spinner: 'crescent',
      backdropDismiss: false,
    });
    // await loading.present();

    console.log('Dados do vídeo:', this.videoAula);

    this.videoAulaService
      .updateVideoAula(this.videoAula!.id!, this.videoAula!)
      .subscribe({
        next: (videoAula) => {
          loading.dismiss();
          loading.dismiss();
          this.videoAula = videoAula;
          this.videoAulaOriginal = JSON.parse(JSON.stringify(videoAula));
          this.presentToast('Edição salva com sucesso!', 'success');
        },
        error: (err) => {
          loading.dismiss();
          console.error('Erro ao salvar edição:', err);
          this.presentToast('Erro ao salvar edição: ' + err.message, 'danger');
        },
      });
  }
}
