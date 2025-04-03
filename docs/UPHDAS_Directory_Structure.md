# UPHDAS Directory Structure, Storage, Retrieval, Compression, and Archival Plan

This document outlines a detailed gameplan for the directory layout and responsibilities for both the **Raspberry Pi units** and the **central server** in the UPHDAS system. It also addresses where all files and configurations should reside and how data should be stored, synced, and archived.

---

## 🌐 GitHub Repository Structure (Already Existing)

```
<repo-root>
├── .github/ISSUE_TEMPLATE/           # GitHub issue templates
├── docs/                             # Project documentation (hardware, server, budget, design)
│   ├── pi/                           # Raspberry Pi specific setup
│   ├── server/                       # Server configuration and setup
│   └── ...                           # Other project docs
├── src/                              # Core scripts
│   ├── common/                       # Shared Python utilities
│   ├── pi/                           # All Pi-side Python + Bash scripts
│   └── server/                       # Server-side utilities & service scripts
├── README.md
└── requirements.txt                 # Global pip dependencies
```

---

## 🧠 Raspberry Pi Unit Directory Layout

### Base Path: `/home/pi/uphdas`

```
/home/pi/uphdas/
├── bin/                         # Executables and service scripts
│   ├── rolling_capture.py       # Main entrypoint script for automated observations
│   ├── setup_pi.sh              # Pi provisioning script
│   ├── sync_to_server.sh        # Rsync push script
│   └── start_capture.sh         # Startup launcher
├── config/
│   ├── config.yaml              # Pi-specific configuration (thresholds, camera ID, FOV, etc)
│   └── site_info.json           # Location metadata (lat, lon, alt, site tag)
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
│   ├── YYYY-MM-DD/              # One folder per date
│   │   ├── shot001.jpg
│   │   ├── shot001_meta.json
│   │   └── ...
├── archive/                     # Optional compressed image logs
│   └── 2025-04-03.tar.gz        # After successful sync
├── crons/
│   └── rsync.cron               # Cron jobs (e.g. weather check, nightly startup)
└── requirements.txt             # Pi-specific Python dependencies
```

> 📝 **Notes**:
- `sync_to_server.sh` reads `config.yaml` for Rsync target info
- No `.wcs`, `.ini`, or streak masks are uploaded—just `*.jpg` and `*_meta.json`
- Logs roll daily or weekly with optional compression

---

## 🖥️ Server Directory Layout

### Base Path: `/var/www/html/uphdas`

```
/var/www/html/uphdas/
├── php/                          # Web interface files
│   ├── index.php                 # Dashboard/landing
│   ├── viewer.php                # Data viewer by site/date
│   ├── api/                      # JSON API endpoints
│   │   ├── get_metadata.php
│   │   ├── get_sites.php
│   │   └── get_latest.php
├── assets/                       # Static CSS/JS/images
│   └── ...
├── includes/                     # PHP includes/configs
│   └── db_connect.php
├── config/
│   └── global_config.yaml        # Shared config for PHP, paths, access levels
├── data/                         # Synchronized images + metadata
│   ├── Cedarville/
│   │   └── 2025-04-03/
│   │       ├── shot001.jpg
│   │       └── shot001_meta.json
│   └── Pickford/
│       └── ...
├── archive/
│   └── Cedarville_2025-04-03.tar.gz  # Archived daily image logs
└── logs/
    └── web.log                   # Web interface access logs
```

> 📝 **Notes**:
- Rsync destination is `/var/www/html/uphdas/data/<site>/YYYY-MM-DD/`
- Each Pi pushes to its own subdirectory under `data/`
- Metadata API uses `*_meta.json` to build site-wide and time-based queries
- Archive jobs (cron or manual) compress old folders and move them to `archive/`
- ✅ When syncing, if a folder for the site name does not exist in `data/`, it should be **created automatically** at that moment. This ensures full scalability for new school units without requiring manual folder setup.

---

## 🗃️ Data Flow Summary

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

## 🧩 Compression & Archival Plan

- **Compression Tool**: `tar -czf`
- **Triggered By**:
  - Manual job or cronjob (e.g., 3AM daily)
  - Folders older than `N` days (e.g. 3)
- **Naming Convention**:
  - `{SiteName}_{YYYY-MM-DD}.tar.gz`
- **Source**: `/var/www/html/uphdas/data/<site>/YYYY-MM-DD/`
- **Destination**: `/var/www/html/uphdas/archive/`

---

Let me know if you'd like bash templates, cronjob entries, or systemd unit files included next.
