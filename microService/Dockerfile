FROM nvidia/cuda:12.2.2-cudnn8-devel-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive

# Instala o curl primeiro junto com as outras dependências
RUN apt-get update && apt-get install -y \
    curl \
    python3-pip \
    python3-dev \
    build-essential \
    ffmpeg \
    wkhtmltopdf \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libharfbuzz0b \
    libpangoft2-1.0-0 \
    && rm -rf /var/lib/apt/lists/*

# 👇 NOVO: Instala o Node.js v20 (necessário para resolver o challenge moderno do YT)
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN python3 -m pip install --upgrade pip


# Substitua a linha de instalação atual por esta:
RUN pip install torch torchaudio --index-url https://download.pytorch.org/whl/cu121

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

RUN pip install ninja packaging
RUN pip install flash-attn --no-build-isolation

# 👇 IMPORTANTE: copiar cookies
COPY cookies.txt /app/cookies.txt

COPY . .

EXPOSE 5000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000"]