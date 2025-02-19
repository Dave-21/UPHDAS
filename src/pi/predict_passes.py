#!/usr/bin/env python3
## predict_passes.py

"""
Predicts upcoming satellite passes based on TLE data.

TODO:
- Implement pass prediction using Skyfield.
- Rank passes based on visibility conditions (degrees above horizon).
"""

import os
import numpy as np
from datetime import datetime, timedelta, timezone
from skyfield.api import load, wgs84, EarthSatellite
from math import radians, degrees, sin, cos, acos

# Observer location and elevation
OBSERVER_LAT = 46.4977
OBSERVER_LON = -84.3476
OBSERVER_ELEV = 188

# Observation period and sample interval
OBSERVATION_PERIOD_HOURS = 5
SAMPLE_INTERVAL_MINUTES = 1

# For grouping samples into a pass:
PASS_MIN_ELEVATION = 10

# Pass peak
CAMERA_FOV_RADIUS = 5

# Files (using a pre-generated combined TLE file)
TLE_DIR = "tles"
COMBINED_TLE_FILE = os.path.join(TLE_DIR, "combined.tle")
VISIBLE_PASSES_FILE = os.path.join(TLE_DIR, "visible_passes_overhead.txt")

# --------------------------------------------------
# TLE PROCESSING FUNCTIONS
# --------------------------------------------------
def parse_tle_entries(content):
    lines = [line.strip() for line in content.splitlines() if line.strip()]
    entries = []
    i = 0
    while i < len(lines):
        if lines[i].startswith("0") and i+2 < len(lines) and lines[i+1].startswith("1") and lines[i+2].startswith("2"):
            entries.append((lines[i], lines[i+1], lines[i+2]))
            i += 3
        else:
            i += 1
    return entries

def get_satellite_number(entry):
    # NORADD satellite index
    try:
        return entry[1][2:7].strip()
    except Exception:
        return None

# Proprogate
def compute_satellite_positions(satellites, ts, ts_times, observer, time_list, min_alt):
    sat_positions = {}
    for sat_id, name, line1, line2 in satellites:
        try:
            sat = EarthSatellite(line1, line2, name, ts)
            diff = sat - observer
            apparent = diff.at(ts_times)
            alt, az, _ = apparent.altaz()
            valid = alt.degrees >= min_alt
            if np.any(valid):
                pos_list = []
                for idx, is_valid in enumerate(valid):
                    if is_valid:
                        pos_list.append((time_list[idx], az.degrees[idx], alt.degrees[idx]))
                if pos_list:
                    sat_positions[sat_id] = pos_list
        except Exception as e:
            print(f"Error computing position for satellite {name}: {e}")
    return sat_positions

# Detect pass
def compute_passes(positions, sample_interval_minutes):
    passes = []
    if not positions:
        return passes

    current_group = [positions[0]]
    for i in range(1, len(positions)):
        prev_time = positions[i-1][0]
        curr_time = positions[i][0]
        gap = (curr_time - prev_time).total_seconds()
        if gap <= 1.5 * sample_interval_minutes * 60:
            current_group.append(positions[i])
        else:
            if current_group:
                passes.append(current_group)
            current_group = [positions[i]]
    if current_group:
        passes.append(current_group)

    pass_details = []
    for group in passes:
        rise_time, rise_az, rise_el = group[0]
        set_time, set_az, set_el = group[-1]
        # Culmination is the sample with the maximum altitude.
        culm_sample = max(group, key=lambda x: x[2])
        culm_time, culm_az, culm_el = culm_sample
        duration = int((set_time - rise_time).total_seconds())
        pass_details.append((rise_time, rise_az, rise_el,
                             culm_time, culm_az, culm_el,
                             set_time, set_az, set_el,
                             duration))
    return pass_details

# main
def main():
    if not os.path.exists(COMBINED_TLE_FILE):
        print(f"Error: Combined TLE file not found at {COMBINED_TLE_FILE}")
        return

    # Read and parse the combined TLE file.
    with open(COMBINED_TLE_FILE, "r") as f:
        content = f.read()
    entries = parse_tle_entries(content)
    print(f"Total TLE entries found in combined file: {len(entries)}")

    # Deduplicate by NORAD number.
    unique_entries = {}
    for entry in entries:
        satnum = get_satellite_number(entry)
        if satnum and satnum not in unique_entries:
            unique_entries[satnum] = entry
    print(f"Unique satellites after deduplication: {len(unique_entries)}")

    # Build the list of satellites.
    satellites = []
    sat_names = {}
    for satnum, entry in unique_entries.items():
        header = entry[0]
        name = header[2:].strip()
        line1 = entry[1]
        line2 = entry[2]
        satellites.append((satnum, name, line1, line2))
        sat_names[satnum] = name

    # Set up Skyfield timescale, observer, and time sampling.
    ts = load.timescale()
    observer = wgs84.latlon(OBSERVER_LAT, OBSERVER_LON, elevation_m=OBSERVER_ELEV)
    start_dt = datetime.now(timezone.utc)
    num_samples = int(OBSERVATION_PERIOD_HOURS * 60 / SAMPLE_INTERVAL_MINUTES) + 1
    time_list = [start_dt + timedelta(minutes=i * SAMPLE_INTERVAL_MINUTES) for i in range(num_samples)]
    ts_times = ts.utc([dt.year for dt in time_list],
                      [dt.month for dt in time_list],
                      [dt.day for dt in time_list],
                      [dt.hour for dt in time_list],
                      [dt.minute for dt in time_list],
                      [dt.second for dt in time_list])

    # Pass Detection: compute positions using a low threshold (to catch full passes)
    pass_positions = compute_satellite_positions(satellites, ts, ts_times, observer, time_list, PASS_MIN_ELEVATION)
    print(f"\nTotal satellites with passes above {PASS_MIN_ELEVATION}°: {len(pass_positions)}")

    visible_passes = {}
    for sat_id, positions in pass_positions.items():
        passes = compute_passes(positions, SAMPLE_INTERVAL_MINUTES)
        # Filter passes: only keep passes where the culmination altitude is at least (90 - CAMERA_FOV_RADIUS)
        passes = [p for p in passes if p[5] >= (90 - CAMERA_FOV_RADIUS)]
        if passes:
            visible_passes[sat_id] = passes

    total_pass_satellites = len(visible_passes)
    print(f"\nTotal satellites with overhead passes (culmination >= {90 - CAMERA_FOV_RADIUS}°): {total_pass_satellites}")

    # Output visible overhead passes to a file.
    with open(VISIBLE_PASSES_FILE, "w") as f_out:
        for sat_id, passes in visible_passes.items():
            f_out.write(f"Satellite: {sat_names[sat_id]} (NORAD: {sat_id})\n")
            for idx, p in enumerate(passes, start=1):
                rise_time, rise_az, rise_el, culm_time, culm_az, culm_el, set_time, set_az, set_el, duration = p
                f_out.write(f"  Pass {idx}:\n")
                f_out.write(f"    Rise:  {rise_time.strftime('%Y-%m-%d %H:%M:%S')} UTC  Az: {rise_az:5.1f}°, El: {rise_el:4.1f}°\n")
                f_out.write(f"    Culm:  {culm_time.strftime('%Y-%m-%d %H:%M:%S')} UTC  Az: {culm_az:5.1f}°, El: {culm_el:4.1f}°\n")
                f_out.write(f"    Set:   {set_time.strftime('%Y-%m-%d %H:%M:%S')} UTC  Az: {set_az:5.1f}°, El: {set_el:4.1f}°\n")
                f_out.write(f"    Duration: {duration:4d} seconds\n\n")
    print(f"\nVisible overhead passes have been saved to {VISIBLE_PASSES_FILE}")

if __name__ == '__main__':
    main()
