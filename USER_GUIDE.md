# Forensic Medicine Department - System User Guide

## Table of Contents
1. [Introduction](#1-introduction)
2. [System Requirements & Installation](#2-system-requirements--installation)
3. [Database Architecture & Setup](#3-database-architecture--setup)
4. [Roles & Credentials](#4-roles--credentials)
5. [User Interface & Navigation](#5-user-interface--navigation)
6. [Role-Specific Workflows](#6-role-specific-workflows)
    - [Administrator](#administrator)
    - [Doctor (JMO)](#doctor-jmo)
    - [Lab Technician](#lab-technician)
    - [Viewer / Investigator](#viewer--investigator)

---

## 1. Introduction
The **Forensic Medicine Database System** is a comprehensive, role-based platform designed to manage sensitive forensic cases, postmortem examinations, evidence tracking, and clinical details securely. Built with Django and backed by a MySQL database, it strictly enforces access control based on user roles, ensuring data integrity and confidentiality.

---

## 2. System Requirements & Installation

### Prerequisites
- **Python**: Version 3.10 or higher.
- **MySQL**: Version 8.0 or higher.
- **Git**: For version control.

### How to Run Manually

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd "Database Project"
   ```

2. **Set Up a Virtual Environment (Recommended)**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Variables**
   Create a `.env` file in the root directory by copying `.env.example`:
   ```bash
   cp .env.example .env
   ```
   *Note: Ensure you update the `DB_PASSWORD` in the `.env` file to match your local MySQL root password.*

5. **Database Setup**
   *(See section 3 for detailed database initialization steps).*

6. **Run the Development Server**
   ```bash
   python manage.py runserver
   ```
   The application will be accessible at `http://127.0.0.1:8000/`.

---

## 3. Database Architecture & Setup

The system relies on a strictly structured MySQL database optimized for forensic data, including cases, patients, clinical reports, postmortems, evidence, and staff records.

### Database Initialization
The `sql/` folder contains scripts to initialize the complete database schema, triggers, stored procedures, and sample data.

1. **Log into MySQL:**
   ```bash
   mysql -u root -p
   ```

2. **Execute the SQL Scripts in Order:**
   ```sql
   -- Create Schema & Tables
   source e:/Database Project/sql/01_schema.sql;
   
   -- Create Views
   source e:/Database Project/sql/02_views.sql;
   
   -- Create Stored Procedures
   source e:/Database Project/sql/03_stored_procedures.sql;
   
   -- Insert Sample Data
   source e:/Database Project/sql/04_sample_data.sql;
   
   -- Test Queries (Optional)
   source e:/Database Project/sql/05_queries.sql;
   
   -- Create Triggers
   source e:/Database Project/sql/06_triggers.sql;
   ```
   *(Alternatively, you can import the consolidated `schema_dump.sql`)*

### Key Database Components
- **Views**: Provide pre-aggregated data (e.g., mortality breakdowns, active cases).
- **Stored Procedures**: Handle complex transactional logic like case assignment and evidence tracking securely.
- **Triggers**: Automate background updates, such as setting a case to "Closed" when the final report is generated.

---

## 4. Roles & Credentials

The system provides different views and access rights depending on the role.

| Role | Username | Password | Access Level |
|---|---|---|---|
| **Administrator** | `admin` | `Admin@123` | Full access, system activity logs, staff management. |
| **Doctor / JMO** | `dr_perera` | `Doctor@123` | Add cases, patients, clinical data, postmortems. |
| **Lab Technician** | `lab_tech` | `Lab@123` | Manage lab tests, evidence, update test status. |
| **Viewer** | `viewer` | `Viewer@123` | Read-only access to specific permitted records. |
| **Django Superuser** | `superuser` | `Superuser@123` | Backend admin panel access only (`/admin`). |

*(Note: The Django Admin Panel is strictly for backend administrative overrides and model management.)*

---

## 5. User Interface & Navigation

### Login Screen
The secure entry point to the system. Enter your role-specific credentials here.

*[Insert Screenshot of Login Page Here]*

### The Dashboard
Upon successful login, a tailored dashboard is presented based on the user's role.
- **KPI Cards**: Quick metrics at the top (e.g., Active Cases, Pending Lab Tests).
- **Navigation Sidebar**: Quick links to Patients, Cases, Evidence, etc.
- **Role-Aware Greeting**: A toast notification briefly confirms your successful login and role.

*[Insert Screenshot of Dashboard Overview Here]*

---

## 6. Role-Specific Workflows

### Administrator
The administrator oversees system operations, audits, and staff management.
- **System Activity Log**: Administrators have exclusive access to a real-time audit log on the dashboard showing who logged in, created, or updated records.
- **Staff Management**: Can add or remove staff members and adjust roles.

*[Insert Screenshot of Administrator Dashboard highlighting System Activity Log Here]*

### Doctor (JMO)
Doctors are the primary data entry personnel for medical cases.
- **Adding a Patient/Case**: Navigate to the "Patients" or "Cases" tab via the sidebar to register new entries.
- **Postmortem & Clinical Data**: Doctors have exclusive buttons to generate reports, submit clinical notes, and add postmortem findings.
- **Dashboard View**: Clean view focusing on Active Cases, Recent Cases, and Overdue Cases.

*[Insert Screenshot of Doctor Dashboard / Case Detail view highlighting Action Buttons Here]*

### Lab Technician
Lab Techs process forensic evidence and update lab results.
- **Evidence Management**: View the "Pending Lab Tests" KPI or navigate to the "Evidence" tab.
- **Updating Results**: Click on an evidence item or test request to mark it as 'In Progress' or 'Completed' and attach result notes.
- **Dashboard View**: Focused heavily on pending tasks and evidence chains of custody.

*[Insert Screenshot of Lab Technician Evidence/Lab Tests view Here]*

### Viewer / Investigator
Viewers have strict read-only access.
- **Viewing Records**: Can search and view case summaries and basic patient details.
- **Restrictions**: Cannot add, edit, or delete any records. Action buttons (like "Add New", "Edit", "Submit Report") are completely hidden from the UI.

*[Insert Screenshot of Viewer Dashboard showing restricted/clean UI Here]*

---
*End of Document*
