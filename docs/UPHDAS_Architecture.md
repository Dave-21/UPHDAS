# UPHDAS Satellite Tracking System Architecture

## 1.  Hardware Architecture

### Capture Unit (per site)
- **Camera**: IMX477 (12.3 MP)
- **Lens**: Varifocal C/CS mount (8-50mm)
- **Computer**: Raspberry Pi 5
- **Storage**: Micro SD card
- **Power**: Outdoor AC extension cord & AC adapter
- **Mounting**: Antenna mount on roof or gable end
- **Housing**: Weatherproof case with ventilation and heated glass viewing window

## 2.  Server Infrastructure

### Server Details
- **Provider**: Homestead Space Operations
- **Type**: Basic HP workstation server
- **Hosting**: Hosted at Homestead
- **Networking**: Has a dedicated public IP provided by Homestead

### Roles
- Stores both validated and unvalidated satellite image data
- Hosts metadata per image:
  - Timestamp of image
  - Camera location (latitude, longitude, altitude, and site tag)
  - Camera identifier
  - Field of view (in degrees)
  - Pointing angle (azimuth)
  - Gain settings and intensity range
- Provides data to Raspberry Pi units via Rsync
- Not directly accessible from Pi (only server has port forwarding)

## 3.  Operational Schedule
- **Pi Boot Time**: Daily at 7:00 PM
- **Exposure Time**: 10 seconds per image

## 4.  Weather & Cloud Screening

### Script: `weather_check.py`
- Uses **weather.gov (NOAA)**
- Pulls forecast data for:
  - Cloud coverage
  - Rain/snow precipitation
- Calculates Moon phase with Skyfield
- Thresholds are defined in `config.yaml`
- Only captures if conditions are within acceptable thresholds

## 5.  Plate Solving and Calibration
- Uses **ASTAP CLI** for plate solving
- Extracts WCS data from `.wcs` file
- Converts pixel coordinates to RA/Dec for satellite streak segments

## 6.  Satellite Detection & Metadata Extraction
- Detects satellite streaks in long-exposure images
- Annotates debug image with RA/Dec and direction
- No streak masks or `.wcs` files uploaded to server
- Only image + metadata file per image is synced to server

## 7.  Satellite Catalog & Tracking

### TLE Management (`update_tle.py`)
- Retrieves daily TLEs from:
  - space-track.org
  - Celestrak (Starlink, OneWeb)
- Consolidates to `tles/combined.tle`

### Pass Prediction (`predict_passes.py`)
- Uses Skyfield to predict visibility
- Filters based on altitude and ground station

## 8.  Observation Planning

- Pass prediction window: ~8 hours ahead
- Sampling interval: 30 seconds
- Satellite detection preference: max number visible in 45&deg; FOV

## 9.  Data Sync & Management
- **File Upload**:
  - Only image and its JSON metadata
- **Protocol**: Rsync
- **Direction**: Pi &rarr; Server only
- **GitHub**:
  - Used **only** for code backups documentation

## 10.  Directory Structure Example
```
/var/www/html/uphdas/
├── data/                         # Synchronized images + metadata
│   ├── Cedarville/
│   │   └── 2025-04-03/
│   │       ├── shot001.png
│   │       └── shot001_meta.json
│   └── Pickford/
│       └── ...
```

## 11.  Performance Metrics (TBD)
- Accuracy of satellite matching
- % of passes detected vs predicted
- Exposure success rate
- Visual magnitude limits for camera
