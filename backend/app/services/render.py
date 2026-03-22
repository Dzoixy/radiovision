import cv2
import numpy as np

def generate_heatmap(cam):
    cam = cam - np.min(cam)
    cam = cam / (np.max(cam) + 1e-8)
    cam = np.uint8(255 * cam)
    heatmap = cv2.applyColorMap(cam, cv2.COLORMAP_JET)
    return heatmap


def overlay(original, heatmap, alpha=0.4):
    heatmap = cv2.resize(heatmap, (original.shape[1], original.shape[0]))

    if len(original.shape) == 2:
        original = cv2.cvtColor(original, cv2.COLOR_GRAY2BGR)

    return cv2.addWeighted(original, 1 - alpha, heatmap, alpha, 0)