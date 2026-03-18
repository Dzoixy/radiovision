# backend/app/models/lung_model.py

import torch
from pathlib import Path

# 🔹 หา path ของ project root
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent

# 🔹 path ไปที่ model
MODEL_PATH = BASE_DIR / "ai" / "lung_model.pt"

# 🔹 load model (TorchScript)
model = torch.jit.load(str(MODEL_PATH), map_location="cpu")

# 🔹 set eval mode
model.eval()