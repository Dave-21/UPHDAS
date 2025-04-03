# UPHDAS Directory Structure, Storage, Retrieval, Compression, and Archival Plan

This document outlines the directory layout and responsibilities for both the **Raspberry Pi units** and the **central server** in the UPHDA-System. It also addresses where all files and configurations should reside and how data should be stored, synced, and archived.

---

## GitHub Repo Structure

```
<repo-root>
├── .github/ISSUE_TEMPLATE/           # GitHub issue templates
├── docs/                             # Project documentation (hardware, server, design)
│   ├── pi/                           # Raspberry Pi configuration/setup/docs
│   ├── server/                       # Server configuration/setup/docs
│   └── ...                           # Other project docs
├── src/                              # Core scripts
│   ├── common/                       # Shared Python utilities (probly just Rsync)
│   ├── pi/                           # All Pi-side Python + Bash scripts
│   └── server/                       # Server-side utilities, Bash scripts, and web-interface
├── README.md
└── requirements.txt                 # Global pip dependencies
```

---

## Raspberry Pi Directory Layout

### Base Path: `/home/pi/uphdas`

```
/home/pi/uphdas/
├── bin/                         # Executables and service scripts
│   ├── rolling_capture.py       # Main entrypoint script for automated observations
│   ├── setup_pi.sh              # Pi initialization script
│   ├── sync_to_server.sh        # Rsync push script
│   └── start_capture.sh         # Startup launcher (can be run from cron job)
├── config/
│   ├── config.yaml              # Pi-specific configuration (thresholds, camera ID, FOV, etc)
│   └── site_info.json           # Location metadata (lat, lon, alt, elv, site tag)
├── logs/                        # Rolling logs
│   ├── capture.log
│   └── error.log
├── scripts/                     # All processing utilities
│   ├── plate_solve.py
│   ├── predict_passes.py
│   ├── calibrate_image.py
│   ├── extract_streak.py
│   ├── update_tle_catalog.py
│   ├── validate_satellite_detection.py
│   ├── weather_check.py
│   └── temperature.py
├── tle/
│   ├── starlink.tle
│   ├── oneweb.tle
│   ├── catalog.tle              # Raw TLEs
│   └── combined.tle             # Merged for prediction
├── data/                        # All captured observation data
│   ├── YYYY-MM-DD/              # One folder per date (they get recycled tho)
│   │   ├── shot001.png
│   │   ├── shot001_meta.json    # Currently it's in JSON format
│   │   └── ...
├── crons/
│   └── rsync.cron               # Cron jobs (e.g. weather check, nightly startup)
└── requirements.txt             # Pi-specific Python dependencies (these are pip reqs but we'll but APT installs in setup)
```

---

## Server Directory Layout

### Base Path: `/var/www/html/uphdas`

```
/var/www/html/uphdas/
├── php/                          # Web interface files
│   ├── index.php                 # Dashboard/homepage
│   ├── viewer.php                # Data viewer by site/date
│   ├── api/                      # JSON API endpoints (there are many ways we can do this)
│   │   ├── get_metadata.php
│   │   ├── get_sites.php
│   │   └── get_latest.php
├── assets/                       # Static CSS/JS/images
│   └── ...
├── includes/
│   └── db_connect.php
├── config/
│   └── global_config.yaml
│   └── # We'll probably need another shared config for PHP, paths, access levels
├── data/                         # Synchronized images + metadata
│   ├── Cedarville/
│   │   └── 2025-04-03/
│   │       ├── shot001.png
│   │       └── shot001_meta.json
│   └── Pickford/
│       └── ...
├── archive/                       # We should honestly archive everything say yearly (not in our plan) - Optional
│   └── Cedarville_2025-04-03.tar.gz  # Archived daily image logs
└── logs/
    └── web.log                   # Web interface access logs
    └── # Many other logs too. For e.g. climate.log, issues.log, errors.log, debug.log (if debug mode is on)
```

---

## Data Flow Summary

1. **Observation Phase (Pi):**
    - Pi wakes at 7PM
    - `weather_check.py` validates night conditions
    - If clear, `rolling_capture.py` runs
    - For each frame:
      - Capture, plate solve, extract RA/Dec
      - Match satellite with local TLEs
      - Write JPEG and `*_meta.json`
2. **Sync Phase (Pi → Server):**
    - Cron runs `sync_to_server.sh`
    - Rsyncs to `/var/www/html/uphdas/data/<site>/YYYY-MM-DD/`
    - Ensures target folder exists; creates it if necessary
3. **Web Phase (Server):**
    - PHP reads metadata to populate dashboard
    - Archive or auto-archive old nights

---

## Compression & Archival Plan (not planning on this/Optional)
``(just an example of the process not our compression method)``

- **Compression Tool**: `tar -czf`
- **Triggered By**:
  - Cronjob (e.g., 3am monthly/yearly)
  - Folders older than `N` days (e.g. 3)
- **Naming Convention**:
  - `{SiteName}_{YYYY-MM-DD}.tar.gz`
- **Source**: `/var/www/html/uphdas/data/<site>/YYYY-MM-DD/`
- **Destination**: `/var/www/html/uphdas/archive/`

---
