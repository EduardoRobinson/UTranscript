import gc
import logging
import os
import threading

import torch
from dotenv import load_dotenv
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig

load_dotenv()

logger = logging.getLogger("Inicializacao")

MODELO = "Qwen/Qwen3-0.6B"
# A RTX 4060 Ti tem 8 GB. O Llama 8B em 4 bits e o Whisper já ocupam quase toda a placa.
# O Qwen 8B não cabe junto e o device_map automático o manda para a CPU, onde a geração parece um loop.
_VRAM_MINIMA_GPU = 1_300_000_000


class QwenJudge:
    """Juiz Qwen3-0.6B, carregado na inicialização do microsserviço."""

    def __init__(self):
        self._lock = threading.Lock()
        self.tokenizer = None
        self.model = None

    def carregar(self):
        with self._lock:
            self._carregar()

    def gerar(self, messages: list[dict]) -> str:
        with self._lock:
            self._carregar()
            inputs = self.tokenizer.apply_chat_template(
                messages,
                add_generation_prompt=True,
                tokenize=True,
                return_dict=True,
                return_tensors="pt",
                enable_thinking=False,
            ).to(self.model.device)

            fim = [self.tokenizer.eos_token_id]
            for simbolo in ("<|im_end|>", "<|endoftext|>"):
                indice = self.tokenizer.convert_tokens_to_ids(simbolo)
                if isinstance(indice, int) and indice >= 0 and indice not in fim:
                    fim.append(indice)

            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_new_tokens=240,
                    do_sample=False,
                    eos_token_id=fim,
                    pad_token_id=self.tokenizer.pad_token_id,
                )

            novo = outputs[0][inputs["input_ids"].shape[-1]:]
            return self.tokenizer.decode(novo, skip_special_tokens=True)

    def _carregar(self):
        if self.model is not None:
            return

        token = os.getenv("HF_TOKEN") or None
        gc.collect()
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
            livre, total = torch.cuda.mem_get_info()
        else:
            livre, total = 0, 0

        self.tokenizer = AutoTokenizer.from_pretrained(MODELO, token=token)
        if self.tokenizer.pad_token_id is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token

        if livre >= _VRAM_MINIMA_GPU:
            logger.info(f"Carregando {MODELO} em 4 bits na GPU")
            quantizacao = BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_quant_type="nf4",
                bnb_4bit_compute_dtype=torch.float16,
                bnb_4bit_use_double_quant=True,
            )
            self.model = AutoModelForCausalLM.from_pretrained(
                MODELO,
                quantization_config=quantizacao,
                device_map={"": "cuda:0"},
                token=token,
            )
        else:
            livre_mib = livre // (1024 * 1024)
            total_mib = total // (1024 * 1024)
            logger.info(
                f"Carregando {MODELO} em float32 na CPU. "
                f"VRAM livre: {livre_mib} MiB de {total_mib} MiB"
            )
            self.model = AutoModelForCausalLM.from_pretrained(
                MODELO,
                dtype=torch.float32,
                device_map={"": "cpu"},
                token=token,
            )
        logger.info(f"{MODELO} carregado em {self.model.device}")
