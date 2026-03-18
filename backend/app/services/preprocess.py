# backend/app/services/preprocess.py

import cv2
import numpy as np


def run(image_bytes, preset):
    np_arr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_GRAYSCALE)

    original = img.copy()

    if preset == "standard":
        size = 224
    else:
        size = 512
        img = cv2.equalizeHist(img)
        img = cv2.GaussianBlur(img, (3, 3), 0)

    img = cv2.resize(img, (size, size))
    img = img / 255.0

    img = np.expand_dims(img, axis=0)

    return img.astype("float32"), original