import numpy as np
import cv2
import torch

def run(image_bytes, preset="standard"):
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_GRAYSCALE)

    if img is None:
        raise ValueError("Image decode failed")

    original = img.copy()
    img = cv2.resize(img, (224, 224))
    img = img / 255.0
    img = torch.tensor(img, dtype=torch.float32)
    img = img.unsqueeze(0).unsqueeze(0)

    return img, original