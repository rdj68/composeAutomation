#!/bin/bash

# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Display instructions for deactivating the virtual environment
echo "Virtual environment created and activated. To deactivate the virtual environment, run: deactivate"
