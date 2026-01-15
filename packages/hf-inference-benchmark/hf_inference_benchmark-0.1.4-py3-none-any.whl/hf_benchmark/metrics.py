import os
import psutil
import torch
from hf_benchmark.device import get_device

def get_peak_memory_mb():
    """
    Returns the peak memory usage in MB.
    - CPU: Measures the process RAM (RSS).
    - GPU: Measures VRAM allocated.
    """
    device = get_device()
    
    if device.type == "cuda":
        # GPU VRAM
        return torch.cuda.max_memory_allocated() / (1024 ** 2)
    else:
        # CPU RAM (Current process)
        process = psutil.Process(os.getpid())
        # rss = Resident Set Size (Physical Memory)
        return process.memory_info().rss / (1024 ** 2)

def reset_memory_stats():
    """Resets the peak tracker (GPU only)."""
    if torch.cuda.is_available():
        torch.cuda.reset_peak_memory_stats()