import os
import subprocess

from fastapi import HTTPException
from fastapi.responses import FileResponse
from pytubefix import YouTube


class YoutubeService():
    def __init__(self, video_url):
        # Usando o volume compartilhado do seu Docker Compose
        self.path = "shared-files/"
        self.video_url = video_url
        os.makedirs(self.path, exist_ok=True)

    def baixar_video(self):
        # MWEB e TV passam pela página do YouTube e levam 429.
        # VISION_OS fala direto com a API e devolve áudio e vídeo separados.
        try:
            yt = YouTube(self.video_url, client="VISION_OS")
            output = self._baixar_mp4(yt)
            return FileResponse(
                output,
                media_type="video/mp4",
                filename=os.path.basename(output),
            )
        except HTTPException:
            raise
        except Exception as e:
            print(f"Erro no Pytube: {str(e)}")
            if "429" in str(e):
                raise HTTPException(
                    status_code=429,
                    detail=(
                        "O YouTube limitou as requisições deste IP. "
                        "Aguarde alguns minutos antes de tentar de novo."
                    ),
                )
            raise HTTPException(
                status_code=502,
                detail=f"Erro ao baixar o vídeo: {str(e)}",
            )

    def _baixar_mp4(self, yt: YouTube) -> str:
        progressive = yt.streams.filter(
            progressive=True, file_extension="mp4"
        ).get_highest_resolution()
        if progressive is not None:
            print(f"Baixando: {yt.title}")
            return progressive.download(output_path=self.path)

        video = self._melhor_video(yt)
        audio = self._melhor_audio(yt)
        if video is None or audio is None:
            raise RuntimeError(
                "O YouTube não retornou faixas de vídeo e áudio para este link."
            )

        print(f"Baixando: {yt.title} ({video.resolution})")
        video_path = video.download(output_path=self.path, filename="_video.mp4")
        audio_path = audio.download(output_path=self.path, filename="_audio.m4a")
        output = os.path.join(self.path, self._nome_arquivo(yt.title))

        try:
            self._juntar(video_path, audio_path, output)
        finally:
            for parcial in (video_path, audio_path):
                if os.path.exists(parcial):
                    os.remove(parcial)

        return output

    def _melhor_video(self, yt: YouTube):
        faixas = yt.streams.filter(
            adaptive=True, only_video=True, file_extension="mp4"
        )
        return max(faixas, key=self._resolucao, default=None)

    def _melhor_audio(self, yt: YouTube):
        faixas = list(yt.streams.filter(only_audio=True, mime_type="audio/mp4"))
        if not faixas:
            faixas = list(yt.streams.filter(only_audio=True))
        if not faixas:
            return None
        return max(faixas, key=self._bitrate)

    def _juntar(self, video_path: str, audio_path: str, output: str):
        resultado = subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-i",
                video_path,
                "-i",
                audio_path,
                "-c",
                "copy",
                "-movflags",
                "+faststart",
                output,
            ],
            capture_output=True,
            text=True,
        )
        if resultado.returncode != 0 or not os.path.exists(output):
            detalhe = (resultado.stderr or "").strip().splitlines()
            fim = detalhe[-1] if detalhe else "ffmpeg falhou"
            raise RuntimeError(f"Não foi possível juntar áudio e vídeo: {fim}")

    @staticmethod
    def _resolucao(stream) -> int:
        try:
            return int((stream.resolution or "0").replace("p", ""))
        except ValueError:
            return 0

    @staticmethod
    def _bitrate(stream) -> int:
        try:
            return int((stream.abr or "0").replace("kbps", ""))
        except ValueError:
            return 0

    @staticmethod
    def _nome_arquivo(titulo: str) -> str:
        limpo = "".join(
            caractere if caractere.isalnum() or caractere in " -_" else " "
            for caractere in titulo
        )
        limpo = " ".join(limpo.split())[:80].strip() or "video"
        return f"{limpo}.mp4"
