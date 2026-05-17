"""Configuration management for Dehaze backend."""
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Path configuration
BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = os.getenv("MODEL_PATH", str(BASE_DIR / "maxim_savedmodel"))
ADAPTER_PATH = os.getenv("ADAPTER_PATH", str(BASE_DIR / "adapter_best.weights.h5"))

# API configuration
API_PORT = int(os.getenv("API_PORT", 5000))
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_ENV = os.getenv("FLASK_ENV", "development")
DEBUG = os.getenv("FLASK_DEBUG", "False").lower() == "true"

# File handling
UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER", str(BASE_DIR / "backend" / "uploads"))
RESULTS_FOLDER = os.getenv("RESULTS_FOLDER", str(BASE_DIR / "backend" / "results"))
MAX_FILE_SIZE = int(os.getenv("MAX_FILE_SIZE", 10485760))  # 10MB

# CORS configuration
ENABLE_CORS = os.getenv("ENABLE_CORS", "True").lower() == "true"
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://localhost:8080").split(",")

# Model configuration
IMG_SIZE = 256
IMG_EXTS = (".jpg", ".jpeg", ".png", ".bmp", ".webp", ".tiff")

# Create necessary directories
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULTS_FOLDER, exist_ok=True)

print(f"✓ Configuration loaded")
print(f"  - Model path: {MODEL_PATH}")
print(f"  - Adapter path: {ADAPTER_PATH}")
print(f"  - API running on {API_HOST}:{API_PORT}")
