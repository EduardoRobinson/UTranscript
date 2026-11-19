import { Component, OnDestroy, OnInit } from '@angular/core';
import { LoadingController, ToastController } from '@ionic/angular';
import { VideoAulaService } from '../services/video_aula.service';
import { LoginService } from '../services/login.service';
import { Router } from '@angular/router';
import { Curso, Tema, Universidade, VideoAula, AvaliacaoAula } from '../types/VideoAula';
import { Location } from '@angular/common';

@Component({
  selector: 'app-read-by-id',
  templateUrl: './read-by-id.page.html',
  styleUrls: ['./read-by-id.page.scss'],
  standalone: false,
})
export class ReadByIdPage implements OnInit, OnDestroy {
  videoAula: VideoAula | undefined;
  isCreator: boolean = false;
  Editable: boolean = false;
  cursos: Curso[] = [];
  universidades: Universidade[] = [];
  temasSugeridos: Tema[] = [];
  videoAulaOriginal: any = null;
  avaliacao: AvaliacaoAula | null = null;
  private acompanhamento: ReturnType<typeof setInterval> | null = null;
  constructor(
    private videoAulaService: VideoAulaService,
    private loginService: LoginService,
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
          this.aplicarAvaliacaoSalva();
          const user = this.loginService.getUser() || {};

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

  ngOnDestroy() {
    this.pararAcompanhamento();
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

  transcricaoPronta(): boolean {
    const transcricao = this.videoAula?.transcricoes;
    return transcricao?.status?.descricao === 'Concluído'
      && !!transcricao.prompt?.trim()
      && !!transcricao.conteudo?.trim();
  }

  async avaliarResumo() {
    if (!this.videoAula?.id) {
      this.presentToast('Vídeo não carregado.', 'danger');
      return;
    }
    if (!this.transcricaoPronta()) {
      this.presentToast('A transcrição precisa estar concluída, com prompt e conteúdo.', 'warning');
      return;
    }
    if (this.videoAula.transcricoes?.statusAvaliacao === 'Em Andamento') {
      this.presentToast('A avaliação já está em andamento.', 'warning');
      return;
    }

    this.videoAulaService.avaliarVideoAula(this.videoAula.id).subscribe({
      next: () => {
        if (this.videoAula?.transcricoes) {
          this.videoAula.transcricoes.statusAvaliacao = 'Em Andamento';
          this.videoAula.transcricoes.avaliacao = undefined;
        }
        this.avaliacao = null;
        this.presentToast('Avaliação em andamento. O resultado aparece nesta página quando terminar.', 'success');
        this.acompanharAvaliacao();
      },
      error: (err) => {
        const mensagem = err?.error?.erro || err?.message || 'Erro ao avaliar o resumo.';
        this.presentToast(mensagem, 'danger');
      },
    });
  }

  private aplicarAvaliacaoSalva() {
    const transcricao = this.videoAula?.transcricoes;
    if (transcricao?.statusAvaliacao === 'Concluído' && transcricao.avaliacao) {
      try {
        this.avaliacao = JSON.parse(transcricao.avaliacao);
      } catch {
        this.avaliacao = null;
      }
    }
    if (transcricao?.statusAvaliacao === 'Em Andamento') {
      this.acompanharAvaliacao();
    }
  }

  private acompanharAvaliacao() {
    if (this.acompanhamento || !this.videoAula?.id) {
      return;
    }
    const id = this.videoAula.id;
    this.acompanhamento = setInterval(() => {
      this.videoAulaService.getVideoAulaById(id).subscribe({
        next: (video) => {
          if (!this.videoAula?.transcricoes || !video.transcricoes) {
            return;
          }
          this.videoAula.transcricoes.statusAvaliacao = video.transcricoes.statusAvaliacao;
          this.videoAula.transcricoes.avaliacao = video.transcricoes.avaliacao;
          const status = video.transcricoes.statusAvaliacao;
          if (status === 'Concluído') {
            this.aplicarAvaliacaoSalva();
            this.pararAcompanhamento();
            this.presentToast('Avaliação concluída.', 'success');
          } else if (status === 'Erro') {
            this.pararAcompanhamento();
            this.presentToast(video.transcricoes.avaliacao || 'Erro ao avaliar o resumo.', 'danger');
          }
        },
      });
    }, 5000);
  }

  private pararAcompanhamento() {
    if (this.acompanhamento) {
      clearInterval(this.acompanhamento);
      this.acompanhamento = null;
    }
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
