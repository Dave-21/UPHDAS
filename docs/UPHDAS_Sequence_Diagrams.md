# UPHDAS Sequence Diagrams

This document contains all detailed sequence diagrams for UPHDAS, written in Mermaid format (a markdown language). These cover operations such as the weather check, pass prediction, image capture, streak processing, data upload, and TLE update.

---

## 1. Pi Daily Startup Routine
```mermaid
sequenceDiagram
    autonumber
    participant Pi as Raspberry Pi
    participant Config as config.yaml
    participant NOAA as weather.gov API
    participant Skyfield as skyfield.api

    Pi->>Config: Load config.yaml
    Pi->>NOAA: Fetch forecast (cloud, snow & rain precipitation)
    Pi->>Skyfield: Calculate moon phase
    NOAA-->>Pi: Forecast data
    Pi->>Pi: Evaluate conditions against thresholds
    alt Conditions are favorable
        Pi->>Pi: Proceed to observation setup
    else Unfavorable
        Pi->>Pi: Skip imaging for tonight
    end
```

---

## 2. Satellite Pass Prediction
```mermaid
sequenceDiagram
    autonumber
    participant Pi as Raspberry Pi
    participant TLE as combined.tle
    participant Skyfield as skyfield.api
    participant Observer as Observer Location

    Pi->>TLE: Load latest satellite TLEs
    Pi->>Skyfield: Compute pass visibility (next 3 hrs)
    Skyfield->>Observer: Project paths from observer lat/lon
```

---

## 3. Image Capture and Streak Detection
```mermaid
sequenceDiagram
    autonumber
    participant Pi as Raspberry Pi
    participant Camera as IMX477
    participant Storage as MicroSD
    participant ASTAP as ASTAP CLI
    participant WCS as .wcs File

    Pi->>Camera: Capture image (10 sec exposure)
    Camera-->>Pi: Raw image (PNG)
    Pi->>Storage: Save image
    Pi->>ASTAP: Run plate solve
    ASTAP-->>WCS: Output .wcs file
    Pi->>Pi: Extract RA/Dec using WCS
    Pi->>Pi: Detect streaks
    Pi->>Pi: Match points on streak with time, direction, etc.
    Pi->>Pi: Identify satellite using TLE match
```

---

## 4. Metadata Generation & Rsync Upload
```mermaid
sequenceDiagram
    autonumber
    participant Pi as Raspberry Pi
    participant Server as Homestead Server
    participant Rsync as Rsync Tool

    Pi->>Pi: Generate JSON metadata file
    Pi->>Rsync: Push image + metadata to Server
    Rsync->>Server: Transfer data
    Server-->>Pi: Acknowledge receipt
```

---

## 5. TLE Update on Pi
```mermaid
sequenceDiagram
    autonumber
    participant Pi as Raspberry Pi
    participant SpaceTrack as space-track.org
    participant Celestrak as celestrak.org
    participant Catalog as TLE Catalog

    Pi->>SpaceTrack: Fetch active satellite TLEs
    Pi->>Celestrak: Fetch Starlink, OneWeb TLEs
    SpaceTrack-->>Pi: TLE Data
    Celestrak-->>Pi: TLE Data
    Pi->>Catalog: Merge and store as combined.tle
```

---

## 6. Image Validation and Matching (on Pi)
```mermaid
sequenceDiagram
    autonumber
    participant Pi as Raspberry Pi
    participant Catalog as combined.tle
    participant Skyfield as Skyfield Library
    participant Metadata as Image Metadata

    Pi->>Metadata: Load image RA/Dec and timestamp
    Pi->>Catalog: Load recent TLEs
    Pi->>Skyfield: Predict positions at image time
    Skyfield-->>Pi: Predicted satellite positions
    Pi->>Pi: Compare RA/Dec vectors
    alt Match found
        Pi->>Pi: Mark image as validated
    else No match
        Pi->>Pi: Store as unvalidated
    end
```

---
