-- ============================================================
-- Forensic Medicine Department — 33 Analytical SQL Queries
-- File: sql/05_queries.sql
-- Purpose: Demonstrates SELECT, JOIN, GROUP BY, subqueries,
--          views, and stored procedure calls
-- ============================================================

USE forensic_medicine_db;

-- ═══════════════════════════════════════════════════════════
-- SECTION 1: Basic SELECT Queries
-- ═══════════════════════════════════════════════════════════

-- Q01: List all active doctors with their JMO type
SELECT doctor_id, full_name, jmo_type, specialization, nmc_number
FROM staff_doctor
WHERE is_active = 1
ORDER BY jmo_type, full_name;

-- Q02: List all patients registered in Colombo or Gampaha
SELECT patient_id, full_name, nic_passport, gender, age, district, contact_no
FROM patients_patient
WHERE district IN ('Colombo', 'Gampaha')
ORDER BY full_name;

-- Q03: Find all high and critical priority cases
SELECT case_id, case_number, case_type, case_status, priority, incident_date
FROM cases_forensiccase
WHERE priority IN ('High', 'Critical')
ORDER BY incident_date DESC;

-- Q04: All postmortems where death was Homicidal
SELECT pm.postmortem_id, pm.autopsy_date, pm.immediate_cause,
       pm.cause_a, pm.death_type, c.case_number
FROM postmortem_postmortem pm
JOIN cases_forensiccase c ON pm.case_id = c.case_id
WHERE pm.death_type = 'Homicidal'
ORDER BY pm.autopsy_date DESC;

-- Q05: Evidence items pending lab analysis
SELECT ev.evidence_number, ev.evidence_type, ev.barcode_number,
       ev.collection_date, ev.storage_location, c.case_number
FROM evidence_evidence ev
JOIN cases_forensiccase c ON ev.case_id = c.case_id
WHERE ev.analysis_status = 'Pending'
ORDER BY ev.collection_date ASC;

-- ═══════════════════════════════════════════════════════════
-- SECTION 2: JOIN Queries
-- ═══════════════════════════════════════════════════════════

-- Q06: Full case details — patient, doctor, case info
SELECT c.case_number, c.case_type, c.case_status, c.priority,
       p.full_name AS patient_name, p.nic_passport, p.district,
       d.full_name AS doctor_name, d.jmo_type,
       c.incident_date, c.incident_location, c.incident_type
FROM cases_forensiccase c
JOIN patients_patient p ON c.patient_id = p.patient_id
JOIN staff_doctor d     ON c.doctor_id  = d.doctor_id
ORDER BY c.created_at DESC;

-- Q07: Clinical examinations with case and patient details
SELECT ce.exam_id, c.case_number, p.full_name AS patient_name,
       d.full_name AS doctor_name, ce.examination_date,
       ce.consciousness, ce.injury_details
FROM clinical_clinicalexamination ce
JOIN cases_forensiccase c ON ce.case_id  = c.case_id
JOIN patients_patient p   ON c.patient_id = p.patient_id
JOIN staff_doctor d       ON ce.doctor_id = d.doctor_id
ORDER BY ce.examination_date DESC;

-- Q08: Lab tests with evidence and case numbers
SELECT lt.test_id, lt.test_type, lt.test_status, lt.test_date,
       ev.evidence_number, ev.evidence_type, c.case_number
FROM evidence_laboratorytest lt
JOIN evidence_evidence ev    ON lt.evidence_id = ev.evidence_id
JOIN cases_forensiccase c    ON ev.case_id     = c.case_id
ORDER BY lt.test_date DESC;

-- Q09: Court reports with associated doctor and case details
SELECT rpt.report_id, rpt.report_type, rpt.report_status,
       c.case_number, c.case_type,
       d.full_name AS doctor_name, rpt.court_name,
       rpt.generated_at, rpt.submitted_at
FROM reports_courtreport rpt
JOIN cases_forensiccase c ON rpt.case_id  = c.case_id
JOIN staff_doctor d       ON rpt.doctor_id = d.doctor_id
ORDER BY rpt.generated_at DESC;

-- Q10: All staff with their linked doctor profile (LEFT JOIN)
SELECT s.staff_id, s.full_name, s.staff_type, s.designation,
       d.doctor_id, d.nmc_number, d.jmo_type, d.specialization
FROM staff_staff s
LEFT JOIN staff_doctor d ON d.staff_id = s.staff_id
ORDER BY s.staff_type, s.full_name;

-- ═══════════════════════════════════════════════════════════
-- SECTION 3: Aggregate / GROUP BY Queries
-- ═══════════════════════════════════════════════════════════

-- Q11: Total cases per doctor
SELECT d.full_name AS doctor_name, d.jmo_type,
       COUNT(c.case_id) AS total_cases,
       SUM(CASE WHEN c.case_status = 'Closed' THEN 1 ELSE 0 END) AS closed_cases,
       SUM(CASE WHEN c.case_status IN ('Pending','InProgress') THEN 1 ELSE 0 END) AS open_cases
FROM staff_doctor d
LEFT JOIN cases_forensiccase c ON c.doctor_id = d.doctor_id
GROUP BY d.doctor_id, d.full_name, d.jmo_type
ORDER BY total_cases DESC;

-- Q12: Cases by type
SELECT case_type,
       COUNT(*) AS total,
       SUM(CASE WHEN case_status = 'Completed' THEN 1 ELSE 0 END) AS completed,
       SUM(CASE WHEN case_status = 'Pending'   THEN 1 ELSE 0 END) AS pending
FROM cases_forensiccase
GROUP BY case_type;

-- Q13: Postmortem death type summary with percentage
SELECT death_type, COUNT(*) AS total_cases,
       ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM postmortem_postmortem), 1) AS percentage
FROM postmortem_postmortem
GROUP BY death_type
ORDER BY total_cases DESC;

-- Q14: Evidence collected per month (2026)
SELECT DATE_FORMAT(collection_date, '%Y-%m') AS month,
       COUNT(*) AS evidence_count,
       COUNT(DISTINCT case_id) AS cases_involved
FROM evidence_evidence
WHERE YEAR(collection_date) = 2026
GROUP BY month
ORDER BY month;

-- Q15: Cases per district (via patient)
SELECT p.district, COUNT(c.case_id) AS total_cases
FROM patients_patient p
JOIN cases_forensiccase c ON c.patient_id = p.patient_id
GROUP BY p.district
ORDER BY total_cases DESC;

-- ═══════════════════════════════════════════════════════════
-- SECTION 4: Subquery / Advanced Queries
-- ═══════════════════════════════════════════════════════════

-- Q16: Patients with more than one forensic case
SELECT p.patient_id, p.full_name, p.nic_passport,
       COUNT(c.case_id) AS case_count
FROM patients_patient p
JOIN cases_forensiccase c ON c.patient_id = p.patient_id
GROUP BY p.patient_id, p.full_name, p.nic_passport
HAVING case_count > 1
ORDER BY case_count DESC;

-- Q17: Cases with no evidence collected yet (NOT IN subquery)
SELECT c.case_id, c.case_number, c.case_type, c.case_status,
       p.full_name AS patient_name, c.incident_date
FROM cases_forensiccase c
JOIN patients_patient p ON c.patient_id = p.patient_id
WHERE c.case_id NOT IN (SELECT DISTINCT case_id FROM evidence_evidence)
ORDER BY c.incident_date;

-- Q18: Most active doctor this year
SELECT d.full_name, COUNT(c.case_id) AS cases_this_year
FROM staff_doctor d
JOIN cases_forensiccase c ON c.doctor_id = d.doctor_id
WHERE YEAR(c.incident_date) = YEAR(CURDATE())
GROUP BY d.doctor_id, d.full_name
ORDER BY cases_this_year DESC
LIMIT 1;

-- Q19: Evidence items for critical priority cases
SELECT ev.evidence_number, ev.evidence_type, ev.analysis_status,
       c.case_number, c.priority
FROM evidence_evidence ev
JOIN cases_forensiccase c ON ev.case_id = c.case_id
WHERE c.priority = 'Critical'
ORDER BY ev.collection_date;

-- Q20: Court reports not yet submitted (days pending)
SELECT rpt.report_id, rpt.report_type, rpt.report_status,
       c.case_number, d.full_name AS doctor,
       DATEDIFF(CURDATE(), rpt.generated_at) AS days_pending
FROM reports_courtreport rpt
JOIN cases_forensiccase c ON rpt.case_id  = c.case_id
JOIN staff_doctor d       ON rpt.doctor_id = d.doctor_id
WHERE rpt.report_status IN ('Draft', 'Generated', 'Reviewed')
ORDER BY days_pending DESC;

-- ═══════════════════════════════════════════════════════════
-- SECTION 5: Using Database Views
-- ═══════════════════════════════════════════════════════════

-- Q21: Active cases from view
SELECT * FROM v_ActiveCases LIMIT 20;

-- Q22: Full case details from view (InProgress cases)
SELECT * FROM v_CaseFullDetail WHERE case_status = 'InProgress';

-- Q23: Pending reports from view
SELECT * FROM v_PendingReports;

-- Q24: Deaths by type from view
SELECT * FROM v_DeathsByType;

-- Q25: Doctor workload from view
SELECT * FROM v_DoctorWorkload ORDER BY total_cases DESC;

-- ═══════════════════════════════════════════════════════════
-- SECTION 6: Stored Procedure Calls
-- ═══════════════════════════════════════════════════════════

-- Q26: Generate next case number for current year
CALL sp_GenerateCaseNumber(@new_case_number);
SELECT @new_case_number AS next_case_number;

-- Q27: Get all cases for a specific patient
CALL sp_GetPatientCases('PAT-0001');

-- Q28: Get case summary for a specific case
CALL sp_GetCaseSummary('CASE-00001');

-- Q29: Get statistics report
CALL sp_GetStatisticsReport();

-- Q30: Search cases by keyword
CALL sp_SearchCases('assault');

-- ═══════════════════════════════════════════════════════════
-- SECTION 7: Reporting & Forensic-Specific Queries
-- ═══════════════════════════════════════════════════════════

-- Q31: Average age of patients by case type
SELECT c.case_type,
       ROUND(AVG(p.age), 1) AS avg_patient_age,
       MIN(p.age) AS youngest, MAX(p.age) AS oldest,
       COUNT(DISTINCT c.case_id) AS total_cases
FROM cases_forensiccase c
JOIN patients_patient p ON c.patient_id = p.patient_id
WHERE p.age IS NOT NULL
GROUP BY c.case_type;

-- Q32: Gender breakdown of cases with percentage
SELECT p.gender, COUNT(c.case_id) AS total_cases,
       ROUND(COUNT(c.case_id) * 100.0 / (SELECT COUNT(*) FROM cases_forensiccase), 1) AS percentage
FROM cases_forensiccase c
JOIN patients_patient p ON c.patient_id = p.patient_id
GROUP BY p.gender;

-- Q33: Cases overdue (> 30 days open, not closed/archived)
SELECT c.case_number, c.case_type, c.case_status, c.priority,
       c.incident_date,
       DATEDIFF(CURDATE(), c.incident_date) AS days_open,
       p.full_name AS patient_name, d.full_name AS doctor_name
FROM cases_forensiccase c
JOIN patients_patient p ON c.patient_id = p.patient_id
JOIN staff_doctor d     ON c.doctor_id  = d.doctor_id
WHERE c.case_status NOT IN ('Closed', 'Archived', 'Completed')
  AND c.incident_date < DATE_SUB(CURDATE(), INTERVAL 30 DAY)
ORDER BY days_open DESC;
