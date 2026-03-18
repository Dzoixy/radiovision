# backend/app/api/routes.py

from fastapi import APIRouter, UploadFile, File, Form, HTTPException
import uuid
import os
from pathlib import Path
import cv2

from app.services import preprocess, inference, postprocess, render
from app.schemas.result import ResultResponse

router = APIRouter()

# safer path
BASE_DIR = Path("backend/data")
UPLOAD_DIR = BASE_DIR / "uploads"
OUTPUT_DIR = BASE_DIR / "outputs"

UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


@router.post("/analyze", response_model=ResultResponse)
async def analyze(
    file: UploadFile = File(...),
    purpose: str = Form(...),
    preset: str = Form(...)
):
    # 🔹 validate file type
    if file.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(status_code=400, detail="Invalid file type")

    # 🔹 validate options
    if purpose not in ["screening", "diagnostic"]:
        raise HTTPException(status_code=400, detail="Invalid purpose")

    if preset not in ["standard", "high"]:
        raise HTTPException(status_code=400, detail="Invalid preset")

    try:
        # 1. read file
        image_bytes = await file.read()

        # 2. generate id
        study_id = str(uuid.uuid4())

        input_path = UPLOAD_DIR / f"{study_id}.jpg"
        output_path = OUTPUT_DIR / f"{study_id}.jpg"

        # 3. save original
        with open(input_path, "wb") as f:
            f.write(image_bytes)

        # 4. preprocess
        img, original = preprocess.run(image_bytes, preset)

        # 5. inference
        prob = inference.run(img)

        # 6. postprocess
        result = postprocess.run(prob, purpose)

        # 7. render
        heatmap = render.generate_heatmap()
        result_img = render.overlay(original, heatmap)

        # 8. save result image
        cv2.imwrite(str(output_path), result_img)

        # 9. return (ใช้ schema)
        return ResultResponse(
            id=study_id,
            finding=result["label"],
            confidence=result["confidence"],
            purpose=purpose,
            preset=preset,
            image_url=f"/outputs/{study_id}.jpg",
            suggestion="Follow-up recommended"
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))