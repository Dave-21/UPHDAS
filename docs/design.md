# Satellite Tracking & Imaging System - Design Document

This document details the design, architecture, and data flow of the distributed satellite tracking and imaging system. It covers hardware components, software modules, processing pipelines, synchronization methods, and deployment strategies. Diagrams throughout this document illustrate key system components and data flows.

---

## Table of Contents

1. [Overview](#overview)
2. [System Architecture](#system-architecture)
    - [High-Level Components](#high-level-components)
    - [System Diagram](#system-diagram)
3. [Hardware Components](#hardware-components)
    - [Raspberry Pi Unit](#raspberry-pi-unit)
    - [Central Server](#central-server)
4. [Software Architecture](#software-architecture)
    - [Client-Side (Pi Units)](#client-side-pi-units)
    - [Server-Side](#server-side)
    - [Common Utilities](#common-utilities)
5. [Data Processing Pipeline](#data-processing-pipeline)
    - [Image Acquisition and Preprocessing](#image-acquisition-and-preprocessing)
    - [Plate Solving & Coordinate Extraction](#plate-solving--coordinate-extraction)
    - [Satellite Trajectory Analysis](#satellite-trajectory-analysis)
    - [Weather Data Integration](#weather-data-integration)
6. [Communication & Synchronization](#communication--synchronization)
7. [Deployment & Maintenance](#deployment--maintenance)
8. [Error Handling, Logging, and Security](#error-handling-logging-and-security)
9. [Future Enhancements](#future-enhancements)
10. [Conclusion](#conclusion)

---

## 1. Overview

The Satellite Tracking & Imaging System is a distributed architecture that uses Raspberry Pi units to capture and process images of satellites during passes. Processed data is then synchronized with a central server which aggregates TLE data, predicts satellite passes, and refines imaging parameters. This document serves as a comprehensive blueprint for the system design and implementation.

---

## 2. System Architecture

### High-Level Components

- **Client Units (Raspberry Pis):**
  - Capture high-resolution images.
  - Perform local image processing and plate solving.
  - Monitor environmental conditions (e.g., cloud coverage).
  - Synchronize data with the central server.

- **Central Server:**
  - Aggregates data from all Pi units.
  - Updates TLE (Two-Line Element) catalogs from external sources.
  - Predicts satellite passes using computational algorithms.
  - Manages centralized data storage and archival.

- **Common Utilities:**
  - Shared libraries and scripts (e.g., logging, configuration management).

### System Diagram

flowchart TD
    subgraph Clients [Raspberry Pi Units]
        A[Image Capture]
        B[Local Processing]
        C[Plate Solving]
        D[Weather Monitoring]
        E[Data Sync via rsync]
    end

    subgraph Server [Central Server]
        F[TLE Update & Aggregation]
        G[Satellite Pass Prediction]
        H[Central Data Storage]
    end

    A --> B
    B --> C
    B --> D
    C --> E
    D --> E
    E --> H
    F --> G
    G --> H
Figure 1: High-Level System Architecture Diagram

## 3. Hardware Components

### Raspberry Pi Unit

- **Processor:** Raspberry Pi (e.g., Pi 5)
- **Camera:** High-sensitivity camera module (IMX477 preferred for its versatility)
- **Local Storage:** MicroSD card for temporary storage of images and logs
- **Connectivity:** Wi-Fi/Ethernet for data synchronization
- **Sensors:** Optional environmental sensors (temperature, humidity)

### Central Server

- **Processor & Memory:** Sufficient CPU and memory to handle multiple data streams and intensive computations.
- **Storage:** Large capacity for aggregated images, logs, and TLE files.
- **Networking:** Robust network interface for simultaneous client connections.

## 4. Software Architecture

### Client-Side (Pi Units)

#### Modules

- **Image Capture Scripts:**  
  - `capture_images.py` & `Capturelmage.py`: Controls camera operations.
  
- **Local Processing:**  
  - `process_frames.py`: Processes captured images (e.g., noise reduction, streak isolation).
  - `extract_ra_dec.py`: Converts pixel coordinates to celestial coordinates using ASTAP output.
  - `plate_solve_astap.py`: Interfaces with the ASTAP tool for plate solving.

- **Environmental Monitoring:**  
  - `wheather_check.py`: Checks local weather conditions.
  - `cloud_coverage_meteo.py` & `check_clouds.py`: Fetch cloud coverage data from external APIs.

- **Setup & Synchronization:**  
  - `dependency_install_pi.sh`: Installs necessary software on the Pi.
  - `setup_pi.sh`: Configures the Pi (e.g., entering latitude/longitude).
  - `sync_to_server.sh`: Uses rsync to transfer data to the server.

### Server-Side

#### Modules

- **Satellite Tracking & TLE Management:**
  - `predict_passes.py`: Predicts satellite passes using TLE data.
  - `update_tle.py`: Fetches and aggregates TLE data from external sources.

- **Server Setup & Process Management:**
  - `dependency_install_server.sh`: Installs required packages on the server.
  - `setup_server.sh`: Prepares the server environment (creates directories, configures settings).
  - `run_server_process.sh`: Manages long-running server processes.

### Common Utilities

- **Shared Library:**
  - `utils.py`: Contains common functions for logging, configuration management, and error handling.

## 5. Data Processing Pipeline

### Image Acquisition and Preprocessing

1. **Capture:**  
   The camera module captures images at scheduled times based on predicted satellite passes.
   
2. **Preprocessing:**  
   Images are enhanced through noise reduction, contrast enhancement, and streak isolation.

flowchart LR
    A[Raw Image Capture] --> B[Preprocessing]
    B --> C[Noise Reduction]
    B --> D[Contrast Enhancement]
    D --> E[Streak Isolation]
Figure 2: Image Preprocessing Pipeline

### Plate Solving & Coordinate Extraction

**Plate Solving:**
    The preprocessed image is analyzed to match star fields using the ASTAP tool, generating a configuration file with key parameters.

**Coordinate Conversion:**
    Using `extract_ra_dec.py`, pixel coordinates along the satellite streak are converted to Right Ascension (RA) and Declination (Dec).
sequenceDiagram
    participant Img as Image
    participant ASTAP as PlateSolving Tool
    participant EXTRACT as `extract_ra_dec.py`
    Img->>ASTAP: Submit image for plate solving
    ASTAP-->>Img: Return configuration parameters (CRPIX, CRVAL, CD matrix)
    Img->>EXTRACT: Convert pixel coordinates to RA/Dec using config
Figure 3: Plate Solving & Coordinate Extraction Sequence

### Satellite Trajectory Analysis

- **Streak Analysis:**
    Multiple points along the satellite streak are extracted.
- **Trajectory Calculation:**
    The change in position over time is computed to derive angular velocity and trajectory.

### Weather Data Integration

- **API Calls:**
    `cloud_coverage_meteo.py` and `check_clouds.py` query weather APIs (e.g., Open-Meteo, NWS) for cloud coverage data.
- **Decision Making:**
    The system uses this data to determine if imaging conditions are favorable.

## 6. Communication & Synchronization

### Data Transfer Protocol

- **Rsync:**  
  Utilized by `sync_to_server.sh` to incrementally and securely synchronize images, logs, and metadata from Pi units to the central server.

### Network Resilience

- **Retry Logic:**  
  Data synchronization scripts incorporate error handling and retry mechanisms to manage intermittent network connectivity.

```mermaid
flowchart TD
    A[Pi Unit Data] --> B[Rsync Process]
    B --> C[Network]
    C --> D[Central Server]
    D -->|ACK| C
    C --> B
Figure 4: Data Synchronization Flow

## 7. Deployment & Maintenance

### Client Deployment (Raspberry Pi)

- **Initial Setup:**  
  - Run `dependency_install_pi.sh` to install dependencies.
  - Execute `setup_pi.sh` to configure geographical parameters.
  
- **Operational Workflow:**  
  - Automatic image capture and local processing.
  - Continuous synchronization using `sync_to_server.sh`.

### Server Deployment

- **Environment Setup:**  
  - Execute `dependency_install_server.sh` followed by `setup_server.sh`.
  
- **Process Management:**  
  - Start server-side processes using `run_server_process.sh`.
  
- **Central Logging:**  
  - All logs are stored in a dedicated `logs/` directory for monitoring and troubleshooting.

## 8. Error Handling, Logging, and Security

- **Logging:**  
  Both Pi units and the server implement robust logging (see `utils.py`) for debugging and system health monitoring.
  
- **Error Handling:**  
  API calls, file operations, and network transfers incorporate retry mechanisms and exception handling.
  
- **Security:**  
  - Secure credentials storage for TLE data fetching.
  - Encrypted data transfers where applicable.
  - Controlled access to configuration files.

## 9. Future Enhancements

- **Scalability:**  
  Expand the system by adding more Pi units to increase geographic coverage.
  
- **Advanced Analytics:**  
  Implement machine learning models for improved image processing and anomaly detection.
  
- **User Interface:**  
  Develop a web dashboard for real-time monitoring, historical data analysis, and system configuration.
  
- **Enhanced Synchronization:**  
  Evaluate alternative data transfer methods to support increased data volumes.

## 10. Conclusion

The design of the Satellite Tracking & Imaging System is centered on a modular, scalable architecture that integrates distributed data capture with centralized processing and predictive analytics. This document provides a detailed blueprint for hardware selection, software components, processing pipelines, synchronization mechanisms, and deployment strategies required for a robust and resilient system. Future enhancements and scalability considerations ensure that the system can evolve as new requirements emerge.

---

*End of Document*