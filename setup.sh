#!/usr/bin/env bash

# Exits on command failure
set -e

echo "Detected OS type: $OSTYPE"

if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "Running On Linux"
    python3 -m venv venv
    sleep 5
    source venv/bin/activate
    pip install -r requirements.txt
    cd src/
elif [[ "$OSTYPE" == "darwin"* ]]; then
    echo "Running On macOS"
    python3 -m venv venv
    sleep 5
    source venv/bin/activate
    pip install -r requirements.txt
    cd src/
elif [[ "$OSTYPE" == "msys"* || "$OSTYPE" == "cygwin"* ]]; then
    echo "Running on windows"
    python -m venv venv
    sleep 5
    source venv/Scripts/activate
    pip install -r requirements.txt
    cd src/
else
    echo "Unknown OS: $OSTYPE"
    exit 1
fi



if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    source venv/bin/activate
    cd src/
elif [[ "$OSTYPE" == "darwin"* ]]; then
    source venv/bin/activate
    cd src/
elif [[ "$OSTYPE" == "msys"* || "$OSTYPE" == "cygwin"* ]]; then
    source venv/Scripts/activate
    cd src/
else
    echo "Unknown OS: $OSTYPE"
    exit 1
fi


echo "Setup Complete"


