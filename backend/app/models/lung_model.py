import torch
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[3]

MODEL_PATH = BASE_DIR / "ai" / "lung_model.pt"

print("MODEL PATH:", MODEL_PATH)
print("EXISTS:", MODEL_PATH.exists())

model = torch.jit.load(str(MODEL_PATH), map_location="cpu")
model.eval()