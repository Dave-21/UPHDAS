"""
rolling_capture.py

This continuously captures long-exposure images using Picamera2.
For each image, it:
  - Detects a satellite streak using parameters from the config (config.yaml)
  - If a valid streak is found, samples a configurable number of points along it
  - Computes exact UTC timestamps for each sample point on streak
  - Runs ASTAP plate solving (via plate_solve.py) and converts pixel coordinates to RA/Dec
  - Saves capture metadata
If no valid streak is detected, the image is deleted (trashed).
"""

import os
import time
import json
import yaml
import datetime
from datetime import timedelta

from picamera2 import Picamera2

# Scripts that work in conjunction
import extract_streak
import plate_solve

def load_config(config_path="config.yaml"):
    with open(config_path, "r") as f:
        cfg = yaml.safe_load(f)
    return cfg

# Capture single imaege with Picamera2
# Takes Picamera2 instance, filename, and exposure time in microseconds
# Returns the UTC start time of the capture
def capture_image(camera, filename, exposure_time_us):
    capture_start = datetime.datetime.utcnow()
    camera.start()
    camera.capture_file(filename)
    camera.stop()
    return capture_start

# Process the captured image
# - Detect a satellite streak using provided streak detection parameters
# - Sample points along the streak
# - Run ASTAP plate solving to obtain a WCS solution
# - Convert sampled pixel coordinates to RA/Dec
# Parameters:
# - image_filename (str): Path to the captured image
# - capture_start (datetime): Capture start time (UTC)
# - exposure_time_us (int): Exposure duration in microseconds
# - num_sample_points (int): Number of points to sample along the streak
# - streak_config (dict): Parameters for streak detection
# - astap_config (dict): Parameters for ASTAP plate solving
# Returns:
# - metadata (dict): Metadata for the capture, or None if no valid streak is found
def process_capture(image_filename, capture_start, exposure_time_us, num_sample_points,
                    streak_config, astap_config):
    exposure_duration = exposure_time_us / 1e6
    # Call extract_streak with parameters from the configuration
    streak_line = extract_streak.detect_satellite_streak(
        image_filename,
        min_length=streak_config.get("min_length", 50),
        border_tolerance=streak_config.get("border_tolerance", 10),
        canny_threshold1=streak_config.get("canny_threshold1", 50),
        canny_threshold2=streak_config.get("canny_threshold2", 150),
        hough_threshold=streak_config.get("hough_threshold", 50),
        max_line_gap=streak_config.get("max_line_gap", 5)
    )
    if streak_line is None:
        print(f"No valid satellite streak detected in {image_filename}.")
        return None

    print(f"Satellite streak detected: {streak_line}")
    sample_pixels = extract_streak.sample_line(streak_line, num_sample_points)
    sample_times = []
    for i in range(num_sample_points):
        frac = i / (num_sample_points - 1) if num_sample_points > 1 else 0.5
        sample_time = capture_start + timedelta(seconds=frac * exposure_duration)
        sample_times.append(sample_time.isoformat() + "Z")
    
    # Run ASTAP plate solving using the parameters from the config (config.yaml)
    ini_file = plate_solve.run_plate_solve(image_filename, astap_config)
    if ini_file:
        wcs_sol = plate_solve.load_wcs_from_ini(ini_file)
        if wcs_sol:
            radec_points = [plate_solve.pixel_to_radec(x, y, wcs_sol) for (x, y) in sample_pixels]
        else:
            radec_points = None
    else:
        radec_points = None

    metadata = {
        "image_file": image_filename,
        "capture_start_time": capture_start.isoformat() + "Z",
        "exposure_duration_sec": exposure_duration,
        "streak_line": {"x1": streak_line[0], "y1": streak_line[1],
                        "x2": streak_line[2], "y2": streak_line[3]},
        "sample_points_pixels": sample_pixels,
        "sample_times_utc": sample_times,
        "radec_points": radec_points
    }
    return metadata

def main_loop():
    # Load full configuration
    cfg = load_config()
    pi_config = cfg.get("pi_config", {})
    streak_config = cfg.get("streak_detection", {})

    num_sample_points = pi_config.get("num_sample_points", 3)
    exposure_time_us = pi_config.get("exposure_time_us", 5000000)
    
    # Build the ASTAP config from the pi_config parameters
    astap_config = {
        "astap_speed": pi_config.get("astap_speed", "slow"),
        "astap_search_radius": pi_config.get("astap_search_radius", 180),
        "astap_fov": pi_config.get("astap_fov", 0),
        "astap_demosaic": pi_config.get("astap_demosaic", True),
        "astap_color_correction": pi_config.get("astap_color_correction", True)
    }

    os.makedirs("Captured_Pictures", exist_ok=True)
    os.makedirs("Shot_Metadata", exist_ok=True)

    # Initialize camera
    camera = Picamera2()
    camera.resolution = (4056, 3040)
    still_config = camera.create_still_configuration()
    camera.configure(still_config)
    camera.set_controls({
        "ExposureTime": exposure_time_us,
        "AnalogueGain": 0.5,
        "Brightness": 0.0,
        "Contrast": 1.0,
        "AwbEnable": False,
        "AeEnable": False,
        "AfMode": 0,
        "LensPosition": 0.0
    })

    shot_number = 0
    print("Starting rolling capture loop...")
    while True:
        image_filename = os.path.join("Captured_Pictures", f"shot{shot_number}.png")
        print(f"Capturing image: {image_filename}")
        capture_start = capture_image(camera, image_filename, exposure_time_us)
        metadata = process_capture(image_filename, capture_start, exposure_time_us,
                                   num_sample_points, streak_config, astap_config)
        if metadata is None:
            # Trash the image if no valid satellite streak was detected
            print(f"Trashing image {image_filename} due to no valid streak.")
            try:
                os.remove(image_filename)
            except Exception as e:
                print(f"Error deleting {image_filename}: {e}")
        else:
            meta_filename = os.path.join("Shot_Metadata", f"shot{shot_number}.json")
            with open(meta_filename, "w") as f:
                json.dump(metadata, f, indent=2)
            print(f"Metadata saved to {meta_filename}")
        shot_number += 1
        # Pause between captures
        # TODO: add configurable sleep time
        # TODO: add debug mode
        time.sleep(5)

if __name__ == "__main__":
    main_loop()
