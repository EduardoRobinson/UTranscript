import { Component } from '@angular/core';
import { YoutubeDownloadService } from '../services/youtube.download.service';

@Component({
  selector: 'app-tab5',
  templateUrl: 'tab5.page.html',
  styleUrls: ['tab5.page.scss'],
  standalone: false,
})
export class Tab5Page {

videoUrl: string = '';
  constructor(private ytService: YoutubeDownloadService) {}

  downloadVideo() {
  if (this.videoUrl) {
    this.ytService.downloadVideo(this.videoUrl).subscribe(blob => {
      console.log('Blob recebido:', blob);
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      const videoId = this.extractVideoId(this.videoUrl);
      a.download = `video-${videoId}.mp4`;
      a.click();
      window.URL.revokeObjectURL(url);
    }, error => {
      console.error('Erro ao baixar vídeo:', error);
    });
  } else {
    alert('URL inválida');
  }
}

  private extractVideoId(url: string): string | null {
  const match = url.match(/(?:v=|\.be\/)([a-zA-Z0-9_-]{11})/);
  return match ? match[1] : null;
}

}
