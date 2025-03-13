# This Week

| Name                        | About                                                                                                                                         | Priority |
| --------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------- | -------- |
| Technical Dimensions Doc     | Prepare an in-depth document showing all measurement properties for engineering team                                                           | 1        |
| Pi 5 Case     | Find a slim case with fan and good heatsink for Pi 5                                                           | 2        |
| Server                      | Set up a test server to test our website, database, and rsync                                                                                | 1        |
| ~~Website~~                     | ~~Set up a basic website that can accept and reject logins~~                                                                                      | 2        |
| Database                    | Set up a database with an ER diagram for data flow                                                                                            | 3        |
| Pi Debug & Logging          | Add debug modes and update logging in all critical Pi scripts                                                                                 | 1        |
| Plate Solve Verification    | Confirm ASTAP Pi plate solve functionality works reliably                                                                                   | 1        |
| Image Pipeline Validation   | Validate the image pipeline end-to-end (rolling_capture.py and related documents)                                                             | 1        |
| Streak Detection Testing    | Run and test the streak detection script on good images and on high cloud-covered images (ensure no false positives)                             | 1        |
| Automation Integration      | Integrate the “decision-to-run” script into the nightly Pi 5 schedule and configure nightly operation                                          | 1        |
| Overnight Test              | Run an end-to-end overnight test under high cloud coverage conditions                                                                         | 1        |
| Error Handling              | Implement fallback procedures and error logging/notifications for high cloud coverage                                                         | 2        |
| Web Interface Basic         | Develop a basic web interface with login/signup, user management, and a dashboard/main homepage                                                 | 2        |
| Data Flow Definition        | Define the overall data flow for storing/transferring observation data, including structure for validated satellites and image metadata       | 2        |
| Directory Documentation     | Document the directory layout for data storage, retrieval, compression, and archival                                                           | 3        |

---

# Tasks

| Name                        | About                                                                                                                                         | Priority |
| --------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------- | -------- |
| Server                      | Set up a test server to test our website, database, and rsync                                                                                 | 1        |
| Website                     | Set up a basic website that can accept and reject logins                                                                                      | 2        |
| Database                    | Set up a database with an ER diagram for data flow                                                                                            | 3        |
| Pi Debug & Logging          | Add debug modes and update logging in all critical Pi scripts                                                                                 | 1        |
| Plate Solve Verification    | Confirm ASTAP Pi plate solve functionality works reliably                                                                                   | 1        |
| Image Pipeline Validation   | Validate the image pipeline end-to-end (rolling_capture.py and conjunction documents)                                                         | 1        |
| Streak Detection Testing    | Run and test the streak detection script on both good and high cloud-covered images (ensure no false positives)                                 | 1        |
| Automation Integration      | Integrate the “decision-to-run” script into the nightly Pi 5 schedule and configure nightly operation                                          | 1        |
| Overnight Test              | Run an end-to-end overnight test even under high cloud coverage conditions                                                                   | 1        |
| Error Handling & Fallback   | Implement fallback procedures and error logging/notifications for high cloud coverage                                                         | 2        |
| Web Interface Development   | Develop a basic web interface (login/signup, user management, dashboard) and test user authentication/session management                         | 2        |
| Data Flow Definition        | Define the overall data flow for observation data and specify the data structure (validated satellites; images with metadata)                   | 2        |
| Data Structure Specification| Specify metadata details: latitude/longitude, streak points (with times), exposure length, capture datetime                                      | 2        |
| Directory Layout Documentation | Document the directory layout for data storage, compression, and archival                                                                   | 3        |
| Server-Website Integration  | Set up and integrate the website with the test server and database                                                                            | 2        |
| GitHub Documentation Updates| Continuously update the project GitHub repository with current changes and documentation                                                       | 1        |
| Unit & Integration Testing       | Develop and run unit tests for Pi scripts, web interface, and data processing modules; perform full system integration testing                                             | 1        |
| Security & Access Control        | Implement basic security measures (SSL, user session management, access control for admin areas)                                                                         | 2        |
| Documentation & Code Review      | Finalize project documentation (technical docs, user guides, admin manuals) and perform code reviews                                                                     | 2        |
| Deployment Preparation           | Prepare deployment scripts and finalize environment configurations for production                                                                                    | 2        |
| Client Handoff Documentation     | Create final handoff documentation and user training materials for the client                                                                                          | 2        |
| Post-Deployment Monitoring Setup (Web Page) | Set up monitoring and logging for production environment (performance, errors, uptime)                                                                                 | 2        |
| One-page Summary Preparation| Prepare a one-page summary of the data flow, directory structure, and server/web interface design for internal and client review                  | 1        |

---

# Additional Features & Enhancements (Optional)

| Name                         | About                                                                                                                                         | Priority |
| ---------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------- | -------- |
| Global Config Management     | Implement a global `config.yaml` for admin modification; ensure Pis fetch config values (excluding unit-specific lat/long); add versioning      | 4        |
| Advanced Satellite Statistics| Develop a module to calculate/display satellite capture statistics (counts per school, unit performance, average cloud coverage, names)       | 4        |
| Advanced Analytics Dashboard      | Create dashboards or reports to visualize satellite statistics and system performance; integrate analytics into the web interface                                          | 4        |
| Enhanced Admin Dashboard     | Allow admin to modify/push configuration changes directly from the dashboard; add activity logs and notifications                                | 4        |
| TLE Source| Output URL for detected satelltie (given name, generate url for searching that satellite in an online catalog).                               | 5        |
| Extended Data Flow Enhancements| Define and implement a detailed data schema for observation metadata; automate compression/archival; enhance directory structure                | 4        |
| Future Enhancements          | Develop satellite insights/analytics dashboard; explore machine learning for improved streak detection                                           | 5        |
