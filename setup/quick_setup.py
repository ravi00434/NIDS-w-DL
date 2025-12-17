#!/usr/bin/env python3
"""
⚡ Quick Setup - Get NIDS running in under 2 minutes
Automated setup with minimal user interaction
"""

import os
import sys
import subprocess
import time
from pathlib import Path

def print_step(step, message):
    """Print setup step"""
    print(f"\n[{step}/5] {message}")
    print("-" * 50)

def run_command(cmd, description):
    """Run command with progress indication"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} completed")
            return True
        else:
            print(f"❌ {description} failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ {description} failed: {e}")
        return False

def main():
    """Quick setup main function"""
    print("⚡ NIDS Quick Setup")
    print("=" * 50)
    print("🎯 Getting your NIDS ready in under 2 minutes!")
    
    project_dir = Path(__file__).parent
    os.chdir(project_dir)
    
    # Step 1: Check Python
    print_step(1, "Checking Python Environment")
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ required")
        sys.exit(1)
    print(f"✅ Python {sys.version.split()[0]} detected")
    
    # Step 2: Create virtual environment
    print_step(2, "Setting up Virtual Environment")
    if not Path("nids_env").exists():
        if not run_command(f"{sys.executable} -m venv nids_env", "Creating virtual environment"):
            sys.exit(1)
    else:
        print("✅ Virtual environment already exists")
    
    # Step 3: Install dependencies
    print_step(3, "Installing Dependencies")
    pip_cmd = "nids_env/bin/pip" if os.name != 'nt' else "nids_env\\Scripts\\pip.exe"
    
    # Install in chunks for better progress feedback
    essential_packages = [
        "numpy pandas scikit-learn",
        "tensorflow keras", 
        "flask flask-socketio",
        "matplotlib seaborn joblib"
    ]
    
    for packages in essential_packages:
        if not run_command(f"{pip_cmd} install {packages}", f"Installing {packages}"):
            print("⚠️ Some packages failed to install, but continuing...")
    
    # Step 4: Create directories
    print_step(4, "Setting up Project Structure")
    directories = ["models", "logs", "data", "templates"]
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
    print("✅ Project directories created")
    
    # Step 5: Quick model training
    print_step(5, "Training Models (Quick Version)")
    python_cmd = "nids_env/bin/python" if os.name != 'nt' else "nids_env\\Scripts\\python.exe"
    
    if not Path("models/nids_deep_model.h5").exists():
        print("🧠 Training lightweight models for demo...")
        if not run_command(f"{python_cmd} setup_nids.py", "Training models"):
            print("⚠️ Model training had issues, but you can still run demos")
    else:
        print("✅ Models already exist")
    
    # Success message
    print("\n" + "=" * 50)
    print("🎉 QUICK SETUP COMPLETE!")
    print("=" * 50)
    print("🚀 Your NIDS is ready to use!")
    print("\n📋 Next Steps:")
    print("1. Run: python nids_launcher.py")
    print("2. Choose option 1 for Web Dashboard")
    print("3. Open: http://localhost:5000")
    print("\n💡 Pro Tips:")
    print("• Use the launcher for easy access to all features")
    print("• Web dashboard is the most user-friendly option")
    print("• GPU acceleration is automatically enabled if available")
    print("\n🛡️ Happy threat hunting!")

if __name__ == "__main__":
    main()