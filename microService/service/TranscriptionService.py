import threading
from dotenv import load_dotenv
from models.transcriptionType import TranscriptionResponse
import whisperx
import tempfile
import os
from faster_whisper import WhisperModel
import pdfkit
from jinja2 import Environment, FileSystemLoader
from llama_cpp import Llama


load_dotenv()

class Transcricao():
    def __init__(self):
        self.model = WhisperModel("large-v2")     
        self.llm = ""  # Modelo local
        self.tokenizer = None
        self.model_instance = None

        self.load_local_model()

    def load_local_model(self):
        """Carrega o modelo Llama 3.2-1B localmente."""
        
        print("Carregando modelo local...")
        self.llm = Llama.from_pretrained(
         repo_id="Inza124/Llama3.2_3b",
         filename="Llama3.2-maIN.gguf",
         n_gpu_layers=-1, # Uncomment to use GPU acceleration
         seed=1337, # Uncomment to set a specific seed
         n_ctx=2048, # Uncomment to increase the context window
        )
        
        

    def generate_text(self, prompt):
        """Gera texto usando o modelo Llama local."""
        output=self.llm.create_chat_completion(messages=[
          {
                "role": "system",
                "content": "You are an assistant who perfectly describes text."
          },
          {
              "role": "user",
              "content": f"Gostaria de um relatório sobre a seguinte transcrição feita sobre uma reunião:{prompt}"
          }
        ]
        )
        return output

    async def transcrever2(self, arquivo):
            """Transcreve um áudio usando WhisperX."""
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
                temp_file.write(await arquivo.read())  
                temp_path = temp_file.name
            
            print(f"Arquivo temporário criado em: {temp_path}")

            if not os.path.exists(temp_path):
                raise FileNotFoundError(f"Arquivo temporário não encontrado: {temp_path}")
            
            try:
                audio = whisperx.load_audio(temp_path)
            except FileNotFoundError as e:
                raise FileNotFoundError("Certifique-se de que o FFmpeg está instalado e no PATH do sistema.") from e

            result = self.model.transcribe(audio)
            updated_first_element = [item.__dict__ for item in result[0]]
            result = (updated_first_element, *result[1:])
            model_a, metadata = whisperx.load_align_model(language_code=result[1].language, device="cuda")
            result = whisperx.align(list(result[0]), model_a, metadata, audio, "cuda", return_char_alignments=False)
            
            text = []
            for item in result["segments"]:
                text.append(item["text"])
            result = " ".join(text)
            print(result)

            return await self.resume(result)

    async def resume(self, result):
        """Gera um resumo do texto transcrito."""
        response = self.generate_text(result)
        print(response["choices"])
        transcription = TranscriptionResponse(transcricao=result, resumo=response["choices"][0]["message"]["content"])
        return transcription

    def gerar_pdf(self,Objeto):
        print(Objeto)
        BASE_DIR = os.path.abspath(os.path.dirname(__file__))  # Diretório do script principal
        TEMPLATES_DIR = os.path.join(BASE_DIR, "..", "templates")  # Caminho correto para a pasta templates
        env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))
        template = env.get_template("pdf.html")
        html_content = template.render(objeto=Objeto)
        temp_html_path = "temp.html"
        with open(temp_html_path, "w", encoding="utf-8") as f:
            f.write(html_content)
        caminho_wkhtmltopdf = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
        config = pdfkit.configuration(wkhtmltopdf=caminho_wkhtmltopdf)
        options = {
        "enable-local-file-access": "",
        }
        output_pdf_path = os.path.abspath("app/resumes/out.pdf")
        pdfkit.from_file(temp_html_path, output_pdf_path,configuration=config, options=options)
        if not os.path.exists(output_pdf_path):
            raise FileNotFoundError(f"O arquivo PDF não foi gerado: {output_pdf_path}")
        os.remove(temp_html_path)

        

        
        
        



