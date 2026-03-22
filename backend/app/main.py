from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api.routes import router

import os

# =========================
# INIT APP
# =========================
app = FastAPI()

# =========================
# CORS (frontend เรียกได้)
# =========================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# PATH CONFIG (สำคัญมาก)
# =========================

# path ของไฟล์นี้ (app/)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# path outputs จริง
OUTPUT_PATH = os.path.abspath(
    os.path.join(BASE_DIR, "data", "outputs")
)

# debug
print("📁 BASE_DIR =", BASE_DIR)
print("📁 OUTPUT_PATH =", OUTPUT_PATH)

# สร้างโฟลเดอร์ถ้ายังไม่มี
os.makedirs(OUTPUT_PATH, exist_ok=True)

# ตรวจสอบ path
if not os.path.exists(OUTPUT_PATH):
    print("❌ OUTPUT PATH NOT FOUND")
else:
    print("✅ OUTPUT PATH OK")

# =========================
# STATIC FILE (serve รูป)
# =========================
app.mount(
    "/outputs",
    StaticFiles(directory=OUTPUT_PATH),
    name="outputs"
)

# =========================
# ROUTES
# =========================
app.include_router(router)

# =========================
# ROOT TEST
# =========================
@app.get("/")
def root():
    return {
        "status": "Radiovision AI backend running",
        "outputs_path": OUTPUT_PATH
    }