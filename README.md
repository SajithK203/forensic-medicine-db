<div align="center">

  <h1>🏥 Forensic Medicine Department Database System</h1>
  <h3><i>ForensiDB — A Complete Medico-Legal Enterprise Solution</i></h3>

  <p>
    <b>Designed & Developed by Group 22</b><br>
    Department of Computer Engineering • Faculty of Engineering • University of Peradeniya<br>
    Course: CO2050 Database Systems • Lecturer: Mr. Biswajith • Date: 23 July 2026
  </p>

  <p>
    <a href="https://forensicdb-group22.duckdns.org/"><img src="https://img.shields.io/badge/Live_Domain-HTTPS-success?style=for-the-badge&logo=letsencrypt&logoColor=white" alt="Live Domain"></a>
    <a href="http://3.85.81.252/"><img src="https://img.shields.io/badge/AWS_EC2-Live_IP-orange?style=for-the-badge&logo=amazon-aws&logoColor=white" alt="AWS Server"></a>
    <a href="https://djangoproject.com"><img src="https://img.shields.io/badge/Django-4.2_LTS-092E20?style=for-the-badge&logo=django&logoColor=white" alt="Django"></a>
    <a href="https://mysql.com"><img src="https://img.shields.io/badge/MySQL-8.0_Enterprise-4479A1?style=for-the-badge&logo=mysql&logoColor=white" alt="MySQL"></a>
    <a href="https://nginx.org"><img src="https://img.shields.io/badge/Nginx-Reverse_Proxy-009639?style=for-the-badge&logo=nginx&logoColor=white" alt="Nginx"></a>
  </p>

  ---
</div>

> [!IMPORTANT]
> **Production Status:** 🟢 **100% Operational & Live 24/7**  
> Backed by an **AWS EC2 Ubuntu Server**, **Nginx reverse proxy**, **Gunicorn WSGI**, and **MySQL 8.0** with 26 tables, 12 views, 17 stored procedures, and 8 triggers.

---

## 🌐 Live Production Application Links

| Endpoint | Link | Description | Security |
|---|---|---|---|
| 🔒 **Live Secure Domain** | 👉 **[https://forensicdb-group22.duckdns.org/](https://forensicdb-group22.duckdns.org/)** | **Primary Link** — Global 24/7 Access | 🟢 SSL Encrypted |
| 🌐 **Public Server IP** | 👉 **[http://3.85.81.252/](http://3.85.81.252/)** | Direct AWS EC2 IPv4 Address | 🟡 HTTP |
| ⚙️ **Django Admin Portal** | 👉 **[https://forensicdb-group22.duckdns.org/admin/](https://forensicdb-group22.duckdns.org/admin/)** | Backend Administrative Console | 🔒 Staff Only |

---

## 🎓 Academic & Group Details

<table align="center">
  <tr>
    <td><b>Course</b></td>
    <td>CO2050 — Database Systems</td>
    <td><b>Institution</b></td>
    <td>University of Peradeniya</td>
  </tr>
  <tr>
    <td><b>Faculty</b></td>
    <td>Faculty of Engineering</td>
    <td><b>Department</b></td>
    <td>Department of Computer Engineering</td>
  </tr>
  <tr>
    <td><b>Group Number</b></td>
    <td>Group 22</td>
    <td><b>Lecturer</b></td>
    <td>Mr. Biswajith</td>
  </tr>
  <tr>
    <td><b>Submission Date</b></td>
    <td colspan="3">23 July 2026</td>
  </tr>
</table>

### 👥 Group Members

| Name | Registration Number | Primary Role & Contributions |
|---|---|---|
| **R.M.S.S. Kumara** | `E/22/203` | Team Lead / Django Backend / Database Integration |
| **A.W.H. Panchani** | `E/22/269` | Database Architect / Schema (DDL) / Views & Procedures |
| **K.D. Ashen** | `E/22/032` | Frontend Engineer / HTML5 & CSS3 UI / Chart.js Dashboard |
| **W.A.N. Gunathilaka** | `E/22/121` | Quality Assurance / SQL Queries / Triggers / Documentation |

---

## 🔐 Pre-Seeded Demo Login Credentials

Use these test accounts to evaluate the system's **Role-Based Access Control (RBAC)** mechanisms and Django Admin Portal:

| Role | Username | Password | User Full Name | Access Scope & Permissions |
|---|---|---|---|---|
| ⚡ **Django Superuser** | `superuser` | `Superuser@123` | Django Superuser | Full Django Admin portal root access |
| 👑 **Administrator** | `admin` | `Admin@123` | System Admin | Full system control, user accounts, audit trail logs |
| 🩺 **Consultant JMO** | `dr_perera` | `Doctor@123` | Dr. Samantha Perera | Case management, clinical exams, postmortem autopsies |
| 🩺 **Senior JMO** | `dr_silva` | `Doctor@123` | Dr. Nimal Silva | Examination entries, court report generation |
| 🧪 **Lab Technician** | `lab_tech` | `Lab@123` | Nuwan Karunaratne | Physical evidence tracking, lab test processing, custody log |
| 👁️ **Viewer** | `viewer` | `View@123` | Saman Dissanayake | Read-only departmental record access |

---

## 📊 Database Architecture Summary

> [!NOTE]
> The database schema is strictly normalized to **Third Normal Form (3NF)** to eliminate data redundancy and ensure legal non-repudiation.

```
┌────────────────────────────────────────────────────────────────────────┐
│                   Forensic Medicine Database System                   │
├───────────────────────────────────┬────────────────────────────────────┤
│ 17 Core Business Tables           │ 9 Framework System Tables          │
│ 12 Analytical Database Views      │ 17 Business Logic Stored Procedures│
│ 8 Automated DBMS Triggers         │ 33 Categorized SQL Queries         │
└───────────────────────────────────┴────────────────────────────────────┘
```

<details>
<summary><b>🔍 View Complete SQL File Breakdown</b></summary>

| Script File | Type | Description |
|---|---|---|
| `sql/01_schema.sql` | **DDL** | Table definitions, primary keys, foreign keys, UNIQUE, CHECK constraints, & indexes |
| `sql/02_views.sql` | **Views** | 12 custom SQL views for active cases, doctor workload, mortality analysis, & reports |
| `sql/03_stored_procedures.sql` | **Procedures** | 17 procedures for ID generation sequences (PAT-XXXX, FMD-YYYY-XXXX), status updates |
| `sql/04_sample_data.sql` | **DML** | Realistic Sri Lankan sample records for patients, staff, and doctors |
| `sql/05_queries.sql` | **Queries** | 33 analytical queries covering SELECT, JOIN, GROUP BY, subqueries, & aggregations |
| `sql/06_triggers.sql` | **Triggers** | 8 database triggers for account lockout, audit logs, and evidence deletion blocks |

</details>

---

## 💻 Manual Setup & Execution Guide (Local PC Installation)

> [!TIP]
> Follow these instructions to set up, build, and evaluate the complete system locally on a development PC.

### 1. Prerequisites
- **Python 3.10+** (Ensure "Add Python to PATH" is ticked during installation)
- **MySQL 8.0+** (Server + MySQL Workbench or Command Line Client)
- **Git**

---

### 2. Step-by-Step Local Setup

#### Step 2.1 — Clone the Repository
```bash
git clone https://github.com/SajithK203/forensic-medicine-db.git
cd forensic-medicine-db
```

#### Step 2.2 — Install Python Dependencies
```bash
pip install -r requirements.txt
```

#### Step 2.3 — Create Environment Configuration (`.env`)
Copy `.env.example` to `.env`:
```cmd
copy .env.example .env
```
Configure your local database credentials inside `.env`:
```env
SECRET_KEY=django-insecure-forensic-db-local-key
DEBUG=True
ALLOWED_HOSTS=localhost 127.0.0.1

DB_NAME=forensic_medicine_db
DB_USER=root
DB_PASSWORD=YOUR_LOCAL_MYSQL_PASSWORD
DB_HOST=127.0.0.1
DB_PORT=3306
```

#### Step 2.4 — Execute SQL Scripts in MySQL
Run the SQL scripts located in the `sql/` directory in this exact order:

```sql
-- 1. Create Schema & Constraints (DDL)
mysql -u root -p < sql/01_schema.sql

-- 2. Create Database Views (12 Views)
mysql -u root -p < sql/02_views.sql

-- 3. Create Stored Procedures (17 Procedures)
mysql -u root -p < sql/03_stored_procedures.sql

-- 4. Create Database Triggers (8 Triggers)
mysql -u root -p < sql/06_triggers.sql
```

#### Step 2.5 — Apply Django Migrations & Seed Data
```bash
# Apply Django migrations to construct application tables
python manage.py migrate

# Seed sample data (Patients, Doctors, Cases, Evidence, Autopsies, Reports, Users)
python manage.py seed_data

# Import DML sample records
mysql -u root -p forensic_medicine_db < sql/04_sample_data.sql
```

#### Step 2.6 — Launch Local Server
```bash
python manage.py runserver
```

Open browser → **`http://127.0.0.1:8000/`**

---

## 🛠️ Tech Stack & Infrastructure Specs

<p align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white" alt="Django">
  <img src="https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white" alt="MySQL">
  <img src="https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white" alt="HTML5">
  <img src="https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white" alt="CSS3">
  <img src="https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black" alt="JavaScript">
  <img src="https://img.shields.io/badge/Chart.js-FF6384?style=for-the-badge&logo=chartdotjs&logoColor=white" alt="Chart.js">
  <img src="https://img.shields.io/badge/AWS_EC2-FF9900?style=for-the-badge&logo=amazonaws&logoColor=white" alt="AWS EC2">
  <img src="https://img.shields.io/badge/Nginx-009639?style=for-the-badge&logo=nginx&logoColor=white" alt="Nginx">
  <img src="https://img.shields.io/badge/Gunicorn-4B8BBE?style=for-the-badge&logo=gunicorn&logoColor=white" alt="Gunicorn">
</p>

---

## 📁 Repository Folder Structure

```
forensic-medicine-db/
├── apps/
│   ├── accounts/         # Authentication, RBAC, lockout protection
│   ├── core/             # Dashboard, activity log, notifications
│   ├── staff/            # Staff & doctor profiles
│   ├── patients/         # Patient registration & records
│   ├── cases/            # Forensic case lifecycle management
│   ├── clinical/         # Clinical forensic examinations
│   ├── postmortem/       # Autopsies & mortuary management
│   ├── evidence/         # Evidence tracking, lab tests, chain of custody
│   └── reports/          # Medico-legal court report generation
├── sql/
│   ├── 01_schema.sql              # DDL — Database & Table creation
│   ├── 02_views.sql               # 12 Database Views
│   ├── 03_stored_procedures.sql   # 17 Stored Procedures
│   ├── 04_sample_data.sql         # Sample records
│   ├── 05_queries.sql             # 33 SQL Queries
│   └── 06_triggers.sql            # 8 Database Triggers
├── static/               # CSS stylesheets & JavaScript files
├── templates/            # Responsive HTML5 templates
├── manage.py
└── requirements.txt
```

---

<div align="center">
  <sub>Forensic Medicine Department Database System • Group 22 • University of Peradeniya • 2026</sub>
</div>
