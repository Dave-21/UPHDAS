# UPHDAS Sequence Diagrams (Mermaid Format)

This document contains all detailed sequence diagrams for the Unified Public Highschool Distributed Astrophotography System (UPHDAS), written in Mermaid format. These cover operations including weather checks, pass predictions, image capture, streak processing, data upload, and TLE updates.

---

## 1. Pi Daily Startup Routine
```mermaid
sequenceDiagram
    autonumber
    participant Pi as Raspberry Pi
    participant Config as config.yaml
    participant NOAA as weather.gov API

    Pi->>Config: Load config.yaml
    Pi->>NOAA: Fetch forecast (cloud, precipitation, moon)
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
    participant Skyfield as Skyfield Library
    participant Observer as Observer Location

    Pi->>TLE: Load latest satellite TLEs
    Pi->>Skyfield: Compute pass visibility (next 3 hrs)
    Skyfield->>Observer: Project paths from observer lat/lon
    Skyfield-->>Pi: Best azimuth/elevation to point
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
    Camera-->>Pi: Raw image (JPEG or PNG)
    Pi->>Storage: Save image
    Pi->>ASTAP: Run plate solve
    ASTAP-->>WCS: Output .wcs file
    Pi->>Pi: Extract RA/Dec using WCS
    Pi->>Pi: Detect streaks (custom algorithm)
    Pi->>Pi: Match points on streak with time, direction, etc.
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

## 5. TLE Update on Server
```mermaid
sequenceDiagram
    autonumber
    participant Server as Homestead Server
    participant SpaceTrack as space-track.org
    participant Celestrak as celestrak.org
    participant Catalog as TLE Catalog

    Server->>SpaceTrack: Fetch active satellite TLEs
    Server->>Celestrak: Fetch Starlink, OneWeb TLEs
    SpaceTrack-->>Server: TLE Data
    Celestrak-->>Server: TLE Data
    Server->>Catalog: Merge and store as combined.tle
```

---

## 6. Image Validation and Matching (Server-Side)
```mermaid
sequenceDiagram
    autonumber
    participant Server as Homestead Server
    participant Catalog as combined.tle
    participant Skyfield as Skyfield Library
    participant Metadata as Image Metadata

    Server->>Metadata: Load image RA/Dec and timestamp
    Server->>Catalog: Load recent TLEs
    Server->>Skyfield: Predict positions at image time
    Skyfield-->>Server: Predicted satellite positions
    Server->>Server: Compare RA/Dec vectors
    alt Match found
        Server->>Server: Mark image as validated
    else No match
        Server->>Server: Store as unvalidated
    end
```

---

## 7. GitHub Dev Pipeline (Manual Backup)
```mermaid
sequenceDiagram
    autonumber
    participant Dev as Developer
    participant GitHub as GitHub Repo
    participant Pi as Raspberry Pi

    Dev->>Pi: Pull changes
    Dev->>GitHub: Commit and push code backup
    GitHub-->>Dev: Store in remote
    note over Pi: Pi pulls updates manually if needed
```

---
