import time
import torch
import statistics
from hf_benchmark.device import get_device
from hf_benchmark.throughput import measure_throughput
from hf_benchmark.metrics import get_peak_memory_mb, reset_memory_stats # <--- New Import

def profile_inference(fn, token_count=32, warmup=3, runs=5):
    device = get_device()
    
    print(f"🔥 Warming up ({warmup} runs)...")
    for _ in range(warmup):
        fn()

    # Reset stats before the real test starts
    reset_memory_stats()

    # --- 1. Measure Latency ---
    print(f"🚀 Benchmarking Latency...")
    latencies = []
    for _ in range(runs):
        if device.type == "cuda": torch.cuda.synchronize()
        start = time.time()
        fn()
        if device.type == "cuda": torch.cuda.synchronize()
        latencies.append((time.time() - start) * 1000)
    
    latencies.sort()

    # --- 2. Measure Throughput ---
    tps = measure_throughput(fn, token_count, runs=runs)

    # --- 3. Measure Memory (New) ---
    peak_mem = get_peak_memory_mb()

    return {
        "p50": latencies[len(latencies)//2],
        "mean": statistics.mean(latencies),
        "throughput": tps,
        "memory_mb": peak_mem  # <--- New metric
    }