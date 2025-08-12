#!/usr/bin/env bash
# exit on error
set -o errexit

# Install system dependencies
apt-get update
apt-get install -y build-essential python3-dev libatlas-base-dev

# Ensure we use the correct Python version
python3.10 -m pip install --upgrade pip

# Install Python dependencies with compatibility flags
CFLAGS="-Wno-deprecated-declarations" pip install --no-cache-dir -r requirements.txt
