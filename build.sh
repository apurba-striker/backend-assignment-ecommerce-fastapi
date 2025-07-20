#!/bin/bash
set -o errexit
set -o pipefail
set -o nounset

echo "Starting build process..."

# Upgrade pip
pip install --upgrade pip

# Install only pure Python packages
pip install --no-deps fastapi==0.104.0 uvicorn==0.23.2 pymongo==4.6.0 pydantic==2.4.2 python-dotenv==1.0.0 motor==3.3.1 gunicorn==21.2.0

# Install any dependencies of the above packages, but only if they don't require compilation
pip install --only-binary=:all: -r requirements.txt || echo "Warning: Some dependencies may not have been installed"

echo "Build completed successfully" 