from app.models.lung_model import model
import torch

def run(img):
    tensor = torch.tensor(img).unsqueeze(0)

    with torch.no_grad():
        out = model(tensor)
        prob = torch.softmax(out, dim=1)

    return prob.numpy()[0]