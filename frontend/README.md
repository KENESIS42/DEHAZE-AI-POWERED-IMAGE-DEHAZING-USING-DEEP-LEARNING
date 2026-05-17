# Dehaze Frontend - Setup & Installation Guide

## Quick Start

### 1. Install Dependencies

```bash
# Navigate to frontend directory
cd frontend

# Install Node packages
npm install
```

### 2. Configuration

```bash
# Copy example environment file
copy .env.example .env
# Update .env with backend API URL if needed
```

### 3. Start Development Server

```bash
npm start
```

The frontend will open at `http://localhost:3000`

## Project Structure

```
frontend/
├── public/
│   └── index.html              # HTML entry point
├── src/
│   ├── components/
│   │   ├── ImageUpload.jsx     # Upload component
│   │   └── ImagePreview.jsx    # Results display
│   ├── services/
│   │   └── api.js              # Backend API calls
│   ├── styles/
│   │   ├── main.css            # Global styles
│   │   └── components.css      # Component styles
│   ├── App.jsx                 # Main app component
│   ├── index.js                # Entry point
│   └── index.css               # Global CSS
├── package.json                # Dependencies & scripts
├── .env.example                # Environment template
└── README.md                   # This file
```

## Available Scripts

```bash
# Start development server
npm start

# Build for production
npm run build

# Run tests
npm test

# Eject (one-way operation)
npm run eject
```

## Dependencies

- **react@18.2.0** - UI library
- **react-dom@18.2.0** - React DOM utilities
- **react-scripts@5.0.1** - Build tools

## Browser Support

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## Features

✓ Drag-drop image upload
✓ Optional ground truth image input
✓ Real-time image processing feedback
✓ Before/after image comparison
✓ Quality metrics display (PSNR, SSIM, MSE)
✓ Download dehazed image
✓ Download metrics report (JSON)
✓ Responsive mobile design

## Environment Variables

```env
# Backend API endpoint
REACT_APP_API_URL=http://localhost:5000
```

## Troubleshooting

### Port Already in Use
```bash
# Use different port
PORT=3001 npm start
```

### API Connection Errors
- Ensure backend is running on port 5000
- Check `REACT_APP_API_URL` in `.env`
- Verify CORS is enabled in backend

### Build Issues
```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
```

## Deployment

### Build for Production
```bash
npm run build
```

This creates an optimized production build in the `build/` directory.

### Deploy to Vercel/Netlify
1. Push code to GitHub
2. Connect repository to Vercel/Netlify
3. Set `REACT_APP_API_URL` environment variable
4. Deploy!

### Docker Deployment
```bash
docker build -t dehaze-frontend .
docker run -p 3000:3000 dehaze-frontend
```
