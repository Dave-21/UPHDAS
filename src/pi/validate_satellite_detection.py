"""
validate_satellite_detection.py

This propagates the orbits of satellites from the visible TLE file (visible_satellites.tle) using Skyfield
and compares the predicted celestial positions (RA/Dec) with those measured from an image (sampled along a detected streak).
If the maximum angular error for all sample points is within a specified margin, the detection is considered validated.
"""

import datetime
import numpy as np
from skyfield.api import load, EarthSatellite
from skyfield.api import wgs84

# Parse le TLE file which contains entries in 3-line format (satellite name, line1, line2).
# Takse TLE file path as input and returns a list of tuples (name, line1, line2).
def parse_tle_file(tle_file):
    satellites = []
    with open(tle_file, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]
    i = 0
    while i < len(lines) - 2:
        # If the first line does not start with '1' or '2', it's the satellite name
        if not (lines[i].startswith('1') or lines[i].startswith('2')):
            name = lines[i]
            line1 = lines[i+1]
            line2 = lines[i+2]
            satellites.append((name, line1, line2))
            i += 3
        else:
            # Otherwise, assume a two-line TLE without an explicit name
            if i + 1 < len(lines):
                satellites.append(("", lines[i], lines[i+1]))
                i += 2
            else:
                break
    return satellites

# Compare angular seperation in degrees between two points on the celestial sphere
# Takes RA/Dec coordinates in degrees and returns the angular separation in degrees.
def angular_separation(ra1, dec1, ra2, dec2):
    ra1_rad = np.deg2rad(ra1)
    dec1_rad = np.deg2rad(dec1)
    ra2_rad = np.deg2rad(ra2)
    dec2_rad = np.deg2rad(dec2)
    cos_sep = (np.sin(dec1_rad) * np.sin(dec2_rad) +
               np.cos(dec1_rad) * np.cos(dec2_rad) * np.cos(ra1_rad - ra2_rad))
    cos_sep = np.clip(cos_sep, -1, 1)
    sep_rad = np.arccos(cos_sep)
    return np.rad2deg(sep_rad)

# For each TLE in the file, propagate its orbit at the sample times given in metadata,
# compare the predicted RA/Dec with the measured RA/Dec from the image, and return
# a list (of dicts) of validated detections.
def validate_detection(metadata, tle_file, margin_deg):
    ts = load.timescale()
    sample_times = []
    for t_str in metadata.get("sample_times_utc", []):
        sample_times.append(datetime.datetime.fromisoformat(t_str.replace("Z", "+00:00")))
    ts_times = ts.utc([dt.year for dt in sample_times],
                      [dt.month for dt in sample_times],
                      [dt.day for dt in sample_times],
                      [dt.hour for dt in sample_times],
                      [dt.minute for dt in sample_times],
                      [dt.second for dt in sample_times])
    
    measured_radec = metadata.get("radec_points", [])
    if not measured_radec:
        print("No measured RA/Dec points available in metadata.")
        return []
    
    validated = []
    satellites = parse_tle_file(tle_file)
    print(f"Parsed {len(satellites)} TLE entries from {tle_file}.")
    
    for sat in satellites:
        name, line1, line2 = sat
        try:
            satellite = EarthSatellite(line1, line2, name, ts)
        except Exception as e:
            print(f"Error creating satellite object for {name}: {e}")
            continue
        
        errors = []
        for t, (measured_ra, measured_dec) in zip(ts_times, measured_radec):
            try:
                ra, dec, _ = satellite.at(t).apparent().radec()
                predicted_ra = ra.degrees
                predicted_dec = dec.degrees
                err = angular_separation(measured_ra, measured_dec, predicted_ra, predicted_dec)
                errors.append(err)
            except Exception as e:
                print(f"Error propagating satellite {name} at time {t}: {e}")
                errors.append(float('inf'))
        
        if errors:
            max_error = max(errors)
            avg_error = sum(errors) / len(errors)
            if max_error <= margin_deg:
                validated.append({
                    "name": name,
                    "max_error": max_error,
                    "avg_error": avg_error,
                    "errors": errors
                })
    return validated
