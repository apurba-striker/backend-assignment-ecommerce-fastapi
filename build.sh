#!/bin/bash
set -e

# Upgrade pip and setuptools
pip install --upgrade pip setuptools wheel

# Install packages without Rust dependencies
pip install fastapi==0.104.0 uvicorn==0.23.2 pymongo==4.6.0 pydantic==2.4.2 python-dotenv==1.0.0 motor==3.3.1 gunicorn==21.2.0

# Try to install cryptography with binary wheels
pip install --only-binary=:all: cryptography || echo "Skipping cryptography installation"

# Install any remaining packages
pip install -r requirements.txt || echo "Some packages may not have been installed"

echo "Build completed" 