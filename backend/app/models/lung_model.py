from pathlib import Path
import torch
import torchvision.models as models

MODEL_PATH = Path(__file__).resolve().parent.parent.parent.parent / "ai/lung_model.pth"

model = models.resnet18()

# 🔥 grayscale
model.conv1 = torch.nn.Conv2d(1, 64, kernel_size=7, stride=2, padding=3, bias=False)

# 🔥 แก้ตรงนี้ (สำคัญที่สุด)
model.fc = torch.nn.Linear(512, 2)

# โหลด weights
model.load_state_dict(torch.load(MODEL_PATH, map_location="cpu"))

model.eval()
print("loading model...")
print("Model loaded successfully")