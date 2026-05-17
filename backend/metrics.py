"""Metrics calculation module for image quality assessment."""
import numpy as np
from PIL import Image
from skimage.metrics import peak_signal_noise_ratio, structural_similarity


def load_image_array(image_path_or_pil):
    """
    Load image as numpy array in [0, 255] uint8 format.
    
    Args:
        image_path_or_pil: Path to image or PIL Image object
        
    Returns:
        numpy array [H, W, 3] uint8
    """
    if isinstance(image_path_or_pil, str):
        img = Image.open(image_path_or_pil).convert("RGB")
    else:
        img = image_path_or_pil.convert("RGB")
    
    return np.array(img)


def ensure_same_size(img1, img2):
    """
    Resize images to match the smaller one.
    Handles both PIL Images and Numpy Arrays (Float/Int).
    """
    # Helper to convert input to PIL Image safely
    def to_pil(img):
        if isinstance(img, Image.Image):
            return img
        
        # If it's a numpy array
        arr = np.array(img)
        
        # If it's floating point (0.0-1.0), convert to 0-255 uint8
        if arr.dtype.kind == 'f':
            arr = (np.clip(arr, 0, 1) * 255).astype(np.uint8)
        # If it's integer but not uint8, cast it
        elif arr.dtype != np.uint8:
            arr = arr.astype(np.uint8)
            
        return Image.fromarray(arr)

    # Convert both to PIL first
    pil1 = to_pil(img1)
    pil2 = to_pil(img2)
    
    # Get dimensions
    w1, h1 = pil1.size
    w2, h2 = pil2.size
    
    # If sizes match, return as-is (converted to arrays for math)
    if (w1, h1) == (w2, h2):
        return np.array(pil1), np.array(pil2)
        
    # Resize the larger one to match the smaller one
    if w1 * h1 < w2 * h2:
        pil2 = pil2.resize((w1, h1), Image.Resampling.BICUBIC)
    else:
        pil1 = pil1.resize((w2, h2), Image.Resampling.BICUBIC)
        
    return np.array(pil1), np.array(pil2)


def calculate_psnr(image1_path, image2_path):
    """
    Calculate Peak Signal-to-Noise Ratio (PSNR).
    
    Formula: PSNR = 20 * log10(MAX / sqrt(MSE))
    where MAX = 255 for 8-bit images
    
    Range: Higher is better (typical: 20-40 dB)
    
    Args:
        image1_path: Path to first image (or PIL Image)
        image2_path: Path to second image (or PIL Image)
        
    Returns:
        float: PSNR value in dB
    """
    img1 = load_image_array(image1_path)
    img2 = load_image_array(image2_path)
    
    img1, img2 = ensure_same_size(img1, img2)
    
    # Calculate PSNR
    psnr = peak_signal_noise_ratio(img1, img2, data_range=255)
    
    return float(psnr)


def calculate_ssim(image1_path, image2_path):
    """
    Calculate Structural Similarity Index (SSIM).
    
    Range: -1 to 1 (higher is better, 1 = identical)
    
    Args:
        image1_path: Path to first image (or PIL Image)
        image2_path: Path to second image (or PIL Image)
        
    Returns:
        float: SSIM value
    """
    img1 = load_image_array(image1_path)
    img2 = load_image_array(image2_path)
    
    img1, img2 = ensure_same_size(img1, img2)
    
    # Calculate SSIM for each channel then average
    ssim = structural_similarity(img1, img2, data_range=255, channel_axis=2)
    
    return float(ssim)


def calculate_mse(image1_path, image2_path):
    """
    Calculate Mean Squared Error (MSE).
    
    Args:
        image1_path: Path to first image (or PIL Image)
        image2_path: Path to second image (or PIL Image)
        
    Returns:
        float: MSE value (lower is better)
    """
    img1 = load_image_array(image1_path).astype(np.float32)
    img2 = load_image_array(image2_path).astype(np.float32)
    
    img1, img2 = ensure_same_size(img1, img2)
    
    mse = np.mean((img1 - img2) ** 2)
    
    return float(mse)


def calculate_metrics(hazy_image, dehazed_image, ground_truth_image=None):
    """
    Calculate all available metrics.
    
    Args:
        hazy_image: Path or PIL Image of hazy input
        dehazed_image: Path or PIL Image of dehazed output
        ground_truth_image: Optional path or PIL Image of ground truth
        
    Returns:
        dict: Dictionary containing all metric comparisons
    """
    metrics = {
        "psnr": {},
        "ssim": {},
        "mse": {},
        "has_ground_truth": ground_truth_image is not None
    }
    
    # Hazy vs Dehazed
    psnr_hazy_dehazed = calculate_psnr(hazy_image, dehazed_image)
    ssim_hazy_dehazed = calculate_ssim(hazy_image, dehazed_image)
    mse_hazy_dehazed = calculate_mse(hazy_image, dehazed_image)
    
    metrics["psnr"]["hazy_vs_dehazed"] = round(psnr_hazy_dehazed, 2)
    metrics["ssim"]["hazy_vs_dehazed"] = round(ssim_hazy_dehazed, 4)
    metrics["mse"]["hazy_vs_dehazed"] = round(mse_hazy_dehazed, 2)
    
    # Dehazed vs Ground Truth (if provided)
    if ground_truth_image is not None:
        psnr_dehazed_gt = calculate_psnr(dehazed_image, ground_truth_image)
        ssim_dehazed_gt = calculate_ssim(dehazed_image, ground_truth_image)
        mse_dehazed_gt = calculate_mse(dehazed_image, ground_truth_image)
        
        metrics["psnr"]["dehazed_vs_ground_truth"] = round(psnr_dehazed_gt, 2)
        metrics["ssim"]["dehazed_vs_ground_truth"] = round(ssim_dehazed_gt, 4)
        metrics["mse"]["dehazed_vs_ground_truth"] = round(mse_dehazed_gt, 2)
        
        # Hazy vs Ground Truth
        psnr_hazy_gt = calculate_psnr(hazy_image, ground_truth_image)
        ssim_hazy_gt = calculate_ssim(hazy_image, ground_truth_image)
        mse_hazy_gt = calculate_mse(hazy_image, ground_truth_image)
        
        metrics["psnr"]["hazy_vs_ground_truth"] = round(psnr_hazy_gt, 2)
        metrics["ssim"]["hazy_vs_ground_truth"] = round(ssim_hazy_gt, 4)
        metrics["mse"]["hazy_vs_ground_truth"] = round(mse_hazy_gt, 2)
    
    return metrics


def format_metrics_report(metrics):
    """
    Format metrics as readable report.
    
    Args:
        metrics: Dictionary from calculate_metrics()
        
    Returns:
        str: Formatted report
    """
    report = "=" * 50 + "\n"
    report += "IMAGE QUALITY METRICS\n"
    report += "=" * 50 + "\n\n"
    
    report += "PSNR (Peak Signal-to-Noise Ratio) in dB\n"
    report += "-" * 40 + "\n"
    for key, value in metrics["psnr"].items():
        report += f"  {key}: {value}\n"
    
    report += "\nSSIM (Structural Similarity Index)\n"
    report += "-" * 40 + "\n"
    for key, value in metrics["ssim"].items():
        report += f"  {key}: {value}\n"
    
    report += "\nMSE (Mean Squared Error)\n"
    report += "-" * 40 + "\n"
    for key, value in metrics["mse"].items():
        report += f"  {key}: {value}\n"
    
    report += "\n" + "=" * 50 + "\n"
    
    return report


if __name__ == "__main__":
    # Test metrics module
    print("Testing metrics module...")
    print("✓ Metrics module loaded successfully")
