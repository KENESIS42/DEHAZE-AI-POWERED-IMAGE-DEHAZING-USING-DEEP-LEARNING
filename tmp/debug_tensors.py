import os
import sys
import numpy as np
import tensorflow as tf
from PIL import Image

sys.path.append(os.path.join(os.path.dirname(__file__), '../backend'))
from inference import load_models

def main():
    base_model, _ = load_models()
    
    # Load the actual test image
    img_path = r"C:\Users\abhis\Desktop\maximmodel-main\data\val\input\0010.jpg"
    img = Image.open(img_path).convert("RGB")
    arr = np.array(img).astype(np.float32) / 255.0
    x_tensor = tf.convert_to_tensor(arr)
    # resize to 256
    x_tensor = tf.image.resize(x_tensor[None, ...], (256, 256))
    
    y = base_model(x_tensor, training=False)
    
    print("Testing output tensors against input...")
    if isinstance(y, dict):
        for k, v in y.items():
            if len(v.shape) == 4 and v.shape[1] == 256 and v.shape[2] == 256:
                diff = tf.reduce_mean(tf.abs(x_tensor - v)).numpy()
                print(f"Tensor {k}: Mean Abs Diff from Input = {diff:.6f}")
                
                 # Let's save it to see which one looks dehazed
                out = tf.clip_by_value(v[0], 0.0, 1.0).numpy()
                out_img = Image.fromarray((out * 255).astype(np.uint8))
                out_img.save(f"../tmp/out_{k.replace('/', '_')}.png")
                print(f"Saved ../tmp/out_{k.replace('/', '_')}.png")

if __name__ == "__main__":
    main()
