# User Guide
## ForensiDB — Forensic Medicine Department Database System
### Group 22 | University of Peradeniya | CO2050 Database Systems
### Submission Date: 23 July 2026

---

## Table of Contents
1. System Overview & Architecture
2. Accessing the System (Live Cloud & Local)
3. Pre-Seeded User Accounts & RBAC Roles
4. Role 1: Administrator Guide
5. Role 2: Doctor (JMO) & Mortuary Guide
6. Role 3: Laboratory Technician Guide
7. Role 4: Viewer Guide (Read-Only & Anonymized Privacy)
8. Mortuary & Autopsy Management Module
9. Audit Logging & System Notifications
10. Troubleshooting & System Maintenance

---

## 1. System Overview & Architecture

**ForensiDB** is a web-based enterprise database management system designed specifically for a **Forensic Medicine Department (FMD)** in a teaching or general hospital environment.

It streamlines the complete medico-legal workflow:
- **Patient & Victim Records**: Centralized registration with strict NIC/Passport uniqueness.
- **Forensic Case Lifecycle**: Comprehensive tracking of Clinical Forensic cases, Autopsies, and Combined cases.
- **Mortuary & Autopsies**: Body intake, mortuary cooler allocation, autopsy scheduling, Cause-of-Death recording, and formal body release.
- **Laboratory Evidence & Chain of Custody**: Barcode tracking, physical evidence handling logs, and toxicology/DNA laboratory test requests.
- **Court Reports**: Automated generation of Medico-Legal Examination Certificates (MLEC) and formal Autopsy Reports for judicial submission.
- **Role-Based Access Control (RBAC)**: Strict role segregation (Administrator, Doctor, Lab Technician, Viewer, Superuser) ensuring patient data privacy and legal chain-of-custody compliance.

---

## 2. Accessing the System (Live Cloud & Local)

### 🌐 Option A: Live AWS Cloud Deployment (Recommended for Lecturer Review)
- **Live Application URL:** `https://forensicdb-group22.duckdns.org/`
- **Django Admin Portal:** `https://forensicdb-group22.duckdns.org/admin/`
- **SSL Security:** Secured with DuckDNS and Let's Encrypt HTTPS certificates running on Nginx + Gunicorn on AWS EC2.

### 💻 Option B: Running Locally (Windows Environment)

#### Step 1: Start MySQL Database Service
1. Press `Win + R`, type `services.msc`, and press **Enter**.
2. Locate **MYSQL80** in the list.
3. Right-click → **Start**.
*(Or run in PowerShell as Administrator: `Start-Service MYSQL80`)*

#### Step 2: Launch Django Server
1. Open PowerShell or Command Prompt.
2. Navigate to the project directory:
   ```powershell
   cd "e:\Database Project"
   ```
3. Run the development server:
   ```powershell
   python manage.py runserver
   ```
4. Access in your browser: `http://127.0.0.1:8000/`

---

## 3. Pre-Seeded User Accounts & RBAC Roles

The system uses **Role-Based Access Control (RBAC)** to ensure staff only see views and data relevant to their medical or administrative duties.

| Role | Username | Password | User Full Name | Primary Access Scope & Dashboards |
|---|---|---|---|---|
| 👑 **Administrator** | `admin` | `Admin@123` | System Admin | Full system control, account management, audit logs, system-wide KPI cards |
| 🩺 **Consultant JMO** | `dr_perera` | `Doctor@123` | Dr. Samantha Perera | Case management, clinical exams, autopsies, court report generation |
| 🩺 **Senior JMO** | `dr_silva` | `Doctor@123` | Dr. Nimal Silva | Clinical examinations, autopsy entries, medico-legal documentation |
| 🧪 **Lab Technician** | `lab_tech` | `Lab@123` | Nuwan Karunaratne | Evidence handling, physical chain of custody, toxicology & DNA lab test results |
| 👁️ **Viewer** | `viewer` | `View@123` | Saman Dissanayake | Read-only departmental overview, aggregated trends, masked patient PII |
| ⚡ **Django Superuser** | `superuser` | `Superuser@123` | Django Superuser | Direct Django Admin portal root access (`/admin/`) |

---

## 4. Role 1: Administrator Guide

The **Administrator** has overarching governance over user accounts, security audit trails, and global departmental statistics.

### 4.1 Administrator Dashboard Overview
Upon logging in as `admin`:
- **6 System KPI Cards**: Displays Total Cases, Active Cases, Total Patients, Pending Evidence, Pending Reports, and Locked User Accounts.
- **System Activity Log**: Full real-time audit trail of all staff logins, logouts, case creations, and status modifications.
- **Auto-Dismiss Toast Banner**: Fades away smoothly after 4 seconds to welcome the administrator.

### 4.2 Managing User Accounts & Security
1. Navigate to **Admin Panel** (`/admin/`).
2. Select **System Users** (`CustomUser`).
3. **To Create a User:**
   - Click **Add CustomUser**.
   - Fill in username, password, full name, and email.
   - Assign the appropriate **Role**: `Administrator`, `Doctor`, `LabTechnician`, or `Viewer`.
4. **To Unlock a Locked Account:**
   - Accounts auto-lock after 5 consecutive failed login attempts (enforced via database trigger `trg_AccountLockout`).
   - Locate the locked user, uncheck `Is locked`, reset `Login attempts` to `0`, and click **Save**.

### 4.3 Monitoring System Activity Audit Logs
1. Administrators can view the **System Activity Log** directly on their home dashboard or under `/admin/core/activitylog/`.
2. Displays timestamped events with user role badges, action types (`CREATE`, `UPDATE`, `LOGIN`, `LOGOUT`), record IDs, and client IP addresses.

---

## 5. Role 2: Doctor (JMO) & Mortuary Guide

The **Doctor (Judicial Medical Officer)** manages clinical examinations, autopsies, cause-of-death declarations, and legal court report submissions.

### 5.1 Doctor Workspace Dashboard
Upon logging in as `dr_perera` or `dr_silva`:
- **Doctor Specific KPIs**: Shows assigned active cases, pending autopsy reports, and medico-legal forms requiring attention.
- **Clean Sidebar Menu**: Filtered specifically for clinical, postmortem, evidence, and report modules.

### 5.2 Case & Patient Management
1. Click **Cases** in the sidebar to view all assigned cases.
2. Click **Open New Case** to register a new medico-legal incident linked to a patient.
3. Search and filter by Case Number, Patient Name, Priority, or Case Type.

### 5.3 Clinical Examinations (Living Patients)
1. Open a case from the case list.
2. Under **Clinical Examinations**, click **Add Examination**.
3. Fill in:
   - Examination Date & Time.
   - Injury Details, Wound Descriptions, and Anatomical Diagrams.
   - Causative Weapon Classification (blunt, sharp, firearm, thermal).
   - Referral requirements and treatment recommendations.
4. Click **Save**.

### 5.4 Court Report Generation & Approval Workflow
1. Open a case and click **Generate Court Report**.
2. Select Report Type: *Clinical Report*, *Postmortem Report*, or *Combined Medico-Legal Report*.
3. Enter Court Name, Court Case Number, Magistrate District, and Legal Opinion.
4. Set status to `Draft`, then update to `Generated` or `Submitted` upon formal court delivery.

---

## 6. Role 3: Laboratory Technician Guide

The **Lab Technician** handles physical evidence items, maintains chain-of-custody logs, and enters laboratory test results.

### 6.1 Laboratory Workspace Dashboard
Upon logging in as `lab_tech`:
- Displays **Pending Evidence Items** and **Pending Lab Tests** requiring processing.
- Direct quick-links to physical evidence inventory and lab testing queues.

### 6.2 Evidence Intake & Barcode Scanning
1. Click **Evidence** in the sidebar.
2. Click **New Evidence Item** or use **Barcode Lookup** to scan an item tag.
3. Fill in evidence type (Blood sample, Viscera, Clothing, Weapon, DNA swab), storage location, and collection date.

### 6.3 Chain of Custody Logging
1. Open any evidence record.
2. Click **Log Custody Action**.
3. Record action: `Collected`, `Transferred`, `Analysed`, `Returned`, or `Disposed`.
4. Enter From/To Locations, Handled By, Purpose, and Condition Notes.
5. *Database Rule*: The system automatically blocks custody logging for disposed/destroyed items via database integrity constraints.

### 6.4 Processing Lab Tests & Automated Status Updates
1. Open an evidence item and click **Add Lab Test** (e.g. *Toxicology Screening*, *DNA Profiling*, *Histopathology*).
2. Once testing is complete, click **Enter Results**.
3. Fill in result details and set status to `Completed`.
4. **Automated Database Trigger:** Marking a test as `Completed` automatically updates the parent evidence item's analysis status to `Completed` via trigger `trg_LabTestCompleteUpdateEvidence`.

---

## 7. Role 4: Viewer Guide (Read-Only & Anonymized Privacy)

The **Viewer** role (`viewer`) is designed for administrative oversight, research, and high-level departmental reporting without compromising confidential patient PII.

### 7.1 Anonymized Patient Privacy Controls
- **Patient PII Masking:** When logged in as `viewer`, sensitive personal data (Full Name, NIC/Passport, Phone Numbers, Address, Emergency Contact) are automatically masked across all pages.
- **Patient Identifiers:** Displays anonymous identifiers (e.g. `Patient #PAT-00007`) in case lists, recent cases tables, and detail views.
- **Read-Only Restrictions:** Create, Edit, Delete, and Status Change buttons are hidden and restricted by backend authorization decorators (`@not_viewer`).

---

## 8. Mortuary & Autopsy Management Module

The **Mortuary & Autopsies** module (`/postmortem/`) is accessible via the sidebar under **Core Modules**.

### 8.1 Body Intake & Mortuary Cooler Allocation
- **Deceased Intake:** Register deceased body arrival time, police report reference, and inquest order date.
- **Mortuary Tracking:** Assign Body Tag Numbers (`body_tag_no`) and Mortuary Refrigerator / Cooler Chamber numbers (`cooler_number`).

### 8.2 Autopsy & Postmortem Examination
1. Under **Mortuary & Autopsies**, click **Add Postmortem Record**.
2. Record Autopsy Date, Start/End Times, Location, and Pathologist findings.
3. **ICD Cause of Death Chain:**
   - **Ia:** Immediate Cause of Death.
   - **Ib:** Underlying Cause (due to).
   - **Ic:** Primary Cause of Death.
   - **II:** Other Significant Contributing Conditions.
4. **Death Classification:** Select from `Homicide`, `Suicide`, `Accident`, `Natural`, or `Undetermined`.
5. *Business Rule*: Enforces a 1-to-1 relationship between a Forensic Case and a Postmortem record.

### 8.3 Body Release & Handover Tracking
- Records formal release of deceased bodies to Next of Kin or Police Officers.
- Tracks `released_to_name`, `relation`, `nic_no`, and official release timestamp for legal clearance.

---

## 9. Audit Logging & System Notifications

### 9.1 Database-Level Audit Triggers
The MySQL database enforces automated audit logging independently of application code:
- **`trg_AccountLockout`**: Auto-locks accounts after 5 failed login attempts.
- **`trg_CaseStatusChangeLog`**: Writes an audit log entry whenever a case status changes.
- **`trg_PreventCompletedEvidenceDeletion`**: Blocks deletion of completed evidence items.
- **`trg_CourtReportSubmissionLog`**: Logs formal submission of court reports.

### 9.2 Auto-Dismissing Toast Messages
Upon login, users receive a non-intrusive, role-aware toast notification at the top of the content area that automatically fades away after **4 seconds**.

---

## 10. Troubleshooting & System Maintenance

| Problem / Error | Cause | Recommended Solution |
|---|---|---|
| **Account Locked on Login** | 5 consecutive failed password attempts | Log in as `admin` or `superuser` in `/admin/` and uncheck `Is locked`. |
| **Server Error (500) on Status Update** | MySQL trigger user reference mismatch | Fixed in latest update. Ensure `python manage.py check` reports clean status. |
| **"NIC/Passport Already Exists"** | Patient already registered in database | Search patient list by NIC or name to open existing record. |
| **Cannot Delete Evidence Item** | Analysis status is `Completed` | Completed evidence cannot be deleted to preserve court chain of custody. |
| **Page Not Loading (Local)** | Django server stopped | Open terminal and run `python manage.py runserver`. |
| **Database Connection Error** | MySQL service stopped | Start `MYSQL80` service via Windows Services. |

---

*End of User Guide*  
*ForensiDB v1.0 — Group 22 — Department of Computer Engineering — University of Peradeniya*  
*CO2050 Database Systems — 23 July 2026*
