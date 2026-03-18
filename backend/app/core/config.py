from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

MODEL_PATH = BASE_DIR / "ai" / "lung_model.pt"
UPLOAD_DIR = BASE_DIR / "backend" / "data" / "uploads"
OUTPUT_DIR = BASE_DIR / "backend" / "data" / "outputs"