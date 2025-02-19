#!/usr/bin/env python3
## update_tle_catalog.py

"""
Fetches the latest satellite TLE data.

TODO:
- Pull TLEs from space-track.org and Celestrak (for the most part).
- Save updated TLEs in the project directory.
"""
import re
import os
import datetime
from io import BytesIO
from urllib.request import urlopen
from spacetrack import SpaceTrackClient

TLE_DIR = "tles"  # All TLE files will be saved here
# We'll have to create a new email for any api keys or use BT's
USERNAME = "xxx"
PASSWORD = "xxx"

def main():
    # Create output directory if needed
    os.makedirs(TLE_DIR, exist_ok=True)
    timestamp = datetime.datetime.utcnow().strftime("%Y%m%d_%H%M%S")

    try:
        print("Fetching Space Track TLEs...")
        st = SpaceTrackClient(
            identity=USERNAME,
            password=PASSWORD
        )
        
        catalog_path = os.path.join(TLE_DIR, "catalog.tle")
        data = st.tle_latest(iter_lines=True, epoch=">now-30", ordinal=1, format="3le")
        
        with open(catalog_path, "w") as f:
            for line in data:
                # Fix missing leading zeros
                line = re.sub(r"^1\s+", "1 00000", line)
                line = re.sub(r"^2\s+", "2 00000", line)
                f.write(line + "\n")
        
        os.link(catalog_path, os.path.join(TLE_DIR, f"{timestamp}_catalog.txt"))
    except Exception as e:
        print(f"Space Track failed: {e}")

    # Always available public sources
    sources = {
        "starlink": "https://celestrak.org/NORAD/elements/supplemental/sup-gp.php?FILE=starlink&FORMAT=tle",
        "oneweb": "https://celestrak.org/NORAD/elements/supplemental/sup-gp.php?FILE=oneweb&FORMAT=tle"
    }

    for name, url in sources.items():
        try:
            print(f"Fetching {name} TLEs...")
            dest = os.path.join(TLE_DIR, f"{name}.tle")
            with urlopen(url) as response:
                content = response.read().decode("utf-8")
                with open(dest, "w") as f:
                    f.write(content)
            os.link(dest, os.path.join(TLE_DIR, f"{timestamp}_{name}.txt"))
        except Exception as e:
            print(f"Failed to get {name}: {e}")

    # Create combined catalog
    print("Creating combined catalog...")
    combined_path = os.path.join(TLE_DIR, "combined.tle")
    with open(combined_path, "w") as outfile:
        for fname in os.listdir(TLE_DIR):
            if fname.endswith(".tle"):
                with open(os.path.join(TLE_DIR, fname)) as infile:
                    outfile.write(infile.read() + "\n")

if __name__ == '__main__':
    main()