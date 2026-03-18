# backend/app/main.py

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.api.routes import router

app = FastAPI(title="Lung AI Detection")

# include API routes
app.include_router(router)

# serve output images
app.mount("/outputs", StaticFiles(directory="backend/data/outputs"), name="outputs")