from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.api.routes import router

import os

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


#path config

#path ของไฟล์นี้
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

#path outputs จริง
OUTPUT_PATH = os.path.abspath(
    os.path.join(BASE_DIR, "data", "outputs")
)

#debug
print("📁 BASE_DIR =", BASE_DIR)
print("📁 OUTPUT_PATH =", OUTPUT_PATH)


os.makedirs(OUTPUT_PATH, exist_ok=True)

#path
if not os.path.exists(OUTPUT_PATH):
    print("OUTPUT PATH NOT Oka")
else:
    print("OUTPUT PATH OK")

#static files
app.mount(
    "/outputs",
    StaticFiles(directory=OUTPUT_PATH),
    name="outputs"
)

#routes
app.include_router(router)

@app.get("/")
def root():
    return {
        "status": "Radiovision AI backend running",
        "outputs_path": OUTPUT_PATH
    }