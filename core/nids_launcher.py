#!/usr/bin/env python3
"""
🛡️ NIDS Launcher - One-Click Network Intrusion Detection System
Optimized for ease of use and performance
"""

import os
import sys
import subprocess
import time
import threading
from pathlib import Path

class NIDSLauncher:
    """Easy-to-use NIDS launcher with automatic setup"""
    
    def __init__(self):
        self.project_dir = Path(__file__).parent
        self.venv_dir = self.project_dir / "nids_env"
        self.models_dir = self.project_dir / "models"
        
    def print_banner(self):
        """Print welcome banner"""
        print("\n" + "="*60)
        print("🛡️  GPU-ACCELERATED NETWORK INTRUSION DETECTION SYSTEM")
        print("="*60)
        print("🚀 Optimized for Performance & Ease of Use")
        print("🎯 Real-time Threat Detection with Deep Learning")
        print("💻 GPU-Accelerated Processing")
        print("="*60 + "\n")
    
    def check_requirements(self):
        """Check if system requirements are met"""
        print("🔍 Checking system requirements...")
        
        # Check Python version
        if sys.version_info < (3, 8):
            print("❌ Python 3.8+ required. Current:", sys.version)
            return False
            
        # Check if virtual environment exists
        if not self.venv_dir.exists():
            print("📦 Virtual environment not found. Creating...")
            self.setup_environment()
            
        # Check if models exist
        if not (self.models_dir / "nids_deep_model.h5").exists():
            print("🧠 Models not found. Training...")
            self.train_models()
            
        print("✅ All requirements satisfied!")
        return True
    
    def setup_environment(self):
        """Setup virtual environment and install dependencies"""
        print("📦 Setting up virtual environment...")
        
        try:
            # Create virtual environment
            subprocess.run([sys.executable, "-m", "venv", str(self.venv_dir)], check=True)
            
            # Install requirements
            pip_path = self.venv_dir / "bin" / "pip" if os.name != 'nt' else self.venv_dir / "Scripts" / "pip.exe"
            subprocess.run([str(pip_path), "install", "-r", "requirements.txt"], check=True)
            
            print("✅ Environment setup complete!")
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Environment setup failed: {e}")
            sys.exit(1)
    
    def train_models(self):
        """Train models if they don't exist"""
        print("🧠 Training NIDS models (this may take a few minutes)...")
        
        try:
            python_path = self.venv_dir / "bin" / "python" if os.name != 'nt' else self.venv_dir / "Scripts" / "python.exe"
            subprocess.run([str(python_path), "setup/setup_nids.py"], check=True)
            print("✅ Model training complete!")
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Model training failed: {e}")
            sys.exit(1)
    
    def show_menu(self):
        """Show main menu"""
        print("\n🎯 Choose your NIDS mode:")
        print("1. 🌐 Web Dashboard (Recommended)")
        print("2. 💻 Command Line Monitor")
        print("3. 🚨 High Attack Demo")
        print("4. 🔧 GPU Performance Test")
        print("5. 📊 System Status")
        print("6. ❌ Exit")
        
        while True:
            try:
                choice = input("\nEnter your choice (1-6): ").strip()
                if choice in ['1', '2', '3', '4', '5', '6']:
                    return int(choice)
                else:
                    print("❌ Invalid choice. Please enter 1-6.")
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                sys.exit(0)
    
    def launch_web_dashboard(self):
        """Launch web dashboard"""
        print("\n🌐 Starting Web Dashboard...")
        print("📊 Dashboard will be available at: http://localhost:5000")
        print("🔄 Starting server...")
        
        python_path = self.venv_dir / "bin" / "python" if os.name != 'nt' else self.venv_dir / "Scripts" / "python.exe"
        
        try:
            subprocess.run([str(python_path), "web/nids_dashboard.py"])
        except KeyboardInterrupt:
            print("\n🛑 Dashboard stopped.")
    
    def launch_cli_monitor(self):
        """Launch optimized command line monitor"""
        print("\n💻 Starting Optimized CLI Monitor...")
        print("🛡️ High-performance network monitoring active")
        print("⏹️  Press Ctrl+C to stop")
        
        python_path = self.venv_dir / "bin" / "python" if os.name != 'nt' else self.venv_dir / "Scripts" / "python.exe"
        
        try:
            subprocess.run([str(python_path), "engine/optimized_nids.py"])
        except KeyboardInterrupt:
            print("\n🛑 Monitoring stopped.")
    
    def launch_attack_demo(self):
        """Launch high attack demo using optimized engine"""
        print("\n🚨 Starting High Attack Demo...")
        print("⚠️  Simulating 50% attack traffic")
        print("🔍 Watch for security alerts")
        print("🚀 Using optimized processing engine")
        
        python_path = self.venv_dir / "bin" / "python" if os.name != 'nt' else self.venv_dir / "Scripts" / "python.exe"
        
        # Create temporary high-attack demo
        demo_code = '''
import sys
sys.path.append('.')
from optimized_nids import OptimizedNIDS, FastTrafficGenerator
import time

nids = OptimizedNIDS(batch_size=16)
if nids.load_models():
    nids.start_processing()
    generator = FastTrafficGenerator(attack_probability=0.5)
    
    print("🚨 High attack simulation running...")
    try:
        for i in range(100):
            flow = generator.generate_flow()
            nids.process_flow(flow)
            
            result = nids.get_result()
            if result and result[0]['is_attack']:
                print(f"🚨 ATTACK #{i}: {result[0]['confidence']:.1%} confidence")
            
            if i % 20 == 0:
                stats = nids.get_performance_stats()
                print(f"📊 Processed: {stats['flows_processed']}, Attacks: {stats['attacks_detected']}")
            
            time.sleep(0.1)
    except KeyboardInterrupt:
        pass
    finally:
        nids.stop_processing()
        print("✅ Demo completed!")
'''
        
        try:
            # Write and execute temporary demo
            with open('temp_demo.py', 'w') as f:
                f.write(demo_code)
            subprocess.run([str(python_path), "temp_demo.py"])
            os.remove('temp_demo.py')  # Clean up
        except KeyboardInterrupt:
            print("\n🛑 Demo stopped.")
        except Exception as e:
            print(f"❌ Demo failed: {e}")
    
    def test_gpu_performance(self):
        """Test GPU performance"""
        print("\n🔧 Testing GPU Performance...")
        
        python_path = self.venv_dir / "bin" / "python" if os.name != 'nt' else self.venv_dir / "Scripts" / "python.exe"
        
        try:
            subprocess.run([str(python_path), "utils/test_gpu.py"])
        except KeyboardInterrupt:
            print("\n🛑 Test stopped.")
    
    def show_system_status(self):
        """Show system status"""
        print("\n📊 System Status:")
        print("="*40)
        
        # Check GPU
        try:
            result = subprocess.run(["nvidia-smi", "--query-gpu=name,memory.total,memory.used", 
                                   "--format=csv,noheader,nounits"], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                gpu_info = result.stdout.strip().split(', ')
                print(f"🎮 GPU: {gpu_info[0]}")
                print(f"💾 GPU Memory: {gpu_info[2]}MB / {gpu_info[1]}MB")
            else:
                print("🎮 GPU: Not available")
        except FileNotFoundError:
            print("🎮 GPU: NVIDIA drivers not found")
        
        # Check models
        if (self.models_dir / "nids_deep_model.h5").exists():
            model_size = (self.models_dir / "nids_deep_model.h5").stat().st_size / (1024*1024)
            print(f"🧠 Deep Learning Model: ✅ ({model_size:.1f}MB)")
        else:
            print("🧠 Deep Learning Model: ❌ Not found")
            
        if (self.models_dir / "nids_rf_model.pkl").exists():
            rf_size = (self.models_dir / "nids_rf_model.pkl").stat().st_size / (1024*1024)
            print(f"🌲 Random Forest Model: ✅ ({rf_size:.1f}MB)")
        else:
            print("🌲 Random Forest Model: ❌ Not found")
        
        # Check environment
        if self.venv_dir.exists():
            print("📦 Virtual Environment: ✅ Ready")
        else:
            print("📦 Virtual Environment: ❌ Not found")
        
        print("="*40)
        input("\nPress Enter to continue...")
    
    def run(self):
        """Main launcher loop"""
        self.print_banner()
        
        if not self.check_requirements():
            print("❌ Setup failed. Please check the errors above.")
            sys.exit(1)
        
        while True:
            choice = self.show_menu()
            
            if choice == 1:
                self.launch_web_dashboard()
            elif choice == 2:
                self.launch_cli_monitor()
            elif choice == 3:
                self.launch_attack_demo()
            elif choice == 4:
                self.test_gpu_performance()
            elif choice == 5:
                self.show_system_status()
            elif choice == 6:
                print("\n👋 Thank you for using NIDS!")
                break

if __name__ == "__main__":
    launcher = NIDSLauncher()
    launcher.run()