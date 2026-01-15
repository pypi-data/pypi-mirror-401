from transformers import AutoModelForCausalLM, AutoTokenizer
from hf_benchmark.device import get_device
import torch

def load_model(model_name):
    device = get_device()
    print(f"⏳ Loading {model_name} on {device}...")
    
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name).to(device).eval()
    return model, tokenizer, device

def run_once(model, tokenizer, device, prompt="Hello", max_new_tokens=32):
    inputs = tokenizer(prompt, return_tensors="pt").to(device)
    with torch.no_grad():
        output = model.generate(**inputs, max_new_tokens=max_new_tokens)

    return output.shape[-1] - inputs["input_ids"].shape[-1]
