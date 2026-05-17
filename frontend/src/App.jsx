// Main App Component
// Orchestrates the entire dehazing workflow

import React, { useState, useEffect } from 'react';
import './styles/main.css';
import ImageUpload from './components/ImageUpload';
import ImagePreview from './components/ImagePreview';
import DehazeAPI from './services/api';

function App() {
  const [isProcessing, setIsProcessing] = useState(false);
  const [error, setError] = useState(null);
  const [apiReady, setApiReady] = useState(false);
  const [hazyImageSrc, setHazyImageSrc] = useState(null);
  const [dehazedImageSrc, setDehazedImageSrc] = useState(null);
  const [metrics, setMetrics] = useState(null);

  // Check API health on mount
  useEffect(() => {
    const checkAPI = async () => {
      try {
        await DehazeAPI.health();
        setApiReady(true);
        console.log('✓ API is ready');
      } catch (err) {
        setError('API server not available. Ensure backend is running.');
        console.error('API health check failed:', err);
      }
    };

    checkAPI();
  }, []);

  const handleImagesSelected = async (hazyFile, groundTruthFile) => {
    setIsProcessing(true);
    setError(null);
    setMetrics(null);

    try {
      // Display hazy image
      const hazyReader = new FileReader();
      hazyReader.onload = (e) => {
        setHazyImageSrc(e.target.result);
      };
      hazyReader.readAsDataURL(hazyFile);

      // Process with or without metrics
      let response;
      if (groundTruthFile) {
        response = await DehazeAPI.dehazeImageWithMetrics(hazyFile, groundTruthFile);
      } else {
        response = await DehazeAPI.dehazeImage(hazyFile);
      }

      if (response.success) {
        setDehazedImageSrc(response.dehazed_image);
        if (response.metrics) {
          setMetrics(response.metrics);
        }
        console.log(`✓ Processing completed in ${response.processing_time_ms}ms`);
      } else {
        setError('Processing failed. Please try again.');
      }
    } catch (err) {
      console.error('Error:', err);
      setError(err.message || 'An error occurred during processing');
    } finally {
      setIsProcessing(false);
    }
  };

  const handleNewImage = () => {
    setHazyImageSrc(null);
    setDehazedImageSrc(null);
    setMetrics(null);
    setError(null);
  };

  return (
    <div className="app">
      <div className="app-grid-overlay"></div>
      
      <header className="app-header">
        <div className="header-content">
          <div className="header-icon">
            <svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
              <polyline points="17 8 12 3 7 8"></polyline>
              <line x1="12" y1="3" x2="12" y2="15"></line>
            </svg>
          </div>
          <h1>Image Dehazing API</h1>
          <p>Instantly restore visibility to hazy, foggy, or low-contrast images using the MAXIM-S2 neural network model.</p>
          
          {apiReady ? (
            <span className="status-badge ready">System Online</span>
          ) : (
            <span className="status-badge error">System Offline</span>
          )}
        </div>
      </header>

      <main className="app-main">
        {error && (
          <div className="error-banner">
            <span>
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <circle cx="12" cy="12" r="10"></circle>
                <line x1="12" y1="8" x2="12" y2="12"></line>
                <line x1="12" y1="16" x2="12.01" y2="16"></line>
              </svg>
              {error}
            </span>
            <button onClick={() => setError(null)}>
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <line x1="18" y1="6" x2="6" y2="18"></line>
                <line x1="6" y1="6" x2="18" y2="18"></line>
              </svg>
            </button>
          </div>
        )}

        {!dehazedImageSrc ? (
          <ImageUpload
            onImagesSelected={handleImagesSelected}
            isProcessing={isProcessing}
          />
        ) : (
          <ImagePreview
            hazyImage={hazyImageSrc}
            dehazedImage={dehazedImageSrc}
            metrics={metrics}
            isLoading={isProcessing}
          />
        )}

        {dehazedImageSrc && (
          <div className="new-image-button-container">
            <button onClick={handleNewImage} className="new-image-btn">
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"></path>
                <path d="M3 3v5h5"></path>
              </svg>
              Process Another Image
            </button>
          </div>
        )}
      </main>

      <footer className="app-footer">
        <p>
          Powered by MAXIM-S2 Model with Custom Adapter | 
          <a href="#" target="_blank" rel="noopener noreferrer">View Documentation</a>
        </p>
      </footer>
    </div>
  );
}

export default App;
