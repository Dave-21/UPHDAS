#!/bin/bash
# Install dependencies on the Raspberry Pi

echo "Updating package lists..."
sudo apt update && sudo apt upgrade



echo "Installing Python3, pip, and git..."
sudo apt install -y python3 python3-pip git

#Needs testing
echo "Installing Python packages..."
sudo apt install python3-opencv
sudo apt install python3-yaml
sudo apt install python3-numpy
sudo apt install python3-libcamera
pip install spacetrack --break-system-packages
pip install astropy --break-system-packages
pip install picamera2 --break-system-packages
pip install skyfield --break-system-packages
pip install requests --break-system-packages

#figure out how to install argparse/dateutil (or see if they are standard packages)

echo "Pi dependencies installed."
