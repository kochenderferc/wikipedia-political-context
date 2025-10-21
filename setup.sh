#!/usr/bin/env bash

# Exits on command failure
set -e

# ⚠️ IMPORTANT:
# Run this script with "source setup.sh" (or ". setup.sh")
# so that the virtual environment remains active after it finishes.
if [[ "$0" == "$BASH_SOURCE" ]]; then
    echo "⚠️ Please run this script with 'source setup.sh' or '. setup.sh' so the venv stays active."
    exit 1
fi

echo "Detected OS type: $OSTYPE"

if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "Running on Linux"
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    cd src/

elif [[ "$OSTYPE" == "darwin"* ]]; then
    echo "Running on macOS"
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    cd src/

elif [[ "$OSTYPE" == "msys"* || "$OSTYPE" == "cygwin"* ]]; then
    echo "Running on Windows"
    python -m venv venv
    source venv/Scripts/activate
    pip install -r requirements.txt
    cd src/

else
    echo "Unknown OS: $OSTYPE"
    exit 1
fi

echo "Setup complete. Virtual environment is active."
