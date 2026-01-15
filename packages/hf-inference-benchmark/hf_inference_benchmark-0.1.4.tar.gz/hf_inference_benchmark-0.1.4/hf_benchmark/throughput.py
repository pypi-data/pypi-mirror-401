import time
import torch
from hf_benchmark.device import get_device

def measure_throughput(fn, total_tokens, runs=5):
    """
    Calculates generation speed in Tokens Per Second (TPS).
    """
    device = get_device()
    total_time = 0
    
    print(f"🌊 Measuring Throughput over {runs} runs...")
    
    for _ in range(runs):
        # Sync GPU before starting timer (Crucial for accuracy)
        if device.type == "cuda":
            torch.cuda.synchronize()
            
        start = time.time()
        fn() # Runs the model generation
        
        # Sync GPU after finishing
        if device.type == "cuda":
            torch.cuda.synchronize()
            
        total_time += (time.time() - start)
        
    avg_time = total_time / runs
    tps = total_tokens / avg_time
    return tps