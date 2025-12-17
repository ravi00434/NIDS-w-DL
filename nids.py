#!/usr/bin/env python3
"""
🛡️ NIDS Main Launcher - Organized Project Structure
Entry point for the GPU-Accelerated Network Intrusion Detection System
"""

import sys
import os
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Import from organized folders
from core.nids_launcher import NIDSLauncher

def main():
    """Main entry point"""
    print("🛡️ GPU-Accelerated Network Intrusion Detection System")
    print("📁 Organized Project Structure")
    print("=" * 60)
    
    # Initialize and run launcher
    launcher = NIDSLauncher()
    launcher.run()

if __name__ == "__main__":
    main()