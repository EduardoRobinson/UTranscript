from fastapi.responses import FileResponse
import yt_dlp
import os

class YoutubeService():
    def __init__(self,video_url):
        self.path = "downloads/"
        self.video_url = video_url



    def baixar_video(self):
        try:
            ydl_opts = {
                'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4',
                'merge_output_format': 'mp4',
                'outtmpl': self.path + '%(title)s.%(ext)s',
                'quiet': True,
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(self.video_url, download=True)
                filename = ydl.prepare_filename(info)
            return FileResponse(filename, media_type='video/mp4', filename=os.path.basename(filename))

        except Exception as e:
            return {"error": f"Erro ao baixar o vídeo: {str(e)}"}