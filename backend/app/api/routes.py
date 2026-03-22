from fastapi import APIRouter, UploadFile, File, Form
import uuid
import os
import cv2
import numpy as np

from app.services import preprocess, inference, gradcam, render
from app.models.lung_model import model

# =========================
# INIT ROUTER
# =========================
router = APIRouter()

# =========================
# PATH CONFIG (ต้องตรง main.py)
# =========================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

UPLOAD_DIR = os.path.join(DATA_DIR, "uploads")
OUTPUT_DIR = os.path.join(DATA_DIR, "outputs")

# create dirs
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

print("📁 UPLOAD_DIR =", UPLOAD_DIR)
print("📁 OUTPUT_DIR =", OUTPUT_DIR)


# =========================
# ANALYZE API
# =========================
@router.post("/analyze")
async def analyze(
    file: UploadFile = File(...),
    preset: str = Form("standard")
):
    try:
        # =========================
        # READ FILE
        # =========================
        image_bytes = await file.read()

        study_id = str(uuid.uuid4())

        input_path = os.path.join(UPLOAD_DIR, f"{study_id}.jpg")
        output_path = os.path.join(OUTPUT_DIR, f"{study_id}.jpg")
        original_path = os.path.join(OUTPUT_DIR, f"{study_id}_orig.jpg")

        print("\n====== NEW REQUEST ======")
        print("STUDY ID:", study_id)
        print("SAVE INPUT:", input_path)

        # save input
        with open(input_path, "wb") as f:
            f.write(image_bytes)

        # =========================
        # PREPROCESS
        # =========================
        img_tensor, original = preprocess.run(image_bytes, preset)

        print("PREPROCESS DONE")
        print("ORIGINAL TYPE:", type(original))
        print("ORIGINAL SHAPE:", None if original is None else original.shape)

        # =========================
        # INFERENCE
        # =========================
        pred, confidence = inference.run(model, img_tensor)

        print("INFERENCE DONE:", pred, confidence)

        # =========================
        # GRADCAM
        # =========================
        cam = gradcam.generate(model, img_tensor)

        print("CAM TYPE:", type(cam))
        print("CAM SHAPE:", None if cam is None else cam.shape)

        # =========================
        # HEATMAP
        # =========================
        heatmap = render.generate_heatmap(cam)

        print("HEATMAP SHAPE:", None if heatmap is None else heatmap.shape)

        # =========================
        # OVERLAY
        # =========================
        result_img = render.overlay(original, heatmap)

        print("RESULT TYPE:", type(result_img))
        print("RESULT SHAPE:", None if result_img is None else result_img.shape)

        # =========================
        # FIX IMAGE FORMAT (สำคัญมาก)
        # =========================
        def fix_image(img):
            if img is None:
                return None

            if img.dtype != np.uint8:
                if img.max() <= 1.0:
                    img = (img * 255).astype(np.uint8)
                else:
                    img = img.astype(np.uint8)

            return img

        result_img = fix_image(result_img)
        original = fix_image(original)

        # =========================
        # SAVE IMAGE
        # =========================
        ok1 = cv2.imwrite(output_path, result_img)
        ok2 = cv2.imwrite(original_path, original)

        print("SAVE RESULT:", ok1, ok2)
        print("OUTPUT PATH:", output_path)

        # =========================
        # CHECK SAVE FAIL
        # =========================
        if not ok1 or not ok2:
            return {
                "error": "Failed to save images",
                "debug": {
                    "result_img_none": result_img is None,
                    "original_none": original is None
                }
            }

        # =========================
        # RESPONSE
        # =========================
        return {
            "finding": "Pneumonia" if pred == 1 else "Normal",
            "confidence": float(confidence),
            "heatmap_url": f"/outputs/{study_id}.jpg",
            "original_url": f"/outputs/{study_id}_orig.jpg"
        }

    except Exception as e:
        print("🔥 ERROR:", str(e))
        return {
            "error": str(e)
        }