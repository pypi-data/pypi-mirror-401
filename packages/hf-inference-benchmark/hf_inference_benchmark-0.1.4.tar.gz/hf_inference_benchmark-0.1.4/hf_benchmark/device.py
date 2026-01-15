import torch

def get_device():
    """
    Returns the best available device (CUDA > CPU).
    """
    if torch.cuda.is_available():
        return torch.device("cuda")
    # You can add "mps" here later for Mac users
    return torch.device("cpu")