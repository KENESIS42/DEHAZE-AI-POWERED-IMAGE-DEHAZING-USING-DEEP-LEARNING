import os
import sys
import numpy as np
import tensorflow as tf

sys.path.append(os.path.join(os.path.dirname(__file__), '../backend'))
from inference import load_models, backbone_predict, select_best_output, _CACHED_MODELS

def debug_inference():
    print("Loading models...")
    base_model, adapter = load_models()
    
    print("Creating dummy input...")
    x = np.random.rand(1, 256, 256, 3).astype(np.float32)
    x_tensor = tf.convert_to_tensor(x)
    
    print("Running base_model directly...")
    y = base_model(x_tensor, training=False)
    
    print(f"Output type of base_model: {type(y)}")
    if isinstance(y, dict):
        for k, v in y.items():
            print(f"  Key: {k}, Shape: {v.shape}")
    elif isinstance(y, tf.Tensor):
        print(f"  Tensor Shape: {y.shape}")
    else:
        print(f"  Unknown structure: {y}")
        
    print("Running select_best_output...")
    best_pred = select_best_output(y, prefer_hw=(256, 256))
    print(f"  Best Pred Shape: {best_pred.shape}")
    
    print("Running backbone_predict...")
    final_pred = backbone_predict(x_tensor, base_model)
    print(f"  Final Pred Shape: {final_pred.shape}")
    
    print("Diff between input and final pred:")
    diff = tf.reduce_mean(tf.abs(x_tensor - final_pred)).numpy()
    print(f"  Mean Absolute Difference: {diff}")
    
    # Are we just getting the input back?
    if diff == 0.0:
        print("🚨 WARNING: The model is returning the EXACT same image as the input!")

if __name__ == "__main__":
    debug_inference()
