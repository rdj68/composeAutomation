#!/bin/bash

# Install pipenv
pip install pipenv

# Create a virtual environment
pipenv install

# Activate the virtual environment
pipenv shell

# Display instructions for deactivating the virtual environment
echo "Virtual environment created and activated. To deactivate the virtual environment, run: deactivate"
