#!/bin/bash
# Process manager script to start and monitor server-side processes.
# This may include updating TLE catalogs, predicting passes, and other services
# This is a bad example because we won't be doing this server-side, we'll be doing it per unit (unless Dr. Cesul wants it done server-side).

echo "Starting TLE update process..."
python3 update_tle.py &
TLE_UPDATE_PID=$!

echo "Starting satellite pass prediction service..."
python3 predict_passes.py &
PREDICT_PASSES_PID=$!

# Add more processes (pleasse)

echo "Server processes started."
echo "TLE update PID: $TLE_UPDATE_PID"
echo "Predict passes PID: $PREDICT_PASSES_PID"

wait
