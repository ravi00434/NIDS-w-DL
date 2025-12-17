#!/usr/bin/env python3
"""
Create missing scaler and features files for the NIDS system
"""

import numpy as np
import joblib
from sklearn.preprocessing import StandardScaler
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))
from engine.optimized_nids import FastTrafficGenerator

def create_missing_files():
    """Create the missing scaler and features files"""
    
    # Get feature names from the traffic generator template
    generator = FastTrafficGenerator()
    normal_template = generator.feature_templates['normal']
    
    # Extract feature names (excluding metadata fields)
    feature_names = [key for key in normal_template.keys() 
                    if key not in ['src_ip', 'dst_ip', 'timestamp', 'actual_attack']]
    
    print(f"Creating files with {len(feature_names)} features...")
    
    # Create some sample data to fit the scaler
    sample_data = []
    for _ in range(1000):
        flow = generator.generate_flow()
        features = [flow[feature] for feature in feature_names]
        sample_data.append(features)
    
    sample_data = np.array(sample_data)
    
    # Create and fit the scaler
    scaler = StandardScaler()
    scaler.fit(sample_data)
    
    # Save the scaler and features
    joblib.dump(scaler, 'nids_scaler.pkl')
    joblib.dump(feature_names, 'nids_features.pkl')
    
    print("✅ Created nids_scaler.pkl")
    print("✅ Created nids_features.pkl")
    print(f"📊 Features: {feature_names}")
    
    return True

if __name__ == "__main__":
    create_missing_files()