import { HttpClient } from "@angular/common/http";
import { Injectable } from "@angular/core";
import { Observable } from "rxjs";
import { environment } from "src/environments/environment";

@Injectable({
  providedIn: 'root'
})

export class YoutubeDownloadService {
  private readonly apiUrl = `${environment.apiUrl}/youtube_download`;

  constructor(private http: HttpClient) {}

  downloadVideo(videoUrl: string): Observable<Blob> {
  return this.http.post(`${this.apiUrl}`, { video_url: videoUrl }, {
    responseType: 'blob'
  });
}
}