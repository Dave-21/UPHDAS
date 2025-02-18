#!/bin/bash
# Script to continuously sync captured data from the Pi to the central server using rsync.
# we need to adjust the source and destination paths and server credentials

# Example paths; update these variables as per your environment
LOCAL_DATA_DIR="/home/pi/data/"
SERVER_USER="piuser"
SERVER_IP="192.168.1.100"
SERVER_DATA_DIR="/home/piuser/satellite_data/"

while true; do
    rsync -avz $LOCAL_DATA_DIR ${SERVER_USER}@${SERVER_IP}:${SERVER_DATA_DIR}
    echo "Data synced at $(date)."
    # Sleep for 10 minutes before next sync
    sleep 300
done
