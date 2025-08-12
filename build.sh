#!/usr/bin/env bash
# exit on error
set -o errexit

# Install system dependencies
apt-get update
apt-get install -y build-essential python3.10-dev libatlas-base-dev python3.10-distutils

# Ensure Python 3.10 is used
python3.10 -m venv .venv
source .venv/bin/activate

# Install essential build tools first
curl -sS https://bootstrap.pypa.io/get-pip.py | python3.10
pip install --upgrade pip setuptools wheel

# Install Python dependencies with compatibility flags
CFLAGS="-Wno-deprecated-declarations" pip install --no-cache-dir -r requirements.txt
echo "Python version: $(python --version)"
echo "Pip version: $(pip --version)"
echo "Setuptools path: $(python -c 'import setuptools; print(setuptools.__file__)')"
