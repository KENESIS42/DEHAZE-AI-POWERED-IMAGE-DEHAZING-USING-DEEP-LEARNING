# Dehaze Project - Implementation Plan

## 📋 Project Objective

Develop a **complete end-to-end image dehazing application** with:
1. Backend inference pipeline for hazy image processing
2. Metrics calculation (PSNR & SSIM) for quality assessment
3. Frontend web interface with drag-drop functionality
4. Real-time processing and results visualization

---

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    USER INTERFACE (Frontend)                │
│  • Drag-drop hazy image input                               │
│  • Optional: Upload ground truth image                      │
│  • Display dehazed output                                   │
│  • Show metrics (PSNR, SSIM) if ground truth provided       │
└─────────────────────────────┬───────────────────────────────┘
                              │ HTTP/WebSocket
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                  BACKEND API SERVER                         │
│  • Flask/FastAPI REST endpoints                             │
│  • Request handling & validation                            │
│  • File upload management                                   │
│  • Inference orchestration                                  │
└─────────────────────────────┬───────────────────────────────┘
                              │
                              ↓
┌─────────────────────────────────────────────────────────────┐
│              INFERENCE & PROCESSING LAYER                   │
│  • Load MAXIM-S2 SavedModel (frozen backbone)              │
│  • Load trained adapter weights (adapter_best.weights.h5)  │
│  • Preprocess input image (256×256, [0,1] normalization)   │
│  • Execute forward pass (backbone + adapter)               │
│  • Post-process output (denormalization, clipping)         │
└─────────────────────────────┬───────────────────────────────┘
                              │
                              ↓
┌─────────────────────────────────────────────────────────────┐
│            METRICS CALCULATION LAYER                        │
│  • PSNR (Peak Signal-to-Noise Ratio)                        │
│  • SSIM (Structural Similarity Index)                       │
│  • Comparison: hazy vs dehazed vs ground truth              │
└─────────────────────────────┬───────────────────────────────┘
                              │
                              ↓
┌─────────────────────────────────────────────────────────────┐
│               RESPONSE & DELIVERY                           │
│  • JSON API response with results                           │
│  • Base64 encoded images                                    │
│  • Metric scores                                            │
│  • Processing metadata (time, size, etc.)                   │
└─────────────────────────────────────────────────────────────┘
```

---

## 📦 Implementation Phases

### **PHASE 1: Backend Setup & Inference Pipeline**

#### 1.1 Environment Configuration
**Deliverable**: `backend/environment_setup.md` + dependency files

**Tasks**:
- [ ] Create Python virtual environment (venv or conda)
- [ ] Install TensorFlow 2.15.x with GPU support (if available)
- [ ] Install additional dependencies:
  - `flask` or `fastapi` (API framework)
  - `pillow` (image processing)
  - `numpy` (numerical operations)
  - `scikit-image` (PSNR/SSIM metrics)
  - `python-dotenv` (environment variables)
  - `cors` (for frontend cross-origin requests)

**Requirements File**: `requirements.txt`
```
tensorflow==2.15.x
flask==3.0.x OR fastapi==0.x
pillow>=10.0.0
numpy>=1.24.0
scikit-image>=0.21.0
python-dotenv>=1.0.0
flask-cors>=4.0.0 (if using Flask)
uvicorn>=0.24.0 (if using FastAPI)
```

#### 1.2 Inference Module
**Deliverable**: `backend/inference.py`

**Key Components**:

**a) Model Loading Manager**
- Load MAXIM-S2 SavedModel from `maxim_savedmodel/`
- Load trained adapter weights from `adapter_best.weights.h5`
- Implement caching to load models once (not per request)
- Error handling for missing model files

**b) Image Preprocessing**
- Input validation (file type, size, format)
- Load image using PIL (supports JPG, PNG, BMP, etc.)
- Resize to 256×256 (bilinear interpolation)
- Normalize to [0, 1] float32 range
- Convert to tensor batch format [1, 256, 256, 3]

**c) Inference Function**
- Execute frozen MAXIM-S2 backbone prediction
- Get baseline dehaized estimate
- Apply trained adapter for refinement
- Clip output to valid range [0, 1]
- Denormalize to [0, 255] uint8
- Return PIL Image object

**d) Batch Processing**
- Support single image inference
- Optional: Support batch inference for multiple images
- Handle memory management for large batches

**Function Signatures**:
```
load_models(model_path, adapter_path) → (base_model, adapter)
preprocess_image(image_path) → torch.Tensor
inference(image_tensor, base_model, adapter) → np.ndarray
postprocess_output(output_array) → PIL.Image
process_single_image(image_path, models) → PIL.Image
```

#### 1.3 Test Inference Script
**Deliverable**: `backend/test_inference.py`

**Purpose**: Standalone test script to verify inference works before API integration

**Functionality**:
- Load test image from `data/val/input/`
- Run inference
- Save output to `results/test_output.jpg`
- Display processing time
- Verify output shape and value ranges

**Execution**: 
```bash
python backend/test_inference.py --image "data/val/input/0010.jpg"
```

---

### **PHASE 2: Metrics Calculation Module**

#### 2.1 Metrics Calculation Module
**Deliverable**: `backend/metrics.py`

**Key Components**:

**a) PSNR (Peak Signal-to-Noise Ratio)**
- Formula: 20 × log₁₀(MAX / √MSE)
  - MAX = 255 (for 8-bit images)
  - MSE = Mean Squared Error between images
- Range: Higher is better (typical: 20-40 dB)
- Use: `skimage.metrics.peak_signal_noise_ratio()`
- Input: Dehazed image vs Ground truth (or hazy vs dehazed)

**b) SSIM (Structural Similarity Index)**
- Formula: Compares luminance, contrast, structure
- Range: -1 to 1 (higher is better, 1 = identical)
- Use: `skimage.metrics.structural_similarity()`
- Input: Dehazed image vs Ground truth (or hazy vs dehazed)
- Configuration: data_range=255, channel_axis=2 (for RGB)

**c) Additional Metrics (Optional)**
- MSE (Mean Squared Error)
- RMSE (Root Mean Squared Error)
- Difference maps visualization

**Function Signatures**:
```
calculate_psnr(image1, image2) → float
calculate_ssim(image1, image2) → float
calculate_metrics(hazy, dehazed, ground_truth=None) → dict
visualize_difference(image1, image2) → PIL.Image
```

#### 2.2 Validation Tests
**Deliverable**: `backend/test_metrics.py`

**Tests**:
- [ ] Test PSNR with identical images (should be inf)
- [ ] Test SSIM with identical images (should be 1.0)
- [ ] Test with slightly different images (verify reasonable values)
- [ ] Test with different image sizes (ensure proper handling)

**Comparison Cases**:
1. **Hazy vs Dehazed**: Shows improvement from processing
2. **Hazy vs Ground Truth**: Shows how far hazy image is from clean
3. **Dehazed vs Ground Truth**: Shows inference quality

---

### **PHASE 3: Backend API Development**

#### 3.1 API Server Setup
**Deliverable**: `backend/app.py` (Flask) or `backend/main.py` (FastAPI)

**Framework Choice**: **FastAPI recommended**
- Advantages: Async support, automatic API documentation, faster
- File upload handling built-in
- Better for concurrent requests

**Alternative**: Flask
- Simpler to learn
- Sufficient for moderate traffic
- Good for prototyping

#### 3.2 REST API Endpoints

**Endpoint 1: Health Check**
```
GET /api/health
Response:
{
  "status": "ok",
  "models_loaded": true,
  "version": "1.0"
}
```

**Endpoint 2: Inference (Hazy → Dehazed)**
```
POST /api/dehaze
Content-Type: multipart/form-data

Request:
- file: <binary image file>

Response:
{
  "success": true,
  "dehazed_image": "<base64 encoded image>",
  "processing_time_ms": 245,
  "input_size": [H, W],
  "output_size": [256, 256]
}
```

**Endpoint 3: Inference with Metrics (Hazy + Optional Ground Truth)**
```
POST /api/dehaze-with-metrics
Content-Type: multipart/form-data

Request:
- hazy_image: <binary image file>
- ground_truth: <optional binary image file>

Response:
{
  "success": true,
  "dehazed_image": "<base64 encoded image>",
  "metrics": {
    "psnr": {
      "hazy_vs_dehazed": 25.3,
      "dehazed_vs_ground_truth": 28.5
    },
    "ssim": {
      "hazy_vs_dehazed": 0.82,
      "dehazed_vs_ground_truth": 0.87
    }
  },
  "processing_time_ms": 300,
  "has_ground_truth": true
}
```

**Endpoint 4: Batch Processing (Optional)**
```
POST /api/dehaze-batch
Content-Type: multipart/form-data

Request:
- files: <multiple image files>

Response:
{
  "success": true,
  "processed_count": 5,
  "failed_count": 0,
  "results": [
    {
      "filename": "image1.jpg",
      "dehazed_image": "<base64>",
      "success": true
    },
    ...
  ]
}
```

#### 3.3 Error Handling
**Deliverable**: Comprehensive error responses

**Error Cases**:
- Invalid file format (not image)
- File too large (set limit: 10MB)
- Unsupported image format
- Model loading failure
- Out of memory during processing
- Invalid ground truth image

**Standard Error Response**:
```json
{
  "success": false,
  "error": "Error message",
  "error_code": "INVALID_FILE_FORMAT",
  "status_code": 400
}
```

#### 3.4 Configuration Management
**Deliverable**: `backend/.env` and `backend/config.py`

**Configuration Variables**:
```
FLASK_ENV=production
FLASK_DEBUG=False
API_PORT=5000
API_HOST=0.0.0.0
MAX_FILE_SIZE=10485760  # 10MB in bytes
UPLOAD_FOLDER=./uploads
RESULTS_FOLDER=./results
MODEL_PATH=./maxim_savedmodel
ADAPTER_PATH=./adapter_best.weights.h5
ENABLE_CORS=True
CORS_ORIGINS=["http://localhost:3000", "http://localhost:8080"]
```

#### 3.5 Logging & Monitoring
**Deliverable**: `backend/logger.py`

**Features**:
- Structured logging (timestamp, level, message)
- Log file rotation
- API request/response logging
- Error stack traces
- Performance metrics (processing time per request)

**Log Levels**: DEBUG, INFO, WARNING, ERROR, CRITICAL

---

### **PHASE 4: Frontend Development**

#### 4.1 Tech Stack Decision
**Recommended**: React.js + TypeScript
- Modern, component-based
- Strong ecosystem for file handling
- Real-time UI updates
- Good for progressive enhancement

**Alternative**: Vue.js (simpler learning curve) or vanilla HTML/CSS/JS (lightest weight)

#### 4.2 Frontend Structure
**Deliverable**: `frontend/` directory

```
frontend/
├── public/
│   ├── index.html
│   └── favicon.ico
├── src/
│   ├── components/
│   │   ├── ImageUpload.jsx         # Drag-drop component
│   │   ├── ImagePreview.jsx        # Display before/after
│   │   ├── MetricsDisplay.jsx      # PSNR/SSIM scores
│   │   └── LoadingSpinner.jsx      # Processing indicator
│   ├── services/
│   │   └── api.js                  # Backend API calls
│   ├── styles/
│   │   ├── main.css
│   │   └── components.css
│   ├── App.jsx
│   └── index.js
├── package.json
└── .env
```

#### 4.3 User Interface Components

**a) Drag-Drop Upload Area**
```
┌─────────────────────────────────┐
│     Drop Image Here Or          │
│     Click To Select             │
│                                 │
│     (Accepts JPG, PNG, BMP)     │
└─────────────────────────────────┘
```
- Accept: JPG, PNG, BMP, WEBP, TIFF
- File size validation (max 10MB)
- Visual feedback on hover/drag

**b) Optional Ground Truth Upload**
```
┌─────────────────────────────────┐
│  Upload Ground Truth (Optional) │
│  [Choose File] or Drag & Drop   │
│                                 │
│  (For PSNR/SSIM calculation)    │
└─────────────────────────────────┘
```

**c) Processing Status**
```
┌─────────────────────────────────┐
│     Processing...               │
│     ⟳ (animated spinner)        │
│     Estimated time: 3-5 seconds │
└─────────────────────────────────┘
```

**d) Results Display**
```
┌─────────────────────────────────────────┐
│  BEFORE (Hazy)    │    AFTER (Dehazed)  │
│                   │                     │
│  [Image Preview]  │  [Image Preview]    │
│                   │                     │
│  Resolution: HxW  │  Resolution: 256x256│
└─────────────────────────────────────────┘

Optional Metrics Panel (if ground truth provided):
┌─────────────────────────────────────────┐
│ QUALITY METRICS                         │
├─────────────────────────────────────────┤
│ PSNR:                                   │
│   • Hazy vs Dehazed:  25.3 dB           │
│   • Dehazed vs GT:    28.5 dB           │
│                                         │
│ SSIM:                                   │
│   • Hazy vs Dehazed:  0.82              │
│   • Dehazed vs GT:    0.87              │
└─────────────────────────────────────────┘

Action Buttons:
┌──────────────┬──────────────┬─────────────┐
│ Download     │ Compare View │ New Image   │
│ Dehazed      │              │             │
└──────────────┴──────────────┴─────────────┘
```

#### 4.4 Key Features

**a) Image Comparison Slider**
- Draggable slider to compare before/after
- Interactive visualization

**b) Download Functionality**
- Download dehazed image (JPG/PNG options)
- Download metrics report (JSON/PDF)

**c) Processing History**
- Recent uploads list
- Quick re-process option
- Clear history button

**d) Responsive Design**
- Mobile-friendly (tablet & desktop)
- Touch-friendly drag-drop
- Adaptive image display

#### 4.5 Error Handling (Frontend)
- File validation before upload
- Network error handling
- User-friendly error messages
- Retry mechanism

#### 4.6 Performance Optimization
- Image compression for preview
- Progressive image loading
- Lazy loading for history
- Minimize API calls
- Caching results (browser storage)

---

### **PHASE 5: Integration & Testing**

#### 5.1 Backend-Frontend Integration
**Deliverable**: Integration tests

**Tasks**:
- [ ] Test CORS configuration
- [ ] Verify API endpoint accessibility
- [ ] Test file upload/download
- [ ] Test base64 image encoding/decoding
- [ ] Verify response formats
- [ ] Test error scenarios

#### 5.2 End-to-End Testing
**Deliverable**: E2E test suite

**Test Scenarios**:
1. Upload hazy image → Receive dehazed output
2. Upload hazy + ground truth → Receive dehazed + metrics
3. Invalid file upload → Error message
4. Large file upload → Size validation
5. Network timeout → Retry mechanism
6. Rapid successive uploads → Queue handling

#### 5.3 Performance Testing
**Deliverable**: Performance report

**Metrics**:
- Average inference time per image
- API response time (P50, P95, P99)
- Memory usage during processing
- CPU/GPU utilization
- Concurrent request handling

**Load Testing**: Test with multiple simultaneous requests

#### 5.4 Browser Compatibility
- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)
- Mobile browsers

---

### **PHASE 6: Deployment & Optimization**

#### 6.1 Backend Deployment Options

**Option A: Cloud Platforms**
- **AWS**: EC2 + S3 for image storage
- **Google Cloud**: Cloud Run for serverless, Cloud Storage
- **Azure**: App Service + Blob Storage
- **Heroku**: Simple deployment (limited free tier)

**Option B: On-Premise**
- Docker containerization
- Docker Compose for local development
- Kubernetes for scaling (optional)

#### 6.2 Docker Setup
**Deliverable**: `Dockerfile` and `docker-compose.yml`

**Dockerfile (Backend)**:
```
FROM tensorflow/tensorflow:latest-gpu
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "app.py"]
```

**docker-compose.yml**:
```
version: '3.8'
services:
  backend:
    build: ./backend
    ports:
      - "5000:5000"
    volumes:
      - ./uploads:/app/uploads
      - ./results:/app/results
  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    depends_on:
      - backend
```

#### 6.3 Frontend Deployment
- **Static Hosting**: Vercel, Netlify, GitHub Pages
- **Docker Container**: Same as backend
- **CDN**: CloudFlare for caching
- **Environment Variables**: API endpoint configuration

#### 6.4 Database (Optional)
- Store processing history
- User accounts (future)
- Results caching
- **Options**: SQLite (development), PostgreSQL (production)

#### 6.5 Security Measures
- [ ] Input validation (file type, size, content)
- [ ] Rate limiting (prevent abuse)
- [ ] CORS configuration
- [ ] HTTPS/TLS encryption
- [ ] Authentication (if multi-user)
- [ ] File sanitization
- [ ] XSS prevention
- [ ] CSRF protection

---

## 🔧 Environment & Requirements

### Development Environment Setup

#### Backend Prerequisites
```
OS: Windows 10/11, Linux, macOS
Python: 3.8 - 3.11
Memory: 8GB RAM minimum (16GB recommended for GPU)
GPU: NVIDIA GPU with CUDA support (optional but recommended)
Storage: 2GB for models + data
```

#### GPU Setup (Recommended for Fast Inference)
```
NVIDIA CUDA Toolkit: 11.x or 12.x
NVIDIA cuDNN: 8.x
TensorFlow GPU support (automatic with tensorflow-gpu)
```

#### Python Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/macOS
python3 -m venv venv
source venv/bin/activate
```

#### Install Dependencies
```bash
pip install -r requirements.txt
```

#### Frontend Prerequisites
```
Node.js: 16.x or higher
npm: 8.x or yarn: 3.x
npm install (installs dependencies from package.json)
```

### Production Environment
```
Server OS: Linux (Ubuntu 20.04 LTS recommended)
Python: Same as development
Docker: For containerization
Docker Compose: For multi-container orchestration
PostgreSQL: For database (optional)
Nginx: For reverse proxy
SSL Certificate: For HTTPS
```

---

## 📊 Project Timeline & Milestones

| Phase | Component | Duration | Dependencies |
|-------|-----------|----------|--------------|
| 1 | Inference Pipeline | 1-2 weeks | None |
| 2 | Metrics Module | 3-4 days | Phase 1 |
| 3 | Backend API | 2-3 weeks | Phase 1, 2 |
| 4 | Frontend Development | 2-3 weeks | Phase 3 |
| 5 | Testing & Integration | 1-2 weeks | Phase 3, 4 |
| 6 | Deployment | 1 week | Phase 5 |
| **TOTAL** | **Full Project** | **8-10 weeks** | - |

---

## ✅ Deliverables Checklist

### Backend
- [ ] `backend/inference.py` - Image processing & inference
- [ ] `backend/metrics.py` - PSNR/SSIM calculation
- [ ] `backend/app.py` or `backend/main.py` - API server
- [ ] `backend/config.py` - Configuration management
- [ ] `backend/logger.py` - Logging setup
- [ ] `backend/test_inference.py` - Inference testing
- [ ] `backend/test_metrics.py` - Metrics testing
- [ ] `requirements.txt` - Python dependencies
- [ ] `.env.example` - Environment template
- [ ] `Dockerfile` - Container setup
- [ ] `backend/README.md` - Backend documentation

### Frontend
- [ ] React/Vue app scaffolding
- [ ] `src/components/ImageUpload.jsx` - Drag-drop component
- [ ] `src/components/ImagePreview.jsx` - Before/after display
- [ ] `src/components/MetricsDisplay.jsx` - Metrics visualization
- [ ] `src/services/api.js` - API integration
- [ ] Styling & responsive design
- [ ] `package.json` - Dependencies
- [ ] `.env.example` - Environment template
- [ ] `Dockerfile` - Frontend container
- [ ] `frontend/README.md` - Frontend documentation

### DevOps & Documentation
- [ ] `docker-compose.yml` - Multi-container setup
- [ ] `DEPLOYMENT.md` - Deployment guide
- [ ] `ARCHITECTURE.md` - System architecture
- [ ] `API_DOCUMENTATION.md` - API reference
- [ ] `TESTING.md` - Testing guide

---

## 🚀 Quick Start Workflow (Post-Implementation)

### Development Mode
```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py  # Runs on http://localhost:5000

# Frontend (in new terminal)
cd frontend
npm install
npm start  # Runs on http://localhost:3000
```

### Docker Mode
```bash
docker-compose up --build
# Backend: http://localhost:5000
# Frontend: http://localhost:3000
```

### Production Deployment
```bash
# Build images
docker build -t dehaze-backend ./backend
docker build -t dehaze-frontend ./frontend

# Push to registry (AWS ECR, Docker Hub, etc.)
docker push dehaze-backend:latest
docker push dehaze-frontend:latest

# Deploy (Kubernetes, AWS ECS, etc.)
# Follow cloud platform documentation
```

---

## 📝 Additional Considerations

### Scalability
- **Horizontal Scaling**: Multiple backend instances behind load balancer
- **Caching**: Redis for storing recent results
- **Async Processing**: Queue system (Celery, RQ) for heavy workloads
- **Image Storage**: S3/Cloud Storage for scalable file handling

### Monitoring & Analytics
- Track inference times
- Monitor API performance
- Collect user feedback
- Usage statistics
- Error tracking (Sentry)

### Future Enhancements
- User accounts & authentication
- Processing history database
- Batch processing queue
- API key system for third-party integration
- Model selection (choose different pre-trained models)
- Comparison with other dehazing methods
- Real-time WebSocket updates for long-running tasks
- Image gallery of processed images

### Security Considerations
- Validate uploaded files (content, not just extension)
- Sanitize file names
- Implement rate limiting
- Use HTTPS in production
- Store sensitive data in environment variables
- Implement authentication for private deployments
- Regular security audits

---

## 🔍 Key Technical Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| **API Framework** | FastAPI | Async support, performance, auto-docs |
| **Frontend Framework** | React | Large ecosystem, component reusability |
| **Containerization** | Docker | Consistency across environments |
| **Metrics Library** | scikit-image | Standard, well-tested, minimal deps |
| **Image Format** | Base64 encoding | Easy transmission via JSON, no extra endpoints |
| **Model Loading** | On-startup caching | Avoid repeated loading per request |
| **Inference Approach** | Batch size 1 | Sufficient for current use case |

---

## 📚 Reference Implementation Structure

```
dehaze-project/
├── backend/
│   ├── app.py                    # Main API application
│   ├── inference.py              # Model inference logic
│   ├── metrics.py                # PSNR/SSIM calculations
│   ├── config.py                 # Configuration
│   ├── logger.py                 # Logging setup
│   ├── test_inference.py         # Standalone inference test
│   ├── test_metrics.py           # Metrics unit tests
│   ├── requirements.txt
│   ├── Dockerfile
│   ├── .env.example
│   ├── .gitignore
│   ├── maxim_savedmodel/         # Pre-trained model (copy from original)
│   ├── adapter_best.weights.h5   # Trained adapter (copy from original)
│   ├── uploads/                  # Temporary upload storage
│   └── README.md
│
├── frontend/
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── components/
│   │   ├── services/
│   │   ├── styles/
│   │   ├── App.jsx
│   │   └── index.js
│   ├── package.json
│   ├── Dockerfile
│   ├── .env.example
│   ├── .gitignore
│   └── README.md
│
├── docker-compose.yml
├── .gitignore
├── PLAN.md                       # This file
├── ARCHITECTURE.md               # System design details
├── API_DOCUMENTATION.md          # API specs
├── DEPLOYMENT.md                 # Deployment instructions
└── README.md                     # Main project README
```

---

## 🎯 Success Criteria

✅ **Inference Module**
- Accepts hazy images
- Outputs dehazed images
- Processing time < 1 second per image
- Preserves image quality

✅ **Metrics Module**
- Calculates accurate PSNR scores
- Calculates accurate SSIM scores
- Handles ground truth comparison
- Generates comparison visualizations

✅ **Backend API**
- Responds to all endpoints within 2 seconds
- Handles concurrent requests
- Proper error handling & validation
- CORS enabled for frontend

✅ **Frontend Interface**
- Intuitive drag-drop interface
- Real-time feedback
- Displays results clearly
- Mobile responsive
- Download functionality works

✅ **Integration**
- Complete workflow: upload → process → results
- No manual steps required
- Metrics automatically calculated (if GT provided)
- Error handling prevents crashes

✅ **Production Ready**
- Dockerized setup
- Documented deployment steps
- Security measures implemented
- Performance optimized

---

## 📞 Support & Troubleshooting

### Common Issues & Solutions

**GPU Memory Errors**
- Reduce batch size (already 1, can't reduce)
- Run on CPU (slower but works)
- Clear TensorFlow cache

**CORS Errors**
- Verify CORS headers in API responses
- Check frontend API endpoint configuration
- Ensure backend allows frontend origin

**Image Conversion Errors**
- Verify image format support
- Check file size limits
- Ensure RGB conversion success

**Metric Calculation Errors**
- Verify both images same size (automatic resize in code)
- Check image value ranges [0, 255]
- Ensure images are 3-channel RGB

---

## 📖 Documentation to Generate

1. **ARCHITECTURE.md** - Detailed system architecture
2. **API_DOCUMENTATION.md** - Complete API reference
3. **BACKEND_SETUP.md** - Backend installation guide
4. **FRONTEND_SETUP.md** - Frontend installation guide
5. **DEPLOYMENT.md** - Production deployment guide
6. **TESTING.md** - Testing procedures
7. **TROUBLESHOOTING.md** - Common issues & fixes

---

## 🎓 Learning Resources

- TensorFlow SavedModel: https://www.tensorflow.org/guide/saved_model
- FastAPI Documentation: https://fastapi.tiangolo.com/
- React Documentation: https://react.dev/
- scikit-image SSIM: https://scikit-image.org/docs/stable/api/skimage.metrics.html#skimage.metrics.structural_similarity

---

**Plan Version**: 1.0  
**Last Updated**: January 20, 2026  
**Status**: Ready for Implementation
