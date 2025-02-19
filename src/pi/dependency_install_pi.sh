#!/bin/bash
# Install dependencies on the Raspberry Pi

echo "Updating package lists..."
sudo apt update

echo "Installing Python3, pip, and git..."
sudo apt install -y python3 python3-pip git

echo "Installing Python packages..."
#using pip3 for installation doesn't work on linux, try install python3-[package]
pip3 install -r ../../requirements.txt

echo "Pi dependencies installed."
