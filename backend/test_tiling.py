"""Test script for tiled inference (High-Resolution Support)."""
import os
import sys
import time
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from inference import load_models, process_single_image

def create_high_res_test_image(path):
    """Create a synthetic high-res image (1024x1024) with text."""
    width, height = 1024, 1024
    img = Image.new('RGB', (width, height), color=(200, 200, 200)) # Grey background
    
    d = ImageDraw.Draw(img)
    
    # Add grid lines to check alignment
    for i in range(0, width, 256):
        d.line([(i, 0), (i, height)], fill=(0, 0, 0), width=2)
    for i in range(0, height, 256):
        d.line([(0, i), (width, i)], fill=(0, 0, 0), width=2)
        
    # Add text "ALLEN" in different locations
    # Make sure text crosses tile boundaries
    try:
        # Try to use a default font
        font = ImageFont.truetype("arial.ttf", 60)
    except IOError:
        font = ImageFont.load_default()

    d.text((100, 100), "ALLEN - Top Left", fill=(255, 0, 0), font=font)
    d.text((400, 400), "ALLEN - Center", fill=(0, 255, 0), font=font)
    d.text((240, 240), "ALLEN - Crossing Boundary", fill=(0, 0, 255), font=font) # 256 is boundary
    
    img.save(path)
    print(f"Created synthetic high-res image at {path} ({width}x{height})")
    return width, height

def test_tiling():
    """Test tiled inference."""
    print("=" * 60)
    print("HIGH-RES TILING TEST")
    print("=" * 60)
    
    # 1. Setup
    results_dir = Path(__file__).parent / "results"
    results_dir.mkdir(exist_ok=True)
    
    input_path = results_dir / "test_high_res_input.jpg"
    output_path = results_dir / "test_high_res_output.jpg"
    
    # 2. Create input
    target_w, target_h = create_high_res_test_image(str(input_path))
    
    # 3. Run Inference
    print("\n[TEST] Running inference...")
    try:
        start = time.time()
        # This should trigger the "High-Res Mode" path
        result_img = process_single_image(str(input_path))
        elapsed = time.time() - start
        
        print(f"✓ Inference complete in {elapsed:.2f}s")
        
        # 4. Verify Output Size
        out_w, out_h = result_img.size
        print(f"  Input Size:  {target_w}x{target_h}")
        print(f"  Output Size: {out_w}x{out_h}")
        
        if out_w == target_w and out_h == target_h:
            print("✓ PASS: Output size matches input size (Tiling worked)")
        else:
            print(f"✗ FAIL: Output size mismatch! Expected {target_w}x{target_h}, got {out_w}x{out_h}")
            if out_w == 256:
                print("  (It seems the image was resized instead of tiled)")
            return False
            
        # Save result
        result_img.save(str(output_path))
        print(f"  Saved result to: {output_path}")
        return True
        
    except Exception as e:
        print(f"✗ FAIL: Inference error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_tiling()
    sys.exit(0 if success else 1)
