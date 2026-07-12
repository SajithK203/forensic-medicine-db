# 🏥 Forensic Medicine Department — Database System

> Full-stack web application built with **Django 4.2 + MySQL 8.0** for managing forensic medical cases, patient records, postmortems, evidence chain, and court reports.

---

## ✅ What Every Team Member Needs to Install.

Install these **on your own computer** before starting:

| Software | Where to Download |
|---|---|
| **Python 3.10+** | https://python.org/downloads → tick "Add to PATH" during install |
| **MySQL 8.0+** | https://dev.mysql.com/downloads/installer/ → choose "Developer Default" |
| **Git** | https://git-scm.com/downloads |

---

## 🚀 Setup Guide — Run on Your Own Computer

Follow these steps **once** on your machine.

---

### Step 1 — Clone the Project from GitHub

```bash
git clone https://github.com/<your-team-repo>/forensic-db.git
cd forensic-db
```

> If you already cloned it, just pull latest:
> ```bash
> git pull
> ```

---

### Step 2 — Install Python Packages

```bash
pip install -r requirements.txt
```

This installs Django, PyMySQL, Pillow, and python-dotenv automatically.

---

### Step 3 — Create Your `.env` File

The `.env` file holds your **personal** database password. It is never uploaded to GitHub.

**Windows:**
```cmd
copy .env.example .env
```

**Mac / Linux:**
```bash
cp .env.example .env
```

Now open the `.env` file with any text editor (Notepad, VS Code, etc.) and set your MySQL password:

```
SECRET_KEY=django-insecure-forensic-db-change-in-production
DEBUG=True
ALLOWED_HOSTS=localhost 127.0.0.1

DB_NAME=forensic_medicine_db
DB_USER=root
DB_PASSWORD=YOUR_MYSQL_PASSWORD_HERE
DB_HOST=127.0.0.1
DB_PORT=3306
```

> Replace `YOUR_MYSQL_PASSWORD_HERE` with the password you set when installing MySQL.  
> If you have no password, leave `DB_PASSWORD=` blank.

---

### Step 4 — Create the Database in MySQL

Open **MySQL Command Line Client** or **MySQL Workbench** and run:

```sql
CREATE DATABASE forensic_medicine_db
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;
```

Each team member creates this database on **their own MySQL**.

---

### Step 5 — Apply Database Migrations

```bash
python manage.py migrate
```

This creates all the tables in your local MySQL database automatically.

---

### Step 6 — Load Sample Data

```bash
python manage.py seed_data
```

This creates sample patients, cases, staff records, and login accounts on your local database.

---

### Step 7 — Start the Server

```bash
python manage.py runserver
```

Open your browser and go to:

```
http://127.0.0.1:8000/
```

---

## 🔐 Login Accounts

These are created automatically by `seed_data`:

| Username | Password | Role |
|---|---|---|
| `admin` | `Admin@123` | Administrator — full access |
| `dr_perera` | `Doctor@123` | Doctor |
| `dr_silva` | `Doctor@123` | Doctor |
| `lab_tech` | `Lab@123` | Lab Technician |
| `viewer` | `View@123` | View only |

Django Admin panel → `http://127.0.0.1:8000/admin/` (use `admin`)

---

## 🔄 Daily Workflow (After First Setup)

Every day when you want to work on the project:

```bash
# 1. Get the latest code from GitHub
git pull

# 2. If there are new migrations (someone added a model)
python manage.py migrate

# 3. Start the server
python manage.py runserver

# 4. Open browser → http://127.0.0.1:8000/
```

---

## 📤 Push Your Changes to GitHub

```bash
git add .
git commit -m "Short description of what you changed"
git push
```

> ⚠️ Never run `git add .env` — it is already in `.gitignore` and protected.

---

## 📁 Project Structure

```
forensic-db/
│
├── apps/
│   ├── accounts/         # Login / logout / user roles
│   ├── core/             # Dashboard + activity log
│   │   └── management/commands/seed_data.py
│   ├── staff/            # Staff & doctors
│   ├── patients/         # Patient records
│   ├── cases/            # Forensic cases
│   ├── clinical/         # Clinical examinations
│   ├── postmortem/       # Autopsy reports
│   ├── evidence/         # Evidence + lab tests
│   └── reports/          # Court reports
│
├── sql/
│   ├── 01_schema.sql              # All 11 tables
│   ├── 02_views.sql               # 12 database views
│   ├── 03_stored_procedures.sql   # 17 stored procedures
│   ├── 04_sample_data.sql         # Sample records
│   └── 05_queries.sql             # 33 SQL queries
│
├── static/               # CSS and JavaScript
├── templates/            # HTML templates
├── .env                  # ← YOUR local config (never committed)
├── .env.example          # ← Template everyone copies from
├── manage.py
└── requirements.txt
```

---

## ❌ Common Errors & Fixes

### Error: `No module named 'MySQLdb'`
```bash
pip install PyMySQL
```

### Error: `Access denied for user 'root'@'localhost'`
- Open `.env` and double-check `DB_PASSWORD=` is your correct MySQL password

### Error: `Unknown database 'forensic_medicine_db'`
- You skipped Step 4. Go to MySQL and run:
```sql
CREATE DATABASE forensic_medicine_db CHARACTER SET utf8mb4;
```

### Error: `python is not recognized`
- Python was not added to PATH during install
- Uninstall and reinstall Python, ticking **"Add Python to PATH"**

### Error: `pip is not recognized`
```bash
python -m pip install -r requirements.txt
```

### Migrations out of sync after `git pull`
```bash
python manage.py migrate
```
Always run this after pulling new changes.

---

*Forensic Medicine Department — Database Systems Group Project*
