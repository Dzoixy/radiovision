from fastapi import APIRouter, UploadFile, File, Form
import uuid
import os
import cv2
import numpy as np
from app.services import preprocess, inference, gradcam, render
from app.models.lung_model import model
from app.services.report import generate_medical_report

router = APIRouter()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
UPLOAD_DIR = os.path.join(DATA_DIR, "uploads")
OUTPUT_DIR = os.path.join(DATA_DIR, "outputs")
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)
print("UPLOAD_DIR =", UPLOAD_DIR)
print("OUTPUT_DIR =", OUTPUT_DIR)

def get_location_from_cam(cam):
    h, w = cam.shape
    y, x = np.unravel_index(np.argmax(cam), cam.shape)

    if x < w / 2:
        side = "ซ้าย"
    else:
        side = "ขวา"

    if y < h / 3:
        vertical = "ส่วนบน"
    elif y < 2 * h / 3:
        vertical = "ส่วนกลาง"
    else:
        vertical = "ส่วนล่าง"
    return side, vertical

@router.post("/analyze")
async def analyze(
    file: UploadFile = File(...),
    preset: str = Form("standard")
):
    try:
        #READFILE
        image_bytes = await file.read()
        study_id = str(uuid.uuid4())
        input_path = os.path.join(UPLOAD_DIR, f"{study_id}.jpg")
        output_path = os.path.join(OUTPUT_DIR, f"{study_id}.jpg")
        original_path = os.path.join(OUTPUT_DIR, f"{study_id}_orig.jpg")

        print("\n====== NEW REQUEST ======")
        print("STUDY ID:", study_id)
        print("SAVE INPUT:", input_path)

        #save,input
        with open(input_path, "wb") as f:
            f.write(image_bytes)

        #process
        img_tensor, original = preprocess.run(image_bytes, preset)
        print("PREPROCESS DONE")
        print("ORIGINAL TYPE:", type(original))
        print("ORIGINAL SHAPE:", None if original is None else original.shape)

        #inference"
        pred, confidence = inference.run(model, img_tensor)
        finding = "Pneumonia" if pred == 1 else "Normal"
        print("INFERENCE DONE:", pred, confidence)
        
        #gradcam
        cam = gradcam.generate(model, img_tensor)
        side, vertical = get_location_from_cam(cam)   
        print("CAM TYPE:", type(cam))
        print("CAM SHAPE:", None if cam is None else cam.shape)
        #report
        report = generate_medical_report(
            finding, 
            confidence,
            side=side, 
            vertical=vertical)
        #heatmap
        heatmap = render.generate_heatmap(cam)
        print("HEATMAP SHAPE:", None if heatmap is None else heatmap.shape)

        #overlay
        result_img = render.overlay(original, heatmap)
        print("RESULT TYPE:", type(result_img))
        print("RESULT SHAPE:", None if result_img is None else result_img.shape)
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

        #save,output
        ok1 = cv2.imwrite(output_path, result_img)
        ok2 = cv2.imwrite(original_path, original)

        print("SAVE RESULT:", ok1, ok2)
        print("OUTPUT PATH:", output_path)
        if not ok1 or not ok2:
            return {
                "error": "Failed to save images",
                "debug": {
                    "result_img_none": result_img is None,
                    "original_none": original is None
                }
            }
        #response
        return {
            "finding": "Pneumonia" if pred == 1 else "Normal",
            "confidence": float(confidence),
            "heatmap_url": f"/outputs/{study_id}.jpg",
            "original_url": f"/outputs/{study_id}_orig.jpg",
            "report": report
        }
        
    except Exception as e:
        print("ERROR:", str(e))
        return {
            "error": str(e)
        }
     