#!/usr/bin/env python3
"""
🚀 NIDS Quick Start - Organized Structure
Simple entry point for the organized NIDS project
"""

import subprocess
import sys
from pathlib import Path

def main():
    """Quick start main function"""
    print("🛡️ NIDS Quick Start")
    print("=" * 40)
    print("📁 Organized Project Structure")
    print("🚀 Choose your preferred interface:")
    print()
    print("1. 🌐 Web Dashboard (Browser Interface)")
    print("2. 💻 Command Line (Terminal Interface)")
    print("3. ⚙️ Interactive Launcher (Full Menu)")
    print("4. ❌ Exit")
    
    while True:
        try:
            choice = input("\nEnter choice (1-4): ").strip()
            
            if choice == "1":
                print("\n🌐 Starting Web Dashboard...")
                print("📊 Open: http://localhost:5000")
                subprocess.run([sys.executable, "web/nids_dashboard.py"])
                break
                
            elif choice == "2":
                print("\n💻 Starting Command Line Monitor...")
                subprocess.run([sys.executable, "engine/optimized_nids.py"])
                break
                
            elif choice == "3":
                print("\n⚙️ Starting Interactive Launcher...")
                subprocess.run([sys.executable, "core/nids_launcher.py"])
                break
                
            elif choice == "4":
                print("👋 Goodbye!")
                break
                
            else:
                print("❌ Invalid choice. Please enter 1-4.")
                
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break

if __name__ == "__main__":
    main()