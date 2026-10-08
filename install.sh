#!/bin/bash

set -e

echo "======================================"
echo "Fuzzing Framework - J2"
echo "Environment installation"
echo "======================================"

echo ""
echo "[1/2] Updating package information"
sudo apt update

echo ""
echo "[2/2] Installing system dependencies..."
sudo apt install -y
git
python3
python3-pip
python3-venv
build-essential
curl
wget

echo ""
echo "Base dependencies installed successfully"
