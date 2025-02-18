# UPHDAS
Upper Peninsula High-latitude Domain Awareness System

## Overview
A Raspberry Pi–based project for **autonomously detecting satellites**, generating partial TLEs, and **backing up** to a central server. The system includes weather-based scheduling, image processing to detect streaks, and plate-solving for precise astrometric calibration.

## Features
- 📷 **Starfield Image Capture**: Using IMX477 with calibrated exposure.
- 🔍 **Plate Solving**: Converts pixel coordinates to celestial coordinates using ASTAP.
- 🛰️ **Satellite Streak Detection**: Identifies satellite arc in long-exposure image.
- 🚀 **Orbital Parameter Estimation**: Computes Right Ascension and Declination for a detected satellite.
- 📡 **TLE Generation & Validation**: Compares with official bulk TLE database.
- 🌤️ **Weather-Based Operation**: Determines if weather conditions are favorable for capturing images.
- 🔄 **Automated Data Syncing**: Uses `rsync` to transfer data to a central aggregate server.

## Project Structure
```
📂 root  
 ├── 📄 README.md (You are here!)  
 ├── 📂 docs (Research, API References)  
 ├── 📂 src (All source code)  
 │   ├── capture_images.py (Captures images using IMX477)  
 │   ├── process_images.py (Processes images for satellite streaks)  
 │   ├── plate_solve_astap.py (Performs plate solving)  
 │   ├── extract_ra_dec.py (Extracts RA/Dec from streaks)  
 │   ├── generate_tle.py (Generates TLE sets)  
 │   ├── check_clouds.py (Determines if imaging conditions are favorable)  
 │   ├── update_tle.py (Fetches latest TLEs)  
 │   ├── predict_passes.py (Predicts satellite passes)  
 │   ├── sync_data.sh (Syncs data to server)  
 │   ├── setup_env.sh (Installs dependencies)  
 ├── 📂 tests (Automated tests)  
 ├── 📂 data (Raw images, processed results)  
 ├── 📂 configs (Configuration files)  
```

## Installation
```bash
git clone https://github.com/your-repo/satellite-tracking.git
cd satellite-tracking
bash setup_env.sh
```

## Usage
### **1️⃣ Capturing Starfield Images**
```bash
python src/capture_images.py --exposure 5 --gain 10
```

### **2️⃣ Running Plate Solving**
```bash
python src/plate_solve_astap.py --image data/starfield.jpg --output data/solve_result.ini
```

### **3️⃣ Detecting Satellite Streaks**
```bash
python src/process_images.py --image data/starfield.jpg --streaks-output data/streaks.json
```

### **4️⃣ Extracting RA/Dec from Streaks**
```bash
python src/extract_ra_dec.py --streaks data/streaks.json --plate-solution data/solve_result.ini
```

### **5️⃣ Generating TLE**
```bash
python src/generate_tle.py --input data/ra_dec_times.json --output data/tle.txt
```

### **6️⃣ Updating Satellite Catalog**
```bash
python src/update_tle.py
```

### **7️⃣ Checking Weather Conditions Before Running**
```bash
python src/check_clouds.py
```

### **8️⃣ Predicting Satellite Passes**
```bash
python src/predict_passes.py --tle data/tle.txt --location configs/observer_location.json
```

### **9️⃣ Syncing Data to Server**
```bash
bash src/sync_data.sh
```

## API Integration
- **[Space-Track.org API](https://www.space-track.org/)**: Fetches real-time TLE data.
- **[ASTAP](https://www.hnsky.org/astap.htm)**: Plate solving automation.
- **[NOAA Weather API](https://forecast.weather.gov/)**: Weather forecasting.

## Table of Contents
1. [Introduction & Goals](#introduction--goals)
2. [Project Overview](#project-overview)
3. [Requirements](#requirements)
4. [Hardware Setup](#hardware-setup)
5. [Software & Environment Setup](#software--environment-setup)
6. [Configuration](#configuration)
7. [Operation](#operation)
8. [Data Flow & Storage](#data-flow--storage)
9. [Roadmap / TODOs](#roadmap--todos)
10. [Contributing](#contributing)
11. [License](#license)

---

## Introduction & Goals

<details>
<summary><strong>Click to Expand</strong></summary>

### Introduction
The **Satellite Detection System** aims to capture night-sky images using a Raspberry Pi camera, **detect satellite streaks**, generate partial orbital elements, and compare them to official satellite catalogs. It then uploads the data to a **central server** for archival and further analysis.

### Goals
1. **Automated Observation**  
   - Run autonomously overnight, using weather forecasts to decide if the sky is sufficiently clear.

2. **Accurate Satellite Detection**  
   - Identify satellite streaks in images while filtering out planes, noise, and other false positives.

3. **TLE Generation & Matching**  
   - Perform plate solving to extract RA/Dec coordinates, then generate partial TLEs (RA/Dec) for cross-referencing known catalogs.

4. **Data Aggregation & Reporting**  
   - Centralize logs, TLE data, and optional images on a server, providing a basis for easy reporting or a web dashboard.

</details>

---

## Project Overview

<details>
<summary><strong>Click to Expand</strong></summary>

### High-Level Architecture
[Raspberry Pi + Camera + Scripts] | | Wi-Fi / LAN | [Central Server: Database + Web Interface]

1. **Raspberry Pi Unit**  
   - Captures images (nightly), processes them, optionally handles partial TLE generation.

2. **Central Server**  
   - Receives data from multiple Raspberry Pi units.
   - Stores results in a database or file system.
   - Optionally hosts a dashboard or API to monitor statuses.

### Workflow Summary
1. **Weather Check**: Query an API (e.g., Open-Meteo) to verify cloud coverage.  
2. **Camera Capture**: If clear, capture images at intervals throughout the night.  
3. **Detection & Plate Solving**:  
   - Use line detection (Hough transform) and Astrometry.net for plate solving.  
   - Generate partial orbital elements from RA/Dec/time data.  
4. **Comparison & Upload**:  
   - Optionally compare with Space-Track or N2YO.  
   - Upload logs, images, metadata, TLE data to the central server.

</details>

---

## Requirements

<details>
<summary><strong>Click to Expand</strong></summary>

### Hardware Requirements
- **Raspberry Pi 4 or 5** (recommended for sufficient processing power).  
- **IMX519-based Camera** (or Raspberry Pi HQ Camera).  
- **Lens**:
  - Wide lens (~5–10 mm) → ~50° FOV, or
  - Narrow lens (~50 mm) → ~10° FOV.
- **Power Supply** capable of supporting the Pi + camera + any heater/dew heater (~5V / 3A+).
- **Outdoor Enclosure** (weatherproof) and secure mounting solution.

### Software Requirements
- **Raspberry Pi OS** (64-bit recommended) or similar Linux distro.
- **Python 3.8+**.
- **Astrometry.net** for plate solving.
- **OpenCV** for image processing.
- **Requests / HTTP library** (e.g., Python `requests`) for uploading data & checking weather.
- **(Optional)**: Additional libraries for advanced detection (ML frameworks, etc.).

### Network & Server
- **Wi-Fi or Ethernet** access for the Pi to upload results.
- **Central Server** with enough storage to hold logs, TLE data, or optional images.

### External Services
- **Weather API** (e.g., Open-Meteo) for cloud coverage checks.
- **Satellite Catalog API** (e.g., N2YO, Space-Track) to compare orbits.

</details>

---

## Hardware Setup

<details>
<summary><strong>Click to Expand</strong></summary>

1. **Mounting & Enclosure**  
   - If **roof access** is restricted, secure the camera on a wall bracket or a pole.  
   - Ensure the lens can be angled skyward without interference.

2. **Power & Cables**  
   - Long outdoor-rated cable or local power outlets.  
   - Wi-Fi range check if no Ethernet connection is available.

3. **Heater / Dew Control** (Optional)  
   - Cold or humid climates may need a small heater strip or a fan to prevent condensation.

4. **Lens Focus & FOV**  
   - Wide lens captures more sky but with less detail.  
   - Narrow lens captures fewer passes but more precise streak data.

</details>

---

## Software & Environment Setup

<details>
<summary><strong>Click to Expand</strong></summary>

1. **Operating System**  
   - Flash Raspberry Pi OS (64-bit) onto a microSD card.  
   - Run initial setup (enable SSH if needed).

2. **Installing Dependencies**
   ```bash
   sudo apt-get update
   sudo apt-get install -y python3 python3-pip astrometry.net libopencv-dev
   pip3 install opencv-python numpy requests
   # add any other libraries as needed

Astrometry.net Index Files

Estimate your camera’s field of view.
Download appropriate 4100-series (Tycho-2) or 5200-series (Tycho-2 + Gaia) index files.
Place them in /usr/share/astrometry or a directory referenced in /etc/astrometry.cfg.
Weather API Setup

Sign up for a free or paid plan (e.g., Open-Meteo, AccuWeather).
Store the API key in .env or a config file.
(Optional) Additional Tools

If you want to do advanced analysis, consider ML frameworks (PyTorch, etc.).
For debugging or data visualization, install matplotlib, jupyter, etc.
</details>
Configuration
<details> <summary><strong>Click to Expand</strong></summary>
Config Files
camera:
  resolution: [1920, 1080]
  exposure_seconds: 2
  lens_focal_length: 6
weather:
  api_key: "YOUR_API_KEY"
  coverage_threshold: 70
server:
  host: "192.168.1.100"
  port: 8080
  upload_endpoint: "/api/upload"
catalogs:
  spacetrack:
    user: "YOUR_USER"
    pass: "YOUR_PASS"
  n2yo:
    api_key: "YOUR_N2YO_KEY"
Environment Variables
WEATHER_API_KEY, SPACE_TRACK_USER, SPACE_TRACK_PASS
Keep secrets out of version control.
Logging
Decide on a logging directory (/var/log/satellite_detection or logs/ under your project).
Configure logging levels (DEBUG, INFO, WARN) in config.yaml.
</details>
Operation
<details> <summary><strong>Click to Expand</strong></summary>
Typical Nightly Workflow
Check Weather
If cloud coverage < threshold, proceed. Otherwise, skip imaging.
Camera Capture
Run a capture script (e.g., every 2–5 seconds or on a timed schedule).
Streak Detection
Use Hough transform or morphological operations to find line segments.
Filter out short/dashed lines (planes, noise).
Plate Solving
Run solve-field (Astrometry.net) to map streak endpoints from pixel coords to RA/Dec.
TLE Generation
From multiple RA/Dec/time points, estimate partial orbit or just store raw data.
Compare with official catalogs if desired.
Upload to Server
Send logs, TLE data, or images (compressed) to a central server.
The server can store or display them as needed.
Scheduling & Automation
Cron or systemd timers on the Pi to run a nightly_runner script.
Error Handling: If camera fails or network drops, logs should indicate the cause.
</details>
Data Flow & Storage
<details> <summary><strong>Click to Expand</strong></summary>
Local Storage

Images: Saved in a structured directory (e.g., ~/images/YYYY-MM-DD/).
Partial TLE / RA-Dec Files: Possibly JSON, CSV, or a small local DB (SQLite).
Server Storage

A relational database (e.g., PostgreSQL) or NoSQL store (e.g., MongoDB).
Tables/collections for:
Observations (metadata about the pass, time, Pi location, etc.).
TLE Data (if you store final or partial TLE sets).
Logs or event records.
Retention & Backup

Decide how long to keep raw images before purging to free space.
TLE data is relatively small; can be kept indefinitely or archived.
Catalog Comparison

If using Space-Track or N2YO, store relevant satellite IDs or cross-match data.
Possibly run a job each morning to finalize which satellite was identified.
</details>
Roadmap / TODOs
<details> <summary><strong>Click to Expand</strong></summary>
High-Priority
 Implement Satellite Streak Detection (via Hough transform or advanced approach).
 Plate-Solving Integration: Ensure correct index files & scale range.
 Server Setup: Decide final location, set up ingest endpoint.
Medium-Priority
 Weather-based Scheduling: Fine-tune coverage thresholds.
 TLE Generation: Implement partial orbit solution or best-fit approach.
 User Dashboard: Basic web interface to track daily pass results.
Low-Priority
 Advanced ML for streak detection (beyond line detection).
 Multi-Camera Coordination for more accurate orbit measurement.
 Alerting/Notifications: E.g., email or Slack notifications when interesting passes occur.
</details>
Contributing
Pull Requests: Please create feature branches for new functionality and open PRs for review.
Code Style: Follow PEP 8 for Python.
Issues: Use GitHub Issues to track bugs or feature requests. Include logs or screenshots if relevant.

