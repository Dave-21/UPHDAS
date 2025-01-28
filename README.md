# UPHDAS
Upper Peninsula High-latitude Domain Awareness System

A Raspberry Pi–based project for autonomously detecting satellites, generating TLE data, and backing up to a central server.

## Table of Contents
1. [Introduction](#introduction)
2. [Goals](#goals)
3. [Project Overview](#project-overview)
4. [Hardware Setup](#hardware-setup)
5. [Software & Environment Setup](#software--environment-setup)
6. [Installation](#installation)
7. [Configuration](#configuration)
8. [Operation](#operation)
9. [Data Flow & Storage](#data-flow--storage)
10. [Scripts](#scripts)
11. [Roadmap / TODOs](#roadmap--todos)
12. [Contributing](#contributing)
13. [License](#license)

---

## Introduction
Welcome to the **Satellite Detection System**! This project aims to:
- Capture night-sky images using a Raspberry Pi camera.
- Detect satellite streaks and generate partial TLEs.
- Compare detections with known satellite catalogs (e.g., Space-Track, N2YO).
- Upload results to a central server for further analysis and archiving.

---

## Goals
1. **Automated Observation**  
   - Operate cameras autonomously overnight, triggered by sunset/sunrise or weather conditions.

2. **Accurate Satellite Detection**  
   - Detect streaks via image processing (e.g., Hough transform).
   - Filter out false positives (planes, noise, etc.).

3. **TLE Generation & Comparison**  
   - Convert streak endpoints to RA/Dec using plate-solving.
   - Fit partial orbital elements, compare with official catalogs.

4. **Centralized Data & Reporting**  
   - Aggregate logs and TLE data on a central server.
   - Provide a user-friendly interface to check status and results.

---

## Project Overview

<details>
<summary><strong>Click to Expand</strong></summary>

### Architecture Diagram
