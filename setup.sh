#!/bin/bash
set -e

echo "=== Updating package lists ==="
sudo apt update

echo "=== Installing system dependencies for Sense HAT & Python ==="
sudo apt install -y python3-pip python3-numpy python3-sense-hat

echo "=== Installing Python dependencies ==="
pip3 install -r requirements.txt --break-system-packages

echo "=== Setup complete! ==="
