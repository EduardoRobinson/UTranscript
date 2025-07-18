import gc
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline 
from faster_whisper import WhisperModel
import torch



class llmLoaded:
    def __init__(self):
        self.llm_pipeline = self.load_llm_pipeline()
        self.transcribe_model = WhisperModel("medium")
    
    def load_llm_pipeline(self):
        print("🔁 Carregando modelo LLM local...")

        model_path = "microsoft/Phi-4-mini-instruct"
        device = "cuda" if torch.cuda.is_available() else "cpu"
        
        tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True, use_fast=False)
        model = AutoModelForCausalLM.from_pretrained(
            model_path,
            device_map="cuda",
            torch_dtype=torch.float16 if device == "cuda" else torch.float32,
            offload_folder="offload",
            offload_buffers=True,
            trust_remote_code=True
        )
        gc.collect()
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
            torch.cuda.ipc_collect()

        return pipeline("text-generation", model=model, tokenizer=tokenizer)
    
