// Image Upload Component with Drag-Drop
// Allows users to upload hazy images with optional ground truth

import React, { useState } from 'react';
import '../styles/components.css';

const ImageUpload = ({ onImagesSelected, isProcessing }) => {
  const [dragActive, setDragActive] = useState(false);
  const [hazyFile, setHazyFile] = useState(null);
  const [groundTruthFile, setGroundTruthFile] = useState(null);

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (!isProcessing) {
      setDragActive(e.type === 'dragenter' || e.type === 'dragover');
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);

    if (isProcessing) return;

    const files = e.dataTransfer.files;
    if (files && files.length > 0) {
      const file = files[0];
      if (file.type.startsWith('image/')) {
        setHazyFile(file);
      } else {
        alert('Please drop an image file');
      }
    }
  };

  const handleFileSelect = (e, isGroundTruth = false) => {
    const files = e.target.files;
    if (files && files.length > 0) {
      const file = files[0];
      if (file.type.startsWith('image/')) {
        if (isGroundTruth) {
          setGroundTruthFile(file);
        } else {
          setHazyFile(file);
        }
      } else {
        alert('Please select an image file');
      }
    }
  };

  const handleSubmit = () => {
    if (hazyFile) {
      onImagesSelected(hazyFile, groundTruthFile);
    } else {
      alert('Please select a hazy image first');
    }
  };

  return (
    <div className="upload-container glass-panel">
      <div className="upload-section">
        <h2>Restore Image Quality</h2>

        {/* Hazy Image Upload */}
        <div
          className={`drag-drop-area ${dragActive ? 'active' : ''}`}
          onDragEnter={handleDrag}
          onDragLeave={handleDrag}
          onDragOver={handleDrag}
          onDrop={handleDrop}
        >
          <input
            type="file"
            id="hazy-file"
            accept="image/*"
            onChange={(e) => handleFileSelect(e, false)}
            disabled={isProcessing}
            style={{ display: 'none' }}
          />
          <label htmlFor="hazy-file" className="drag-drop-label">
            <div className="icon">
              <svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
                <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
                <polyline points="17 8 12 3 7 8"></polyline>
                <line x1="12" y1="3" x2="12" y2="15"></line>
              </svg>
            </div>
            <h3>Drop Hazy Image Here</h3>
            <p>or click to target a local file</p>
            <small>Supports JPG, PNG, WEBP, BMP, TIFF</small>
          </label>
        </div>

        {hazyFile && (
          <div className="file-info">
            <span className="file-name">
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                <polyline points="14 2 14 8 20 8"></polyline>
                <line x1="12" y1="18" x2="12" y2="12"></line>
                <line x1="9" y1="15" x2="15" y2="15"></line>
              </svg>
              {hazyFile.name}
            </span>
            <button
              onClick={() => setHazyFile(null)}
              disabled={isProcessing}
              className="remove-btn"
              title="Remove file"
            >
              <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <line x1="18" y1="6" x2="6" y2="18"></line>
                <line x1="6" y1="6" x2="18" y2="18"></line>
              </svg>
            </button>
          </div>
        )}

        {/* Ground Truth Image Upload (Optional) */}
        <div className="optional-section">
          <h3>Ground Truth / Target Image</h3>
          <p>Upload the pristine image to compute detailed algorithmic quality metrics (PSNR, SSIM, MSE).</p>

          <div className="ground-truth-upload">
            <input
              type="file"
              id="gt-file"
              accept="image/*"
              onChange={(e) => handleFileSelect(e, true)}
              disabled={isProcessing}
              style={{ display: 'none' }}
            />
            <label htmlFor="gt-file" className={`file-select-label ${groundTruthFile ? 'has-file' : ''}`}>
              {groundTruthFile ? (
                <>
                  <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                    <polyline points="20 6 9 17 4 12"></polyline>
                  </svg>
                  <span>{groundTruthFile.name}</span>
                </>
              ) : (
                <>
                  <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                    <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
                    <circle cx="8.5" cy="8.5" r="1.5"></circle>
                    <polyline points="21 15 16 10 5 21"></polyline>
                  </svg>
                  <span>Attach Clean Target Image</span>
                </>
              )}
            </label>

            {groundTruthFile && (
              <button
                onClick={() => setGroundTruthFile(null)}
                disabled={isProcessing}
                className="remove-btn-small"
                title="Remove target image"
              >
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                  <path d="M3 6h18"></path>
                  <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
                </svg>
              </button>
            )}
          </div>
        </div>

        {/* Submit Button */}
        <button
          onClick={handleSubmit}
          disabled={!hazyFile || isProcessing}
          className="submit-btn"
        >
          {isProcessing ? (
            <>
              Initializing Network
              <div style={{ display: 'flex', gap: '4px', marginLeft: '6px' }}>
                <span style={{ animation: 'pulse 1s infinite' }}>.</span>
                <span style={{ animation: 'pulse 1s infinite 0.2s' }}>.</span>
                <span style={{ animation: 'pulse 1s infinite 0.4s' }}>.</span>
              </div>
            </>
          ) : (
            <>
              <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <polygon points="5 3 19 12 5 21 5 3"></polygon>
              </svg>
              Engage Dehazing Network
            </>
          )}
        </button>
      </div>
    </div>
  );
};

export default ImageUpload;
