| Name:  | About                                                                    | Priority |
| -------| -------------------------------------------------------------------------|----------| 
|Server  | We need to set up a test server to test our website, database, and rsync |     1    |  
|Website | We Need to set up a basic website that can accept and reject logins      |     2    |
|Database| We Need to set up a database with an ER diagram for dataflow             |     3    |


## Description:

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
  - [ ] Show satellite insights and analytics on dashboard.
  - [ ] Explore machine learning techniques for improved streak detection.
     
