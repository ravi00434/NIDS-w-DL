#!/usr/bin/env python3
"""
Setup script for the Deep Learning NIDS
Trains models and prepares the system for deployment
"""

import os
import sys
import subprocess
from deep_learning_nids import DeepLearningNIDS

def install_requirements():
    """Install required packages"""
    print("📦 Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Requirements installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install requirements: {e}")
        return False

def setup_directories():
    """Create necessary directories"""
    directories = ['models', 'logs', 'data', 'templates']
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"📁 Created directory: {directory}")

def train_models():
    """Train and save the NIDS models"""
    print("\n🧠 Training NIDS Models...")
    print("=" * 50)
    
    # Check if dataset exists
    dataset_path = '/home/ravi/DATASETS/UNSW_NB15/UNSW_NB15_training-set.csv'
    
    if not os.path.exists(dataset_path):
        print(f"❌ Dataset not found at: {dataset_path}")
        print("Please ensure the UNSW-NB15 dataset is available")
        
        # Create a sample dataset for demo purposes
        print("🔄 Creating sample dataset for demonstration...")
        create_sample_dataset()
        return True
    
    try:
        # Initialize and train NIDS
        nids = DeepLearningNIDS(dataset_path)
        
        # Load and preprocess data
        X_train, X_test, y_train, y_test = nids.load_and_preprocess_data()
        
        if X_train is None:
            print("❌ Failed to load training data")
            return False
        
        # Train models
        print("🚀 Starting model training (this may take several minutes)...")
        history = nids.train_models(X_train, X_test, y_train, y_test)
        
        # Evaluate models
        dl_pred, rf_pred, dl_acc, rf_acc = nids.evaluate_models(X_test, y_test)
        
        # Save models
        nids.save_models('models/nids_deep_model.h5', 'models/nids_rf_model.pkl')
        
        print(f"\n🎯 Training Results:")
        print(f"Deep Learning Accuracy: {dl_acc:.4f}")
        print(f"Random Forest Accuracy: {rf_acc:.4f}")
        print("✅ Models trained and saved successfully!")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during training: {e}")
        return False

def create_sample_dataset():
    """Create a sample dataset for demonstration"""
    import pandas as pd
    import numpy as np
    
    print("📊 Generating sample network traffic data...")
    
    # Generate synthetic network flow data
    np.random.seed(42)
    n_samples = 10000
    
    # Feature names matching UNSW-NB15 dataset
    features = [
        'dur', 'sbytes', 'dbytes', 'sttl', 'sload', 'dload', 'spkts', 'dpkts',
        'swin', 'dwin', 'stcpb', 'dtcpb', 'smeansz', 'dmeansz', 'trans_depth',
        'response_body_len', 'ct_srv_src', 'ct_state_ttl', 'ct_dst_ltm',
        'ct_src_dport_ltm', 'ct_dst_sport_ltm', 'ct_dst_src_ltm', 'is_sm_ips_ports',
        'ct_flw_http_mthd', 'is_ftp_login', 'ct_ftp_cmd', 'ct_srv_dst',
        'ct_service_dst', 'ct_log_srv_dst', 'ct_src_ltm', 'ct_tcp_tsl_time',
        'proto', 'service', 'state', 'label'
    ]
    
    # Generate synthetic data
    data = {}
    
    # Normal traffic (70%)
    normal_samples = int(n_samples * 0.7)
    attack_samples = n_samples - normal_samples
    
    for feature in features[:-1]:  # All except label
        if feature in ['proto', 'service', 'state']:
            # Categorical features
            data[feature] = np.random.randint(0, 5, n_samples)
        elif feature.startswith('is_'):
            # Binary features
            data[feature] = np.random.randint(0, 2, n_samples)
        elif 'bytes' in feature or 'pkts' in feature:
            # Packet/byte counts
            normal_vals = np.random.exponential(1000, normal_samples)
            attack_vals = np.random.exponential(5000, attack_samples)  # Higher for attacks
            data[feature] = np.concatenate([normal_vals, attack_vals])
        else:
            # Other numerical features
            data[feature] = np.random.exponential(1, n_samples)
    
    # Labels: 0 = normal, 1 = attack
    data['label'] = np.concatenate([
        np.zeros(normal_samples, dtype=int),
        np.ones(attack_samples, dtype=int)
    ])
    
    # Create DataFrame and shuffle
    df = pd.DataFrame(data)
    df = df.sample(frac=1).reset_index(drop=True)
    
    # Save sample dataset
    os.makedirs('data', exist_ok=True)
    sample_path = 'data/sample_network_data.csv'
    df.to_csv(sample_path, index=False)
    
    print(f"✅ Sample dataset created: {sample_path}")
    print(f"📈 Dataset shape: {df.shape}")
    print(f"🎯 Attack ratio: {df['label'].mean():.2%}")
    
    return sample_path

def create_demo_script():
    """Create a demo script"""
    demo_script = '''#!/usr/bin/env python3
"""
Demo script for the Deep Learning NIDS
Run this to see the system in action
"""

import time
import threading
from deep_learning_nids import DeepLearningNIDS
from realtime_nids import RealTimeNIDS

def run_basic_demo():
    """Run a basic NIDS demo"""
    print("🛡️  Deep Learning NIDS Demo")
    print("=" * 40)
    
    # Initialize NIDS
    nids = DeepLearningNIDS()
    
    # Try to load pre-trained models
    try:
        nids.load_models('models/nids_deep_model.h5', 'models/nids_rf_model.pkl')
        print("✅ Pre-trained models loaded")
    except:
        print("⚠️  No pre-trained models found. Run setup_nids.py first.")
        return
    
    # Demo prediction
    print("\\n🔍 Testing sample predictions...")
    
    # Generate some test samples
    import numpy as np
    
    # Normal traffic sample
    normal_sample = np.random.randn(34) * 0.5  # Low variance
    result = nids.predict_single_sample(normal_sample)
    print(f"Normal traffic prediction: {result}")
    
    # Suspicious traffic sample
    attack_sample = np.random.randn(34) * 2 + 3  # High variance and offset
    result = nids.predict_single_sample(attack_sample)
    print(f"Suspicious traffic prediction: {result}")

def run_realtime_demo():
    """Run real-time monitoring demo"""
    print("\\n🚀 Starting Real-time Monitoring Demo...")
    
    nids = RealTimeNIDS()
    
    try:
        # Start monitoring
        flow_generator = nids.start_monitoring(use_simulator=True, attack_probability=0.2)
        
        # Run for 20 seconds
        for i in range(4):
            time.sleep(5)
            nids.print_dashboard()
        
        # Stop monitoring
        nids.stop_monitoring()
        flow_generator.stop()
        
        print("\\n✅ Real-time demo completed!")
        
    except Exception as e:
        print(f"❌ Demo error: {e}")

if __name__ == "__main__":
    print("Choose demo mode:")
    print("1. Basic NIDS Demo")
    print("2. Real-time Monitoring Demo")
    print("3. Web Dashboard (run nids_dashboard.py)")
    
    choice = input("Enter choice (1-3): ").strip()
    
    if choice == "1":
        run_basic_demo()
    elif choice == "2":
        run_realtime_demo()
    elif choice == "3":
        print("Run: python nids_dashboard.py")
        print("Then open: http://localhost:5000")
    else:
        print("Invalid choice")
'''
    
    with open('demo_nids.py', 'w') as f:
        f.write(demo_script)
    
    print("✅ Demo script created: demo_nids.py")

def main():
    """Main setup function"""
    print("🛡️  Deep Learning NIDS Setup")
    print("=" * 50)
    
    # Setup directories
    setup_directories()
    
    # Install requirements
    if not install_requirements():
        print("❌ Setup failed due to package installation issues")
        return
    
    # Train models
    if not train_models():
        print("❌ Setup failed due to training issues")
        return
    
    # Create demo script
    create_demo_script()
    
    print("\n🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Run 'python demo_nids.py' for a quick demo")
    print("2. Run 'python nids_dashboard.py' for web interface")
    print("3. Run 'python realtime_nids.py' for command-line monitoring")
    print("\n🌐 Web dashboard will be available at: http://localhost:5000")

if __name__ == "__main__":
    main()