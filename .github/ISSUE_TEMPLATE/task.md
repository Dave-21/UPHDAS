# This Week

## Core Tasks

### Pi Script Enhancements & Debugging (Priority 1)
- [ ] Add debug modes to all critical Pi scripts.
- [ ] Review and update logging to capture key events and errors.

### Plate Solving & Image Pipeline Verification (Priority 1)
- [ ] Confirm ASTAP Pi plate solve functionality works reliably.
- [ ] Validate the image pipeline end-to-end (rolling_capture.py and conjunction documents).

### Streak Detection Testing (Priority 1)
- [ ] Run the streak detection script on good images.
- [ ] Test on high cloud-covered images to ensure no false positives.

### Web Interface – Basic Functionality (Priority 2)
- [ ] Develop a basic website with:
  - [ ] Login/Signup (accept and reject logins)
  - [ ] User Management
  - [ ] Dashboard/Main Homepage

### Data Flow & Directory Structure Design (Priority 3)
- [ ] Define how data will be stored and transferred.
- [ ] Specify structure for:
  - Validated satellites.
  - Images with satellite streaks (non-validated) including metadata: latitude/longitude, points along streak (with exact times), exposure length, and exact capture datetime.
- [ ] Document directory layout and compression/archival procedures.

### Automation & Nightly Operation Integration (Priority 2)
- [ ] Integrate the “decision-to-run” script into the nightly Pi 5 schedule.
- [ ] Run an end-to-end overnight test even under high cloud coverage conditions.

### Fallback & Error Handling Enhancements (Priority 3)
- [ ] Implement fallback procedures for high cloud coverage conditions.
- [ ] Ensure error logging and notifications are operational.
---

## Pre-Defined Tasks from tasks.md

| Name:   | About                                                                           | Priority |
| ------- | ------------------------------------------------------------------------------- | -------- |
| Server  | Set up a test server to test our website, database, and rsync                   | 1        |
| Website | Set up a basic website that can accept and reject logins                        | 2        |
| Database| Set up a database with an ER diagram for data flow                              | 3        |

---

# Additional Features & Enhancements (Post-Barebones)

These tasks extend the core functionality and add advanced capabilities beyond the basic project scope. They are not high priority but are valuable for future improvements.

- [ ] **Global Configuration Management**
  - [ ] Implement a global `config.yaml` file for admin modification.
  - [ ] Ensure Pis fetch all configuration values from `config.yaml` (excluding unit-specific values like lat/long).
  - [ ] Develop versioning and validation for configuration updates.

- [ ] **Advanced Satellite Statistics & Analytics**
  - [ ] Develop a module to calculate and display satellite capture statistics:
    - [ ] Count of satellites captured per school in the last month.
    - [ ] Identify which unit captured the most satellites.
    - [ ] Compute average cloud coverage per unit site.
    - [ ] List satellite names captured (or relevant identifiers) per observation.
  - [ ] Create dashboards or reports to visualize these statistics.
  - [ ] Integrate statistical data into the web interface for admin review.

- [ ] **Enhanced Admin Dashboard Features**
  - [ ] Allow admin to modify and push configuration changes (global `config.yaml`) directly from the dashboard.
  - [ ] Implement user activity logs and audit trails for configuration changes.
  - [ ] Add a notifications system for key events and errors reported by Pis.

- [ ] **Extended Data Flow & Storage Enhancements**
  - [ ] Define and implement a more detailed data schema for storing observation metadata.
  - [ ] Automate compression and archival processes for raw and processed image data.
  - [ ] Enhance directory structure to support scalable data storage and retrieval.

- [ ] **Future Enhancements (Optional)**
  - [ ] Show satellite insights and analytics on the dashboard.
  - [ ] Explore machine learning techniques for improved streak detection.
