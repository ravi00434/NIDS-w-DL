#!/bin/bash
# 🛡️ NIDS Quick Launcher Script
# One-click startup for your Network Intrusion Detection System

echo "🛡️ Starting GPU-Accelerated NIDS..."
echo "=================================="

# Check if virtual environment exists
if [ ! -d "nids_env" ]; then
    echo "📦 Setting up NIDS for first time..."
    python3 quick_setup.py
fi

# Activate environment and launch
source nids_env/bin/activate
python3 nids_launcher.py