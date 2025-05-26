#!/bin/bash

# This script sets up the development environment for the Cisco MDS Release Note Agentic System.

# Update package lists
echo "Updating package lists..."
sudo apt-get update

# Install Python and pip if not already installed
echo "Installing Python and pip..."
sudo apt-get install -y python3 python3-pip python3-venv

# Create a virtual environment
echo "Creating a virtual environment..."
python3 -m venv venv

# Activate the virtual environment
echo "Activating the virtual environment..."
source venv/bin/activate

# Install required packages
echo "Installing required packages from requirements.txt..."
pip install -r requirements.txt

# Inform the user that the setup is complete
echo "Setup complete! To activate the virtual environment, run 'source venv/bin/activate'."