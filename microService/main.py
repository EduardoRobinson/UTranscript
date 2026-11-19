import os

os.environ["HF_HUB_DISABLE_PROGRESS_BARS"] = "1"
os.environ["TQDM_DISABLE"] = "1"

import logging
from contextlib import asynccontextmanager

import torch
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from huggingface_hub.utils import disable_progress_bars
from transformers.utils import logging as tf_logging

from api.endpoints import avaliacao_service
from api.endpoints import router as router
from models.llmLoaded import llmLoaded
from models.qwenJudge import QwenJudge

logger = logging.getLogger("Inicializacao")
logger.setLevel(logging.INFO)
logger.propagate = False
if not logger.handlers:
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("%(asctime)s | %(levelname)s | %(message)s"))
    logger.addHandler(handler)

tf_logging.disable_progress_bar()
disable_progress_bars()


@asynccontextmanager
async def lifespan(app: FastAPI):
    cuda = torch.cuda.is_available()
    gpu = torch.cuda.get_device_name(0) if cuda else "indisponível"
    logger.info(f"Iniciando microsserviço. CUDA disponível: {cuda}. GPU: {gpu}.")

    llm_instance = llmLoaded()
    juiz = QwenJudge()
    juiz.carregar()

    if (
        llm_instance.llm_pipeline is None
        or llm_instance.transcribe_model is None
        or juiz.model is None
    ):
        raise RuntimeError("Os três modelos não foram carregados. A API não será aberta.")

    app.state.llm = llm_instance
    app.state.juiz = juiz
    avaliacao_service.definir_juiz(juiz)
    logger.info("Llama, Whisper e Qwen carregados. Abrindo a API.")
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(router)

origins = [
    "http://localhost:3000",  # Adicione o endereço do seu front-end aqui
    "http://127.0.0.1:3000", # Outra possibilidade de endereço
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Permite essas origens
    allow_credentials=True,  # Permite envio de cookies/autenticação
    allow_methods=["*"],  # Permite todos os métodos HTTP (GET, POST, etc.)
    allow_headers=["*"],  # Permite todos os headers
)
