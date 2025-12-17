#!/bin/bash
# NIDS Startup Script with GPU Support

# Set CUDA library path
export LD_LIBRARY_PATH=/usr/lib/cuda/lib64:$LD_LIBRARY_PATH

# Activate virtual environment
source core/nids_env_py310/bin/activate

# Run the NIDS application
python start.py
