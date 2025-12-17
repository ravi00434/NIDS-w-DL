#!/usr/bin/env python3
"""
Test GPU availability and performance for TensorFlow
"""

import tensorflow as tf
import time
import numpy as np

def test_gpu():
    print("🔍 Testing GPU Configuration...")
    print("=" * 50)
    
    # Check TensorFlow version
    print(f"TensorFlow version: {tf.__version__}")
    
    # List physical devices
    print("\n📱 Available devices:")
    for device in tf.config.list_physical_devices():
        print(f"  - {device}")
    
    # Check GPU availability
    gpu_available = tf.config.list_physical_devices('GPU')
    print(f"\n🎮 GPU Available: {len(gpu_available) > 0}")
    
    if gpu_available:
        print(f"GPU Devices: {len(gpu_available)}")
        for i, gpu in enumerate(gpu_available):
            print(f"  GPU {i}: {gpu}")
            
        # Get GPU details
        try:
            gpu_details = tf.config.experimental.get_device_details(gpu_available[0])
            print(f"GPU Details: {gpu_details}")
        except:
            print("Could not get GPU details")
    
    # Test computation on GPU vs CPU
    print("\n⚡ Performance Test:")
    
    # Create test data
    size = 5000
    a = tf.random.normal([size, size])
    b = tf.random.normal([size, size])
    
    # CPU test
    with tf.device('/CPU:0'):
        start_time = time.time()
        c_cpu = tf.matmul(a, b)
        cpu_time = time.time() - start_time
        print(f"CPU computation time: {cpu_time:.4f} seconds")
    
    # GPU test (if available)
    if gpu_available:
        with tf.device('/GPU:0'):
            start_time = time.time()
            c_gpu = tf.matmul(a, b)
            gpu_time = time.time() - start_time
            print(f"GPU computation time: {gpu_time:.4f} seconds")
            
            if gpu_time > 0:
                speedup = cpu_time / gpu_time
                print(f"🚀 GPU Speedup: {speedup:.2f}x faster")
            
            # Verify results are the same
            diff = tf.reduce_max(tf.abs(c_cpu - c_gpu))
            print(f"Max difference between CPU/GPU: {diff:.2e}")
    
    return len(gpu_available) > 0

def test_nids_with_gpu():
    """Test NIDS training with GPU"""
    print("\n🛡️ Testing NIDS with GPU...")
    
    # Simple neural network test
    model = tf.keras.Sequential([
        tf.keras.layers.Dense(128, activation='relu', input_shape=(42,)),
        tf.keras.layers.Dropout(0.3),
        tf.keras.layers.Dense(64, activation='relu'),
        tf.keras.layers.Dropout(0.2),
        tf.keras.layers.Dense(1, activation='sigmoid')
    ])
    
    model.compile(
        optimizer='adam',
        loss='binary_crossentropy',
        metrics=['accuracy']
    )
    
    # Generate sample data
    X_sample = np.random.randn(1000, 42)
    y_sample = np.random.randint(0, 2, 1000)
    
    print("Training small model to test GPU usage...")
    
    # Train with GPU monitoring
    start_time = time.time()
    history = model.fit(
        X_sample, y_sample,
        epochs=5,
        batch_size=32,
        verbose=1
    )
    training_time = time.time() - start_time
    
    print(f"Training completed in {training_time:.2f} seconds")
    
    return model

if __name__ == "__main__":
    gpu_works = test_gpu()
    
    if gpu_works:
        print("\n✅ GPU is working! Your NIDS will use GPU acceleration.")
        test_nids_with_gpu()
    else:
        print("\n❌ GPU not available. NIDS will use CPU only.")
        print("This is still fine - CPU training works well too!")