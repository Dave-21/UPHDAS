# UPHDAS
Upper Peninsula High-latitude Domain Awareness System

<!-- Use badges if relevant, e.g., build status or coverage -->
<!-- [![Build Status](https://github.com/YourOrg/YourRepo/actions/workflows/ci.yml/badge.svg)](https://github.com/YourOrg/YourRepo/actions) -->

## Table of Contents
- [Introduction](#introduction)
- [Project Overview](#project-overview)
  - [Goals and Objectives](#goals-and-objectives)
  - [Key Features](#key-features)
- [System Requirements](#system-requirements)
  - [Hardware Requirements](#hardware-requirements)
  - [Software Requirements](#software-requirements)
- [Architecture](#architecture)
  - [High-Level Diagram](#high-level-diagram)
  - [Data Flow](#data-flow)
- [Hardware Setup](#hardware-setup)
  - [Camera and Lens Selection](#camera-and-lens-selection)
  - [Raspberry Pi Configuration](#raspberry-pi-configuration)
  - [Mounting and Enclosure](#mounting-and-enclosure)
- [Environment Setup](#environment-setup)
  - [Installing Dependencies](#installing-dependencies)
  - [Installing Index Files for Astrometry.net](#installing-index-files-for-astrometrynet)
  - [Network and Server Prep](#network-and-server-prep)
- [Installation](#installation)
  - [Clone the Repository](#clone-the-repository)
  - [Local Installation Steps](#local-installation-steps)
  - [Deployment to Raspberry Pi](#deployment-to-raspberry-pi)
- [Configuration](#configuration)
  - [Config Files](#config-files)
  - [Environmental Variables](#environmental-variables)
  - [Weather API Keys and Secrets](#weather-api-keys-and-secrets)
- [Operation](#operation)
  - [Workflow Overview](#workflow-overview)
  - [Running the Main Scripts](#running-the-main-scripts)
  - [Automated Scheduling](#automated-scheduling)
  - [Data and TLE Generation](#data-and-tle-generation)
  - [Communications Between Units and Server](#communications-between-units-and-server)
  - [Network Configuration](#network-configuration)
- [Scripts](#scripts)
  - [Plate Solving Script](#plate-solving-script)
  - [Satellite Detection Script](#satellite-detection-script)
  - [Weather Check Script](#weather-check-script)
  - [Data Sync/Upload Script](#data-syncupload-script)
- [Data Storage and Format](#data-storage-and-format)
  - [Local Database or File System](#local-database-or-file-system)
  - [Server Database Schema](#server-database-schema)
  - [Backup and Retention Policies](#backup-and-retention-policies)
- [Roadmap / To-Do List](#roadmap--to-do-list)
  - [High-Priority Tasks](#high-priority-tasks)
  - [Medium-Priority Tasks](#medium-priority-tasks)
  - [Low-Priority Tasks](#low-priority-tasks)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)

---

## Introduction
Brief explanation of what the project does and why it exists.  
E.g.,
> This project aims to autonomously detect satellites using a Raspberry Pi and a small-aperture camera, generate TLE data, and back it up to a central server for analysis.

---

## Project Overview

### Goals and Objectives
- List the primary aims, e.g., “Accurately detect satellites at night,” “Automate uploads to a central server,” etc.

### Key Features
- Night-time camera captures  
- Satellite streak detection  
- Automatic TLE generation  
- Weather-based scheduling  

---

## System Requirements

### Hardware Requirements
- **Raspberry Pi 4 or 5** with CSI camera  
- **IMX519** camera sensor (or other if you have updates)  
- **Lens** with focal length X–Y mm  
- **Heater / enclosure** (optional, depending on environment)

### Software Requirements
- **Python 3.8+**  
- **Astrometry.net** (for plate solving)  
- **OpenCV** for image processing  
- Other libraries: `requests`, `numpy`, etc.

---

## Architecture

### High-Level Diagram
> *(Insert a simple block diagram showing the Pi, camera, server, and data flow.)*

### Data Flow
1. Camera captures images  
2. Local detection/plate-solving  
3. TLE generation  
4. Upload to server for analysis & storage  

---

## Hardware Setup

### Camera and Lens Selection
- Explanation of the chosen lens focal length, FOV trade-offs, etc.

### Raspberry Pi Configuration
- Steps for enabling the CSI port and configuring memory split for the GPU.  
- OS and firmware details (e.g., Raspberry Pi OS 64-bit).

### Mounting and Enclosure
- If not on roof, mention recommended angles or baffles.  
- Outdoor-rated cable management.

---

## Environment Setup

### Installing Dependencies
```bash
sudo apt-get update
sudo apt-get install python3 python3-pip astrometry.net ...
pip3 install -r requirements.txt
