from datetime import date
import os
import pdfkit
from jinja2 import Environment, FileSystemLoader
from dto.videoAulaDTO import VideoAulaDTO
from weasyprint import HTML



class pdfService:
    def gerar_pdf(self, Objeto: VideoAulaDTO):
        if isinstance(Objeto.data, list):
            Objeto.data = date(*Objeto.data)

        BASE_DIR = os.path.abspath(os.path.dirname(__file__))
        TEMPLATES_DIR = os.path.join(BASE_DIR, "..", "templates")

        env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))
        template = env.get_template("pdf.html")
        html_content = template.render(objeto=Objeto)

        # 👉 Resolve o caminho da pasta onde o PDF vai ser salvo
        output_dir = os.path.join(BASE_DIR, "..", "resumes")
        os.makedirs(output_dir, exist_ok=True)  # Garante que a pasta existe

        output_pdf_path = os.path.join(output_dir, "out.pdf")

        HTML(string=html_content).write_pdf(output_pdf_path)

        if not os.path.exists(output_pdf_path):
            raise FileNotFoundError(f"O arquivo PDF não foi gerado: {output_pdf_path}")
