#!/usr/bin/env bash

# Exits on command failure
set -e

echo "Detected OS type: $OSTYPE"

if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "Running On Linux"
    python3 -m venv venv
    sleep 5
    source venv/bin/activate
    sleep 5
    pip install -r requirements.txt
    cd src/
elif [[ "$OSTYPE" == "darwin"* ]]; then
    echo "Running On macOS"
    python3 -m venv venv
    sleep 5
    source venv/bin/activate
    sleep 5
    pip install -r requirements.txt
    cd src/
elif [[ "$OSTYPE" == "msys"* || "$OSTYPE" == "cygwin"* ]]; then
    echo "Running on windows"
    python -m venv venv
    sleep 5
    source venv/Scripts/activate
    sleep 5
    pip install -r requirements.txt
    cd src/
else
    echo "Unknown OS: $OSTYPE"
    exit 1
fi 


echo "Setup Complete"


