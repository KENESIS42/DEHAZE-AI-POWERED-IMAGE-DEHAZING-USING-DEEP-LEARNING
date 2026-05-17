// Image Preview Component
// Displays before/after images side by side

import React from 'react';
import '../styles/components.css';

const ImagePreview = ({ hazyImage, dehazedImage, metrics, isLoading }) => {
  const downloadImage = (imageSrc, filename) => {
    const link = document.createElement('a');
    link.href = imageSrc;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  if (isLoading) {
    return (
      <div className="preview-container glass-panel loading-state">
        <div className="spinner-container">
          <div className="spinner"></div>
        </div>
        <div>
          <h3>Enhancing Image Quality</h3>
          <p>Processing via MAXIM-S2 Engine...</p>
        </div>
      </div>
    );
  }

  if (!dehazedImage) {
    return null;
  }

  return (
    <div className="preview-container">
      <div className="preview-header">
        <h3>Restoration Complete</h3>
        <p>Your enhanced image is ready for review.</p>
      </div>

      <div className="image-comparison">
        <div className="image-card">
          <div className="image-card-header">
            <h4>Original</h4>
            <span className="badge">Degraded</span>
          </div>
          <div className="image-wrapper">
            {hazyImage && (
              <img src={hazyImage} alt="Hazy input" className="preview-image" />
            )}
          </div>
        </div>

        <div className="comparison-divider">
          <div className="comparison-arrow">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
              <line x1="5" y1="12" x2="19" y2="12"></line>
              <polyline points="12 5 19 12 12 19"></polyline>
            </svg>
          </div>
        </div>

        <div className="image-card">
          <div className="image-card-header">
            <h4>Restored</h4>
            <span className="badge blue">Enhanced</span>
          </div>
          <div className="image-wrapper">
            <img
              src={dehazedImage}
              alt="Dehazed output"
              className="preview-image"
            />
          </div>
        </div>
      </div>

      {/* Metrics Display */}
      {metrics && (
        <div className="metrics-panel">
          <div className="metrics-header">
            <svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
              <path d="M12 20V10"></path>
              <path d="M18 20V4"></path>
              <path d="M6 20v-4"></path>
            </svg>
            <h4>Algorithm Quality Metrics</h4>
          </div>

          <div className="metrics-grid">
            {/* PSNR Section */}
            <div className="metric-box">
              <h5>
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="8" x2="12" y2="16"></line><line x1="8" y1="12" x2="16" y2="12"></line></svg>
                Peak Signal/Noise
              </h5>
              {metrics.psnr.hazy_vs_dehazed !== undefined && (
                <div className="metric-item">
                  <label>Original vs Restored</label>
                  <span className="value">{metrics.psnr.hazy_vs_dehazed}</span>
                </div>
              )}
              {metrics.psnr.dehazed_vs_ground_truth !== undefined && (
                <div className="metric-item">
                  <label>Restored vs Target</label>
                  <span className="value">{metrics.psnr.dehazed_vs_ground_truth}</span>
                </div>
              )}
              {metrics.psnr.hazy_vs_ground_truth !== undefined && (
                <div className="metric-item">
                  <label>Original vs Target</label>
                  <span className="value">{metrics.psnr.hazy_vs_ground_truth}</span>
                </div>
              )}
            </div>

            {/* SSIM Section */}
            <div className="metric-box">
              <h5>
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"></path><polyline points="3.27 6.96 12 12.01 20.73 6.96"></polyline><line x1="12" y1="22.08" x2="12" y2="12"></line></svg>
                Structural Similarity
              </h5>
              {metrics.ssim.hazy_vs_dehazed !== undefined && (
                <div className="metric-item">
                  <label>Original vs Restored</label>
                  <span className="value">{metrics.ssim.hazy_vs_dehazed}</span>
                </div>
              )}
              {metrics.ssim.dehazed_vs_ground_truth !== undefined && (
                <div className="metric-item">
                  <label>Restored vs Target</label>
                  <span className="value">{metrics.ssim.dehazed_vs_ground_truth}</span>
                </div>
              )}
              {metrics.ssim.hazy_vs_ground_truth !== undefined && (
                <div className="metric-item">
                  <label>Original vs Target</label>
                  <span className="value">{metrics.ssim.hazy_vs_ground_truth}</span>
                </div>
              )}
            </div>

            {/* MSE Section */}
            <div className="metric-box">
              <h5>
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"></polyline></svg>
                Mean Squared Error
              </h5>
              {metrics.mse.hazy_vs_dehazed !== undefined && (
                <div className="metric-item">
                  <label>Original vs Restored</label>
                  <span className="value">{metrics.mse.hazy_vs_dehazed}</span>
                </div>
              )}
              {metrics.mse.dehazed_vs_ground_truth !== undefined && (
                <div className="metric-item">
                  <label>Restored vs Target</label>
                  <span className="value">{metrics.mse.dehazed_vs_ground_truth}</span>
                </div>
              )}
              {metrics.mse.hazy_vs_ground_truth !== undefined && (
                <div className="metric-item">
                  <label>Original vs Target</label>
                  <span className="value">{metrics.mse.hazy_vs_ground_truth}</span>
                </div>
              )}
            </div>
          </div>
        </div>
      )}

      {/* Action Buttons */}
      <div className="action-buttons">
        <button
          onClick={() => downloadImage(dehazedImage, 'dehazed_output.jpg')}
          className="action-btn primary"
        >
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
            <polyline points="7 10 12 15 17 10"></polyline>
            <line x1="12" y1="15" x2="12" y2="3"></line>
          </svg>
          Export Restored Image
        </button>

        {metrics && (
          <button
            onClick={() => {
              const metricsJSON = JSON.stringify(metrics, null, 2);
              const blob = new Blob([metricsJSON], { type: 'application/json' });
              const link = document.createElement('a');
              link.href = URL.createObjectURL(blob);
              link.download = 'metrics.json';
              link.click();
            }}
            className="action-btn"
          >
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
              <polyline points="14 2 14 8 20 8"></polyline>
              <line x1="16" y1="13" x2="8" y2="13"></line>
              <line x1="16" y1="17" x2="8" y2="17"></line>
              <polyline points="10 9 9 9 8 9"></polyline>
            </svg>
            Export Complete Report
          </button>
        )}
      </div>
    </div>
  );
};

export default ImagePreview;
