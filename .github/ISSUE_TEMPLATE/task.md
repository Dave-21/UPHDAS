# This Week

## Main Tasks (from tasks.md)
- [ ] **Server**: Set up a test server to test our website, database, and rsync. (Priority: 1)
- [ ] **Website**: Set up a basic website that can accept and reject logins. (Priority: 2)
- [ ] **Database**: Set up a database with an ER diagram for data flow. (Priority: 3)

## Additional This Week Tasks
### Pi & Automation Tasks
- [ ] Add debug modes to all critical Pi scripts and update logging to capture key events.
- [ ] Confirm ASTAP Pi plate solve functionality works reliably.
- [ ] Validate the image pipeline end-to-end (rolling_capture.py and related documents).
- [ ] Run the streak detection script on good images.
- [ ] Test the streak detection script on high cloud-covered images to ensure no false positives.
- [ ] Integrate the “decision-to-run” script into the nightly Pi 5 schedule.
- [ ] Configure the Pi 5 to run the complete automation pipeline every night.
- [ ] Run an end-to-end overnight test under high cloud coverage conditions.
- [ ] Implement fallback procedures and error logging/notifications for high cloud coverage.

### Web Interface & Data Flow Tasks
- [ ] Develop a basic web interface with:
  - [ ] Login/Signup functionality.
  - [ ] User management.
  - [ ] Dashboard/Main Homepage.
- [ ] Define the overall data flow for storing and transferring observation data.
- [ ] Specify the data structure for:
  - Validated satellites.
  - Images with satellite streaks (non-validated) including metadata: latitude/longitude, streak points with exact times, exposure length, and capture datetime.
- [ ] Document the directory layout for data storage, retrieval, compression, and archival.

### Coordination & Documentation
- [ ] Hold daily stand-up meetings to review progress and resolve blockers.
- [ ] Continuously update the project GitHub repository with current changes and documentation.
- [ ] Prepare a one-page summary of the data flow, directory structure, and server/web interface design for internal and client review.

---


# Tasks
| Name:   | About                                                                           | Priority |
| ------- | ------------------------------------------------------------------------------- | -------- |
| Server  | Set up a test server to test our website, database, and rsync                   | 1        |
| Website | Set up a basic website that can accept and reject logins                        | 2        |
| Database| Set up a database with an ER diagram for data flow                              | 3        |

---

## Main Project Tasks
- [ ] **Server**: Set up a test server to test our website, database, and rsync.
- [ ] **Website**: Set up a basic website that can accept and reject logins.
- [ ] **Database**: Set up a database with an ER diagram for data flow.

## Pi & Automation Tasks
- [ ] Add debug modes to all critical Pi scripts.
- [ ] Update logging to capture key events and errors.
- [ ] Confirm ASTAP Pi plate solve functionality works reliably.
- [ ] Validate the image pipeline end-to-end (rolling_capture.py and conjunction documents).
- [ ] Run and test the streak detection script on both good and high cloud-covered images (ensure no false positives).
- [ ] Integrate the “decision-to-run” script into the nightly Pi 5 schedule.
- [ ] Configure the Pi 5 for nightly operation of the automation pipeline.
- [ ] Run an end-to-end overnight test (even under high cloud coverage).
- [ ] Implement fallback procedures and error logging/notifications for high cloud coverage.

## Web Interface & Data Flow Tasks
- [ ] Develop a basic web interface with:
  - [ ] Login/Signup functionality.
  - [ ] User management.
  - [ ] Dashboard/Main Homepage.
- [ ] Test user authentication and session management.
- [ ] Define the overall data flow for observation data.
- [ ] Specify the data structure for:
  - Validated satellites.
  - Images with satellite streaks (non-validated) including metadata (latitude/longitude, streak points with exact times, exposure length, capture datetime).
- [ ] Document the directory layout for data storage, compression, and archival.
- [ ] Set up and integrate the website with the test server and database.

## Coordination & Documentation
- [ ] Hold daily stand-up meetings to review progress and resolve blockers.
- [ ] Continuously update the project GitHub repository with current changes and documentation.
- [ ] Prepare a one-page summary of the data flow, directory structure, and server/web interface design for internal and client review.

---

# Additional Features & Enhancements (Optional)

These tasks extend core functionality and add advanced capabilities beyond the basic project scope.

### Global Configuration Management
- [ ] Implement a global `config.yaml` file for admin modification.
- [ ] Ensure Pis fetch all configuration values from `config.yaml` (excluding unit-specific values like lat/long).
- [ ] Develop versioning and validation for configuration updates.

### Advanced Satellite Statistics & Analytics
- [ ] Develop a module to calculate and display satellite capture statistics:
  - [ ] Count satellites captured per school in the last month.
  - [ ] Identify which unit captured the most satellites.
  - [ ] Compute average cloud coverage per unit site.
  - [ ] List satellite names (or relevant identifiers) per observation.
- [ ] Create dashboards or reports to visualize these statistics.
- [ ] Integrate statistical data into the web interface for admin review.

### Enhanced Admin Dashboard Features
- [ ] Allow admin to modify and push configuration changes (global `config.yaml`) directly from the dashboard.
- [ ] Implement user activity logs and audit trails for configuration changes.
- [ ] Add a notifications system for key events and errors reported by Pis.

### Extended Data Flow & Storage Enhancements
- [ ] Define and implement a detailed data schema for storing observation metadata.
- [ ] Automate compression and archival processes for both raw and processed image data.
- [ ] Enhance the directory structure to support scalable data storage and retrieval.

### Future Enhancements (Optional)
- [ ] Show satellite insights and analytics on the dashboard.
- [ ] Explore machine learning techniques for improved streak detection.
