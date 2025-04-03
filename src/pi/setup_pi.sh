#!/bin/bash
# Setup script for the Raspberry Pi unit.
# Prompts the user for location information and updates config.yaml accordingly.

CONFIG_FILE="config.yaml"

echo "Setting up the Raspberry Pi unit."
read -p "Enter latitude: " LAT
read -p "Enter longitude: " LON

# Write configuration to config.yaml
cat > $CONFIG_FILE <<EOL
pi_config:
  latitude: ${LAT}
  longitude: ${LON}
EOL

echo "Configuration updated in ${CONFIG_FILE}."

boot_service_file="/etc/systemd/system/boot-script.service"

# Edit the temporary file
echo "[Unit]" >> "temp.txt"
echo "Description=Run boot script" >> "temp.txt"
echo "After=network.target" >> "temp.txt"
echo >> "temp.txt"
echo "[Service]" >> "temp.txt"
echo "ExecStart=/home/kain/Documents/bootTest/test.sh" >> "temp.txt"
echo "User=root" >> "temp.txt"
echo >> "temp.txt"
echo "[Install]" >> "temp.txt"
echo "WantedBy=multi-user.target" >> "temp.txt"

# Move the temporary file back to the service file
mv "temp.txt"  $boot_service_file

# Reload systemd and enable the service
systemctl daemon-reload
systemctl enable boot-script.service

