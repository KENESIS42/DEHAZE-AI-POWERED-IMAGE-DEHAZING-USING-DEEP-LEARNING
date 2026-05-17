// Dehaze API Service
// Handles all backend API calls

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

class DehazeAPI {
  /**
   * Check API health
   */
  static async health() {
    try {
      const response = await fetch(`${API_BASE_URL}/api/health`);
      if (!response.ok) throw new Error('API health check failed');
      return await response.json();
    } catch (error) {
      console.error('Health check error:', error);
      throw error;
    }
  }

  /**
   * Dehaze single image
   * @param {File} file - Image file
   * @returns {Promise<Object>} Response with dehazed image and metadata
   */
  static async dehazeImage(file) {
    try {
      const formData = new FormData();
      formData.append('file', file);

      const response = await fetch(`${API_BASE_URL}/api/dehaze`, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Failed to dehaze image');
      }

      return await response.json();
    } catch (error) {
      console.error('Dehaze error:', error);
      throw error;
    }
  }

  /**
   * Dehaze image with optional metrics
   * @param {File} hazyFile - Hazy image file
   * @param {File} groundTruthFile - Optional ground truth file
   * @returns {Promise<Object>} Response with dehazed image and metrics
   */
  static async dehazeImageWithMetrics(hazyFile, groundTruthFile = null) {
    try {
      const formData = new FormData();
      formData.append('hazy_image', hazyFile);
      if (groundTruthFile) {
        formData.append('ground_truth', groundTruthFile);
      }

      const response = await fetch(`${API_BASE_URL}/api/dehaze-with-metrics`, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Failed to process image');
      }

      return await response.json();
    } catch (error) {
      console.error('Dehaze with metrics error:', error);
      throw error;
    }
  }

  /**
   * Get API info
   */
  static async getInfo() {
    try {
      const response = await fetch(`${API_BASE_URL}/api/info`);
      if (!response.ok) throw new Error('Failed to get API info');
      return await response.json();
    } catch (error) {
      console.error('API info error:', error);
      throw error;
    }
  }
}

export default DehazeAPI;
