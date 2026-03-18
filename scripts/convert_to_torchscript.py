import torch
import torchvision.models as models

# ✅ ต้องแก้ตรงนี้
model = models.resnet18(weights=None)
model.conv1 = torch.nn.Conv2d(1, 64, kernel_size=7, stride=2, padding=3, bias=False)
model.fc = torch.nn.Linear(model.fc.in_features, 2)

# โหลด weights
model.load_state_dict(torch.load("ai/lung_model.pth", map_location="cpu"))
model.eval()

# input ต้องตรง
example = torch.randn(1, 1, 224, 224)

# convert
traced = torch.jit.trace(model, example)

# save
traced.save("ai/lung_model.pt")

print("✅ Convert success")