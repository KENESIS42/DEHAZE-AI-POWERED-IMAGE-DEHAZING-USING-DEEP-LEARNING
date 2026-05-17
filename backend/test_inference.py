"""Test script for inference module."""
import os
import sys
import time
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from inference import load_models, process_single_image


def test_inference():
    """Test inference pipeline."""
    print("=" * 60)
    print("INFERENCE MODULE TEST")
    print("=" * 60)
    
    # Test 1: Load models
    print("\n[TEST 1] Loading models...")
    try:
        start = time.time()
        base_model, adapter = load_models()
        elapsed = time.time() - start
        print(f"✓ Models loaded in {elapsed:.2f}s")
    except Exception as e:
        print(f"✗ Failed to load models: {e}")
        return False
    
    # Test 2: Test with sample image from validation set
    print("\n[TEST 2] Processing test image...")
    test_image_path = Path(__file__).parent.parent / "data" / "val" / "input" / "0010.jpg"
    
    if not test_image_path.exists():
        print(f"✗ Test image not found: {test_image_path}")
        return False
    
    try:
        start = time.time()
        result_image = process_single_image(str(test_image_path), base_model, adapter)
        elapsed = time.time() - start
        
        print(f"✓ Image processed in {elapsed:.2f}s")
        print(f"  Input size: {test_image_path.stat().st_size / 1024:.1f} KB")
        print(f"  Output size: {result_image.size[0]}x{result_image.size[1]}")
        
        # Save output
        output_path = Path(__file__).parent / "results" / "test_inference_output.jpg"
        output_path.parent.mkdir(exist_ok=True)
        result_image.save(str(output_path))
        print(f"  Saved to: {output_path}")
        
    except Exception as e:
        print(f"✗ Failed to process image: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Test 3: Test caching
    print("\n[TEST 3] Testing model caching (second call)...")
    try:
        start = time.time()
        result_image2 = process_single_image(str(test_image_path))
        elapsed = time.time() - start
        print(f"✓ Second inference in {elapsed:.2f}s (models cached)")
    except Exception as e:
        print(f"✗ Failed on second inference: {e}")
        return False
    
    print("\n" + "=" * 60)
    print("✓ ALL INFERENCE TESTS PASSED")
    print("=" * 60)
    return True


if __name__ == "__main__":
    success = test_inference()
    sys.exit(0 if success else 1)
