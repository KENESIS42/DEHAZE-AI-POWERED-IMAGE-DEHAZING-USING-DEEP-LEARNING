import os
import sys
import numpy as np
import tensorflow as tf
from PIL import Image

sys.path.append(os.path.join(os.path.dirname(__file__), '../backend'))
from inference import load_models

def main():
    base_model, _ = load_models()
    
    img_path = r"C:\Users\abhis\Desktop\maximmodel-main\0010_output.jpg"
    img = Image.open(img_path).convert("RGB")
    
    # 256x256
    img = img.resize((256, 256))
    
    arr = np.array(img).astype(np.float32) / 255.0
    x_tensor = tf.convert_to_tensor(arr)[None, ...]
    
    y = base_model(x_tensor, training=False)
    
    print("Evaluating outputs in y...")
    if isinstance(y, dict):
        for k, v in y.items():
            if len(v.shape) == 4 and v.shape[1] == 256 and v.shape[2] == 256:
                diff = tf.reduce_mean(tf.abs(x_tensor - v)).numpy()
                std = np.std(v.numpy())
                
                print(f"\n--- Tensor {k} ---")
                print(f"Mean Abs Diff from Input: {diff:.6f}")
                print(f"Standard Deviation: {std:.6f}")
                print(f"Min: {np.min(v.numpy())}, Max: {np.max(v.numpy())}")
                
                # Check PSNR to input
                psnr = tf.image.psnr(x_tensor, v, max_val=1.0).numpy()[0]
                print(f"PSNR (vs Input): {psnr:.2f} dB")

if __name__ == "__main__":
    main()
