#!/bin/bash

# Create a virtual environment
python3 -m venv myenv

# Activate the virtual environment
source myenv/bin/activate

# Upgrade pip to the latest version
pip install --upgrade pip

# Create a requirements.txt file if it doesn't exist
touch requirements.txt

# Install dependencies from requirements.txt
pip install -r requirements.txt
