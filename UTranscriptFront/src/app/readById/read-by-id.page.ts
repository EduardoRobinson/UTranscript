import { Component, OnInit } from '@angular/core';
import { LoadingController, ToastController } from '@ionic/angular';
import { VideoAulaService } from '../services/video_aula.service';
import { Router } from '@angular/router';
import { VideoAula } from '../types/VideoAula';

@Component({
  selector: 'app-read-by-id',
  templateUrl: './read-by-id.page.html',
  styleUrls: ['./read-by-id.page.scss'],
  standalone: false,
})
export class ReadByIdPage implements OnInit {
  videoAula: VideoAula | undefined;
  constructor(
    private videoAulaService: VideoAulaService,
    private toastController: ToastController,
    private router: Router,
    private loadingCtrl: LoadingController
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
        },
        (error) => {
          this.presentToast('Erro ao carregar vídeo: ' + error.message);
        }
      );
    } else {
      this.presentToast('ID do vídeo não encontrado.');
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
    this.router.navigate(['/tabs/tab2']);
  }

  async exportarParaPDF() {
    if (!this.videoAula) {
      this.presentToast('Vídeo não carregado.', 'danger');
      return;
    }
    if(this.videoAula.transcricoes?.status.descricao === 'Cancelado' || this.videoAula.transcricoes?.status.descricao === 'Pendente' 
      || this.videoAula.transcricoes?.status.descricao === 'Em Andamento') {
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
}
