import gc
import logging
import threading
import torch
import os
from transformers import (
    AutoTokenizer, 
    AutoModelForCausalLM, 
    pipeline, 
    BitsAndBytesConfig,
    GenerationConfig # 🔥 Nova importação
)
from faster_whisper import WhisperModel
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger("Inicializacao")

class llmLoaded:
    def __init__(self):
        self.geracao_lock = threading.Lock()
        self.llm_pipeline = self.load_llm_pipeline()
        logger.info("Carregando Whisper distil-large-v3 na GPU")
        self.transcribe_model = WhisperModel(
            "distil-large-v3", 
            device="cuda", 
            compute_type="int8_float16"
        )
        logger.info("Whisper distil-large-v3 carregado")
        
    def load_llm_pipeline(self):
        logger.info("Carregando Llama-3.1-8B-Instruct em 4 bits na GPU")
        model_id = "meta-llama/Llama-3.1-8B-Instruct"
        token = os.getenv("HF_TOKEN")

        bnb_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype=torch.float16,
            bnb_4bit_use_double_quant=True,
        )

        tokenizer = AutoTokenizer.from_pretrained(model_id, token=token)
        if tokenizer.pad_token is None:
            tokenizer.pad_token = tokenizer.eos_token
        
        model = AutoModelForCausalLM.from_pretrained(
            model_id,
            quantization_config=bnb_config,
            device_map={"":"cuda:0"},
            trust_remote_code=True,
            token=token,
            attn_implementation="flash_attention_2"
        )

        # 🔥 Criando a configuração de geração centralizada
        gen_config = GenerationConfig.from_pretrained(model_id, token=token)
        gen_config.max_new_tokens = 1024
        gen_config.temperature = 0.6
        gen_config.top_p = 0.9
        gen_config.max_length = None
        gen_config.repetition_penalty = 1.15
        gen_config.do_sample = True
        
        # Garante que o modelo saiba onde parar (Tokens de fim de texto)
        gen_config.eos_token_id = [
            tokenizer.eos_token_id, 
            tokenizer.convert_tokens_to_ids("<|eot_id|>")
        ]
        gen_config.pad_token_id = tokenizer.pad_token_id

        # ✅ CORREÇÃO: Atribua a configuração diretamente ao objeto do modelo
        model.generation_config = gen_config

        gc.collect()
        torch.cuda.empty_cache()

        gerador = pipeline(
            "text-generation", 
            model=model, 
            tokenizer=tokenizer
        )
        logger.info(f"Llama-3.1-8B-Instruct carregado em {model.device}")
        return gerador