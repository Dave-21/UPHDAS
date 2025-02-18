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
