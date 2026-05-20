from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.endpoints import router as router
from models.llmLoaded import llmLoaded
import torch

print(f"CUDA está disponível? {torch.cuda.is_available()}")
print(f"Nome da GPU: {torch.cuda.get_device_name(0)}")
app=FastAPI()
print("🚀 Iniciando app e carregando modelo LLM...")
llm_instance = llmLoaded()
app.state.llm = llm_instance
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