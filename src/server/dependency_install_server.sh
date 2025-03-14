#!/bin/bash
# Install dependencies on the central server

echo "Updating package lists..."
sudo apt update

echo "Installing Python3, pip, git, and rsync..."
sudo apt install -y python3 python3-pip git rsync

echo "Installing Python packages..."
pip3 install -r ../../requirements.txt

echo "Server dependencies installed."
