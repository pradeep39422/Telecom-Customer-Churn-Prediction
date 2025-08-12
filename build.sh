#!/usr/bin/env bash
# exit on error
set -o errexit

# Install system dependencies
apt-get update
apt-get install -y build-essential python3.10-dev libatlas-base-dev

# Create and activate virtual environment
python3.10 -m venv .venv
source .venv/bin/activate

# Install Python dependencies
pip install --upgrade pip
CFLAGS="-Wno-deprecated-declarations" pip install --no-cache-dir -r requirements.txt
