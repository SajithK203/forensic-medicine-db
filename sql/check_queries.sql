-- =============================================================================
-- FORENSIC MEDICINE DEPARTMENT DATABASE SYSTEM
-- File        : sql/check_queries.sql
-- Group       : 22
-- Description : Complete Viva & Lecturer Demonstration Query Suite
-- Database    : MySQL 8.0 (forensic_medicine_db)
-- Note        : All queries use actual database table names and work 100%
-- =============================================================================

USE forensic_medicine_db;

-- ═════════════════════════════════════════════════════════════════════════════
-- CATEGORY 1: DATABASE PRIVILEGES & SECURITY (GRANT / REVOKE / USER RIGHTS)
-- ═════════════════════════════════════════════════════════════════════════════

-- 1.1 Show all active database users and host permissions
SELECT user, host FROM mysql.user;

-- 1.2 View grants for current user
SHOW GRANTS FOR CURRENT_USER();

-- 1.3 Create a temporary demonstration user
CREATE USER IF NOT EXISTS 'lecturer_demo'@'localhost' IDENTIFIED BY 'DemoPass@123';

-- 1.4 Grant read-only access (SELECT only) to lecturer_demo
GRANT SELECT ON forensic_medicine_db.* TO 'lecturer_demo'@'localhost';
FLUSH PRIVILEGES;

-- 1.5 Show permissions granted to lecturer_demo
SHOW GRANTS FOR 'lecturer_demo'@'localhost';

-- 1.6 Revoke privileges and remove demo user
REVOKE SELECT ON forensic_medicine_db.* FROM 'lecturer_demo'@'localhost';
DROP USER IF EXISTS 'lecturer_demo'@'localhost';


-- ═════════════════════════════════════════════════════════════════════════════
-- CATEGORY 2: BASIC SELECT, FILTERING, SORTING & PATTERNS (WHERE, IN, BETWEEN, LIKE)
-- ═════════════════════════════════════════════════════════════════════════════

-- 2.1 Filtering with WHERE & IN clause (Patients from specific districts)
SELECT patient_id, full_name, nic_passport, gender, age, district, contact_no
FROM patients_patient
WHERE district IN ('Colombo', 'Gampaha', 'Kandy')
ORDER BY district, full_name;

-- 2.2 Range filtering with BETWEEN (Cases registered in 2026)
SELECT case_id, case_number, case_type, priority, case_status, incident_date
FROM cases_forensiccase
WHERE incident_date BETWEEN '2026-01-01' AND '2026-12-31'
ORDER BY incident_date DESC;

-- 2.3 Pattern matching with LIKE (Search case locations or notes)
SELECT case_id, case_number, case_type, incident_location, case_notes
FROM cases_forensiccase
WHERE incident_location LIKE '%Hospital%' OR case_notes LIKE '%assault%'
ORDER BY case_id DESC;


-- ═════════════════════════════════════════════════════════════════════════════
-- CATEGORY 3: JOIN TYPES (INNER, LEFT, RIGHT, MULTI-TABLE JOINS)
-- ═════════════════════════════════════════════════════════════════════════════

-- 3.1 INNER JOIN (Cases with Patient and Doctor information)
SELECT c.case_number, c.case_type, c.case_status, c.priority,
       p.full_name AS patient_name, p.nic_passport, p.district,
       d.full_name AS doctor_name, d.jmo_type
FROM cases_forensiccase c
INNER JOIN patients_patient p ON c.patient_id = p.patient_id
INNER JOIN staff_doctor d     ON c.doctor_id  = d.doctor_id
ORDER BY c.case_id DESC;

-- 3.2 LEFT JOIN (All staff members, including non-doctors)
SELECT s.staff_id, s.full_name, s.staff_type, s.designation,
       d.doctor_id, d.nmc_number, d.jmo_type, d.specialization
FROM staff_staff s
LEFT JOIN staff_doctor d ON d.staff_id = s.staff_id
ORDER BY s.staff_type, s.full_name;

-- 3.3 RIGHT JOIN (All doctors and their assigned cases)
SELECT d.full_name AS doctor_name, d.jmo_type,
       c.case_number, c.case_type, c.case_status
FROM cases_forensiccase c
RIGHT JOIN staff_doctor d ON c.doctor_id = d.doctor_id
ORDER BY d.full_name;

-- 3.4 Multi-Table JOIN (4-Table Link: Lab Test -> Evidence -> Case -> Patient)
SELECT lt.test_id, lt.test_type, lt.test_status, lt.test_date,
       ev.evidence_number, ev.evidence_type,
       c.case_number, c.priority,
       p.full_name AS patient_name
FROM evidence_laboratorytest lt
INNER JOIN evidence_evidence ev ON lt.evidence_id = ev.evidence_id
INNER JOIN cases_forensiccase c ON ev.case_id     = c.case_id
INNER JOIN patients_patient p   ON c.patient_id   = p.patient_id
ORDER BY lt.test_date DESC;


-- ═════════════════════════════════════════════════════════════════════════════
-- CATEGORY 4: AGGREGATIONS & GROUP BY (WITH HAVING CLAUSE)
-- ═════════════════════════════════════════════════════════════════════════════

-- 4.1 Grouping & Conditional Aggregations (Case status breakdown per Doctor)
SELECT d.full_name AS doctor_name, d.jmo_type,
       COUNT(c.case_id) AS total_assigned_cases,
       SUM(CASE WHEN c.case_status = 'Closed' THEN 1 ELSE 0 END) AS closed_cases,
       SUM(CASE WHEN c.case_status IN ('Pending','InProgress') THEN 1 ELSE 0 END) AS active_cases
FROM staff_doctor d
LEFT JOIN cases_forensiccase c ON c.doctor_id = d.doctor_id
GROUP BY d.doctor_id, d.full_name, d.jmo_type
ORDER BY total_assigned_cases DESC;

-- 4.2 Statistical Aggregate (Average, Min, Max patient age by Case Type)
SELECT c.case_type,
       COUNT(c.case_id) AS total_cases,
       ROUND(AVG(p.age), 1) AS avg_patient_age,
       MIN(p.age) AS youngest_patient,
       MAX(p.age) AS oldest_patient
FROM cases_forensiccase c
INNER JOIN patients_patient p ON c.patient_id = p.patient_id
WHERE p.age IS NOT NULL
GROUP BY c.case_type;

-- 4.3 Filtering aggregated results using HAVING clause (Patients with >= 1 case)
SELECT p.patient_id, p.full_name, p.nic_passport,
       COUNT(c.case_id) AS case_count
FROM patients_patient p
INNER JOIN cases_forensiccase c ON c.patient_id = p.patient_id
GROUP BY p.patient_id, p.full_name, p.nic_passport
HAVING case_count >= 1
ORDER BY case_count DESC;


-- ═════════════════════════════════════════════════════════════════════════════
-- CATEGORY 5: SUBQUERIES & NESTED QUERIES
-- ═════════════════════════════════════════════════════════════════════════════

-- 5.1 Correlated Subquery (Death type percentage distribution)
SELECT death_type,
       COUNT(*) AS case_count,
       ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM postmortem_postmortem), 1) AS percentage
FROM postmortem_postmortem
GROUP BY death_type
ORDER BY case_count DESC;

-- 5.2 NOT IN Subquery (Find cases with ZERO evidence items collected)
SELECT c.case_id, c.case_number, c.case_type, c.case_status,
       p.full_name AS patient_name, c.incident_date
FROM cases_forensiccase c
INNER JOIN patients_patient p ON c.patient_id = p.patient_id
WHERE c.case_id NOT IN (SELECT DISTINCT case_id FROM evidence_evidence)
ORDER BY c.incident_date DESC;

-- 5.3 Date Calculation Subquery (Cases open for more than 30 days)
SELECT c.case_number, c.case_type, c.case_status, c.priority,
       c.incident_date,
       DATEDIFF(CURDATE(), c.incident_date) AS days_open,
       p.full_name AS patient_name
FROM cases_forensiccase c
INNER JOIN patients_patient p ON c.patient_id = p.patient_id
WHERE c.case_status NOT IN ('Closed', 'Archived', 'Completed')
  AND c.incident_date < DATE_SUB(CURDATE(), INTERVAL 30 DAY)
ORDER BY days_open DESC;


-- ═════════════════════════════════════════════════════════════════════════════
-- CATEGORY 6: DATABASE VIEWS
-- ═════════════════════════════════════════════════════════════════════════════

-- 6.1 Inspect all views created in database
SELECT TABLE_NAME AS ViewName
FROM INFORMATION_SCHEMA.VIEWS
WHERE TABLE_SCHEMA = 'forensic_medicine_db'
ORDER BY TABLE_NAME;

-- 6.2 Query Active Cases View
SELECT * FROM v_ActiveCases LIMIT 10;

-- 6.3 Query Doctor Workload View
SELECT * FROM v_DoctorWorkload ORDER BY total_cases DESC;


-- ═════════════════════════════════════════════════════════════════════════════
-- CATEGORY 7: TRIGGERS & AUDIT LOG DEMONSTRATION
-- ═════════════════════════════════════════════════════════════════════════════

-- 7.1 List all 8 active database triggers
SELECT TRIGGER_NAME, EVENT_MANIPULATION, EVENT_OBJECT_TABLE, ACTION_TIMING
FROM INFORMATION_SCHEMA.TRIGGERS
WHERE TRIGGER_SCHEMA = 'forensic_medicine_db'
ORDER BY EVENT_OBJECT_TABLE;

-- 7.2 Safe Trigger Execution Demo (Uses START TRANSACTION & ROLLBACK so data is NOT altered!)
START TRANSACTION;

-- Step A: Update case status (Fires trg_CaseStatusChangeLog trigger automatically)
UPDATE cases_forensiccase
SET case_status = 'Closed'
WHERE case_id = 'CASE-00001';

-- Step B: Verify Trigger Audit Output in core_activitylog
SELECT username, action_type, model_name, action_details, logged_at
FROM core_activitylog
WHERE username = 'SYSTEM_TRIGGER'
ORDER BY logged_at DESC
LIMIT 1;

-- Step C: Undo the changes completely so your database data remains 100% original!
ROLLBACK;

-- End of 07_viva_demo.sql
