# Dehaze Backend - Setup & Installation Guide

## Quick Start

### 1. Environment Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment (Windows)
python -m venv venv
venv\Scripts\activate

# Or on Linux/macOS
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration

```bash
# Copy example environment file
copy .env.example .env
# Update .env with your settings if needed
```

### 3. Run Tests

```bash
# Test inference module
python test_inference.py

# Test metrics module
python test_metrics.py
```

### 4. Start API Server

```bash
python app.py
```

The API will be available at `http://localhost:5000`

## Project Structure

```
backend/
├── app.py                    # FastAPI server
├── inference.py              # Model inference logic
├── metrics.py                # PSNR/SSIM calculations
├── config.py                 # Configuration management
├── logger.py                 # Logging setup
├── test_inference.py         # Inference tests
├── test_metrics.py           # Metrics tests
├── requirements.txt          # Python dependencies
├── .env.example              # Environment template
└── README.md                 # This file
```

## API Endpoints

### Health Check
- `GET /api/health`
- Response: `{"status": "ok", "models_loaded": true}`

### Dehaze Image
- `POST /api/dehaze`
- Input: Image file (multipart/form-data)
- Output: Base64 encoded dehazed image + metadata

### Dehaze with Metrics
- `POST /api/dehaze-with-metrics`
- Input: Hazy image + optional ground truth
- Output: Dehazed image + PSNR/SSIM metrics

## Dependencies

- **tensorflow==2.15.0** - Deep learning framework
- **fastapi==0.109.0** - API framework
- **uvicorn==0.27.0** - ASGI server
- **pillow==10.1.0** - Image processing
- **numpy==1.24.3** - Numerical operations
- **scikit-image==0.22.0** - Image metrics
- **python-dotenv==1.0.0** - Environment management

## GPU Support

For GPU acceleration, ensure:
1. NVIDIA CUDA Toolkit 11.x or 12.x installed
2. NVIDIA cuDNN 8.x installed
3. NVIDIA GPU with compute capability 3.5+

TensorFlow will automatically detect and use GPU if available.

## Troubleshooting

### Import Errors
- Ensure virtual environment is activated
- Run `pip install -r requirements.txt` again

### Model Loading Errors
- Check that `maxim_savedmodel/` and `adapter_best.weights.h5` exist
- Verify paths in `.env` configuration

### CUDA/GPU Errors
- Run on CPU by setting environment variable
- Reduce batch size or input resolution
