from pytubefix import YouTube
import os
from fastapi.responses import FileResponse

class YoutubeService():
    def __init__(self, video_url):
        # Usando o volume compartilhado do seu Docker Compose
        self.path = "shared-files/" 
        self.video_url = video_url
        os.makedirs(self.path, exist_ok=True)

    def baixar_video(self):
        try:
            # Inicializa o objeto YouTube
            yt = YouTube(self.video_url)
            
            # Filtra para pegar a maior resolução que já contenha Áudio + Vídeo (Progressive)
            # Isso evita que você precise do FFmpeg para fazer o merge manual
            stream = yt.streams.filter(progressive=True, file_extension='mp4').get_highest_resolution()
            
            # Realiza o download
            print(f"Baixando: {yt.title}")
            filename = stream.download(output_path=self.path)
            
            # Retorna o arquivo para o FastAPI/Spring Boot
            return FileResponse(
                filename, 
                media_type='video/mp4', 
                filename=os.path.basename(filename)
            )

        except Exception as e:
            print(f"Erro no Pytube: {str(e)}")
            return {"error": f"Erro ao baixar o vídeo: {str(e)}"}