"""Test script for metrics module."""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from metrics import calculate_psnr, calculate_ssim, calculate_mse, calculate_metrics, format_metrics_report


def test_metrics():
    """Test metrics calculation."""
    print("=" * 60)
    print("METRICS MODULE TEST")
    print("=" * 60)
    
    # Get test images
    data_dir = Path(__file__).parent.parent / "data" / "val"
    input_image = data_dir / "input" / "0010.jpg"
    target_image = data_dir / "target" / "0010.png"
    
    if not input_image.exists():
        print(f"✗ Input image not found: {input_image}")
        return False
    
    if not target_image.exists():
        print(f"✗ Target image not found: {target_image}")
        return False
    
    print(f"\nUsing test images:")
    print(f"  Input (hazy): {input_image.name}")
    print(f"  Target (clean): {target_image.name}")
    
    # Test 1: Calculate PSNR
    print("\n[TEST 1] Calculating PSNR...")
    try:
        psnr_value = calculate_psnr(str(input_image), str(target_image))
        print(f"✓ PSNR: {psnr_value:.2f} dB")
    except Exception as e:
        print(f"✗ Failed to calculate PSNR: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Test 2: Calculate SSIM
    print("\n[TEST 2] Calculating SSIM...")
    try:
        ssim_value = calculate_ssim(str(input_image), str(target_image))
        print(f"✓ SSIM: {ssim_value:.4f}")
    except Exception as e:
        print(f"✗ Failed to calculate SSIM: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Test 3: Calculate MSE
    print("\n[TEST 3] Calculating MSE...")
    try:
        mse_value = calculate_mse(str(input_image), str(target_image))
        print(f"✓ MSE: {mse_value:.2f}")
    except Exception as e:
        print(f"✗ Failed to calculate MSE: {e}")
        return False
    
    # Test 4: Calculate all metrics together
    print("\n[TEST 4] Calculating all metrics together...")
    try:
        metrics = calculate_metrics(str(input_image), str(target_image), str(target_image))
        print("✓ Metrics calculated:")
        print(format_metrics_report(metrics))
    except Exception as e:
        print(f"✗ Failed to calculate metrics: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Test 5: Metrics with identical images
    print("\n[TEST 5] Testing with identical images (should show inf/1.0)...")
    try:
        psnr_identical = calculate_psnr(str(target_image), str(target_image))
        ssim_identical = calculate_ssim(str(target_image), str(target_image))
        print(f"✓ PSNR (identical): {psnr_identical:.2f} dB (should be inf)")
        print(f"✓ SSIM (identical): {ssim_identical:.4f} (should be 1.0000)")
    except Exception as e:
        print(f"✗ Failed test with identical images: {e}")
        return False
    
    print("\n" + "=" * 60)
    print("✓ ALL METRICS TESTS PASSED")
    print("=" * 60)
    return True


if __name__ == "__main__":
    success = test_metrics()
    sys.exit(0 if success else 1)
