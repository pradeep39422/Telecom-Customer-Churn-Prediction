#!/usr/bin/env bash
# exit on error
set -o errexit

# Install Python 3.10 explicitly
apt-get update
apt-get install -y python3.10 python3.10-dev python3.10-venv python3.10-distutils build-essential libatlas-base-dev

# Set Python 3.10 as default
update-alternatives --install /usr/bin/python python /usr/bin/python3.10 1
update-alternatives --set python /usr/bin/python3.10

# Create virtual environment
python -m venv .venv
source .venv/bin/activate

# Install essential tools
curl -sS https://bootstrap.pypa.io/get-pip.py | python
pip install --upgrade pip setuptools==68.2.2 wheel

# Install dependencies
CFLAGS="-Wno-deprecated-declarations" pip install --no-cache-dir -r requirements.txt

# Verify Python version
echo "Python version: $(python --version)"
