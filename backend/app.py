"""FastAPI backend server for Dehaze application."""
import io
import time
import base64
from typing import Optional
from pathlib import Path

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn

from config import API_HOST, API_PORT, API_ENV, ENABLE_CORS, CORS_ORIGINS
from inference import load_models, process_image_bytes
from metrics import calculate_metrics, format_metrics_report
from PIL import Image

# Initialize FastAPI app
app = FastAPI(
    title="Dehaze API",
    description="Image dehazing service with quality metrics",
    version="1.0.0"
)

# Add CORS middleware
if ENABLE_CORS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Global models cache
models = {"base_model": None, "adapter": None}


@app.on_event("startup")
async def startup_event():
    """Load models on startup."""
    print("\n" + "=" * 60)
    print("INITIALIZING DEHAZE API SERVER")
    print("=" * 60)
    
    try:
        global models
        models["base_model"], models["adapter"] = load_models()
        print("✓ Models loaded successfully")
        print("=" * 60 + "\n")
    except Exception as e:
        print(f"✗ Failed to load models: {e}")
        raise


@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "ok",
        "models_loaded": models["base_model"] is not None,
        "version": "1.0.0",
        "environment": API_ENV
    }


@app.post("/api/dehaze")
async def dehaze_image(file: UploadFile = File(...)):
    """
    Dehaze a single image.
    
    Args:
        file: Image file (JPG, PNG, BMP, etc.)
        
    Returns:
        JSON with dehazed image (base64) and metadata
    """
    if models["base_model"] is None:
        raise HTTPException(status_code=503, detail="Models not loaded")
    
    try:
        # Validate file
        if not file.filename:
            raise HTTPException(status_code=400, detail="No filename provided")
        
        # Read file
        contents = await file.read()
        if len(contents) == 0:
            raise HTTPException(status_code=400, detail="Empty file")
        
        # Process image
        image_bytes = io.BytesIO(contents)
        dehazed_image, processing_time_ms = process_image_bytes(
            image_bytes,
            models["base_model"],
            models["adapter"]
        )
        
        # Convert to base64
        buffer = io.BytesIO()
        dehazed_image.save(buffer, format="JPEG", quality=95)
        buffer.seek(0)
        image_b64 = base64.b64encode(buffer.getvalue()).decode()
        
        return {
            "success": True,
            "dehazed_image": f"data:image/jpeg;base64,{image_b64}",
            "processing_time_ms": round(processing_time_ms, 2),
            "input_size": list(dehazed_image.size),
            "output_size": list(dehazed_image.size)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in dehaze endpoint: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/dehaze-with-metrics")
async def dehaze_with_metrics(
    hazy_image: UploadFile = File(...),
    ground_truth: Optional[UploadFile] = File(None)
):
    """
    Dehaze image and calculate metrics.
    
    Args:
        hazy_image: Input hazy image file
        ground_truth: Optional ground truth (clean) image
        
    Returns:
        JSON with dehazed image, metrics, and metadata
    """
    if models["base_model"] is None:
        raise HTTPException(status_code=503, detail="Models not loaded")
    
    try:
        # Process hazy image
        hazy_contents = await hazy_image.read()
        if len(hazy_contents) == 0:
            raise HTTPException(status_code=400, detail="Empty hazy image")
        
        hazy_bytes = io.BytesIO(hazy_contents)
        dehazed_image, processing_time_ms = process_image_bytes(
            hazy_bytes,
            models["base_model"],
            models["adapter"]
        )
        
        # Convert dehazed to base64
        buffer = io.BytesIO()
        dehazed_image.save(buffer, format="JPEG", quality=95)
        buffer.seek(0)
        dehazed_b64 = base64.b64encode(buffer.getvalue()).decode()
        
        # Initialize response
        response = {
            "success": True,
            "dehazed_image": f"data:image/jpeg;base64,{dehazed_b64}",
            "processing_time_ms": round(processing_time_ms, 2),
            "has_ground_truth": ground_truth is not None,
            "metrics": None
        }
        
        # Calculate metrics if ground truth provided
        if ground_truth is not None:
            gt_contents = await ground_truth.read()
            if len(gt_contents) == 0:
                raise HTTPException(status_code=400, detail="Empty ground truth image")
            
            # Calculate metrics
            hazy_pil = Image.open(io.BytesIO(hazy_contents)).convert("RGB")
            gt_pil = Image.open(io.BytesIO(gt_contents)).convert("RGB")
            
            metrics = calculate_metrics(hazy_pil, dehazed_image, gt_pil)
            response["metrics"] = metrics
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in dehaze-with-metrics endpoint: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/info")
async def get_info():
    """Get API information."""
    return {
        "name": "Dehaze API",
        "version": "1.0.0",
        "description": "Image dehazing using MAXIM-S2 + Trainable Adapter",
        "endpoints": {
            "health": "GET /api/health",
            "dehaze": "POST /api/dehaze",
            "dehaze_with_metrics": "POST /api/dehaze-with-metrics",
            "info": "GET /api/info"
        }
    }


if __name__ == "__main__":
    print(f"\nStarting server on {API_HOST}:{API_PORT}")
    uvicorn.run(
        app,
        host=API_HOST,
        port=API_PORT,
        log_level="info"
    )
