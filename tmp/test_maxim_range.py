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
    img = img.resize((256, 256))
    
    arr = np.array(img).astype(np.float32) / 255.0
    
    # Range [0,1]
    x_01 = tf.convert_to_tensor(arr)[None, ...]
    y_01 = base_model(x_01, training=False)
    
    # Range [-1,1]
    arr_11 = (arr - 0.5) * 2.0
    x_11 = tf.convert_to_tensor(arr_11)[None, ...]
    y_11 = base_model(x_11, training=False)
    
    # Find add_117 and add_255
    def get_tensors(y_dict):
        tensors = [t for t in y_dict.values() if len(t.shape)==4 and t.shape[1]==256]
        return tensors
        
    t_01 = get_tensors(y_01)
    t_11 = get_tensors(y_11)
    
    print("--- Range [0,1] ---")
    for i, t in enumerate(t_01):
        diff = tf.reduce_mean(tf.abs(x_01 - t)).numpy()
        print(f"Tensor {i} MAD: {diff:.4f}, Mean: {np.mean(t.numpy()):.4f}")
        
    print("\n--- Range [-1,1] ---")
    for i, t in enumerate(t_11):
        # outputs are probably in [-1,1], so scale back to [0,1] to compare
        t_scaled = (t + 1.0) / 2.0
        diff = tf.reduce_mean(tf.abs(x_01 - t_scaled)).numpy()
        print(f"Tensor {i} MAD: {diff:.4f}, Mean: {np.mean(t_scaled.numpy()):.4f}")

if __name__ == "__main__":
    main()
