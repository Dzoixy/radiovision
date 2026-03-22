import torch
import numpy as np

def run(model, img_tensor):
    model.eval()

    with torch.no_grad():
        outputs = model(img_tensor)
        probs = torch.softmax(outputs, dim=1)

    confidence, pred = torch.max(probs, dim=1)

    return pred.item(), confidence.item()