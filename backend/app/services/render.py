# backend/app/services/render.py

import cv2
import numpy as np


def generate_heatmap():
    return np.random.rand(224, 224)


def overlay(original, heatmap):
    heatmap = cv2.resize(heatmap, (original.shape[1], original.shape[0]))
    heatmap = (heatmap * 255).astype("uint8")
    heatmap = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)

    if len(original.shape) == 2:
        original = cv2.cvtColor(original, cv2.COLOR_GRAY2BGR)

    return cv2.addWeighted(original, 0.7, heatmap, 0.3, 0)