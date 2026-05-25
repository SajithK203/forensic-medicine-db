-- =============================================================================
-- FORENSIC MEDICINE DEPARTMENT DATABASE SYSTEM
-- File        : 02_views.sql
-- Description : 12 database views for reporting and data access
-- Run after   : 01_schema.sql and 04_sample_data.sql
-- =============================================================================

USE forensic_medicine_db;

-- =============================================================================
-- VIEW 1: v_ActiveCases
-- All non-closed/archived cases with patient and doctor info
-- =============================================================================
CREATE OR REPLACE VIEW v_ActiveCases AS
SELECT
    fc.CaseID,
    fc.CaseNumber,
    fc.CaseType,
    fc.CaseStatus,
    fc.Priority,
    fc.IncidentDate,
    fc.IncidentLocation,
    fc.PoliceReportNo,
    p.PatientID,
    p.FullName        AS PatientName,
    p.NICPassport,
    p.Gender,
    p.Age,
    p.District,
    d.DoctorID,
    d.FullName        AS DoctorName,
    d.JMOType,
    d.Specialization,
    fc.CreatedAt,
    DATEDIFF(CURDATE(), DATE(fc.IncidentDate)) AS DaysSinceIncident
FROM ForensicCase fc
JOIN Patient p ON fc.PatientID = p.PatientID
JOIN Doctor  d ON fc.DoctorID  = d.DoctorID
WHERE fc.CaseStatus NOT IN ('Closed', 'Archived')
ORDER BY fc.Priority DESC, fc.IncidentDate DESC;


-- =============================================================================
-- VIEW 2: v_CaseFullDetail
-- Complete joined view of all case components
-- =============================================================================
CREATE OR REPLACE VIEW v_CaseFullDetail AS
SELECT
    fc.CaseID,
    fc.CaseNumber,
    fc.CaseType,
    fc.CaseStatus,
    fc.Priority,
    fc.IncidentDate,
    fc.IncidentLocation,
    fc.IncidentType,
    fc.PoliceReportNo,
    fc.CourtCaseNo,
    fc.CaseNotes,
    -- Patient details
    p.PatientID,
    p.FullName          AS PatientName,
    p.NICPassport,
    p.DateOfBirth,
    p.Age,
    p.Gender,
    p.Address,
    p.District,
    p.ContactNo         AS PatientContact,
    p.Occupation,
    -- Doctor details
    d.DoctorID,
    d.FullName          AS DoctorName,
    d.NMCNumber,
    d.JMOType,
    d.Specialization,
    -- Clinical examination (if exists)
    ce.ExaminationID,
    ce.ExaminationDate,
    ce.ExaminationFindings,
    ce.InjuryDetails,
    ce.InvestigationRequired,
    -- Postmortem (if exists)
    pm.PostmortemID,
    pm.AutopsyDate,
    pm.DeathType,
    pm.ImmediateCauseOfDeath,
    pm.ReportStatus     AS PMReportStatus,
    -- Aggregates
    (SELECT COUNT(*) FROM Evidence    e  WHERE e.CaseID  = fc.CaseID) AS EvidenceCount,
    (SELECT COUNT(*) FROM CourtReport cr WHERE cr.CaseID = fc.CaseID) AS ReportCount,
    (SELECT COUNT(*) FROM LaboratoryTest lt
        JOIN Evidence ev ON lt.EvidenceID = ev.EvidenceID
        WHERE ev.CaseID = fc.CaseID) AS LabTestCount,
    fc.CreatedAt,
    fc.UpdatedAt
FROM ForensicCase fc
JOIN Patient p ON fc.PatientID = p.PatientID
JOIN Doctor  d ON fc.DoctorID  = d.DoctorID
LEFT JOIN ClinicalExamination ce ON fc.CaseID = ce.CaseID
LEFT JOIN Postmortem          pm ON fc.CaseID = pm.CaseID;


-- =============================================================================
-- VIEW 3: v_PendingReports
-- Court reports not yet submitted, ordered by age
-- =============================================================================
CREATE OR REPLACE VIEW v_PendingReports AS
SELECT
    cr.ReportID,
    cr.ReportType,
    cr.ReportStatus,
    cr.GeneratedAt,
    cr.CourtName,
    cr.CourtCaseNumber,
    fc.CaseID,
    fc.CaseNumber,
    fc.CaseType,
    p.FullName          AS PatientName,
    d.FullName          AS DoctorName,
    DATEDIFF(CURDATE(), DATE(cr.GeneratedAt)) AS DaysOutstanding
FROM CourtReport cr
JOIN ForensicCase fc ON cr.CaseID   = fc.CaseID
JOIN Patient      p  ON fc.PatientID = p.PatientID
JOIN Doctor       d  ON cr.DoctorID  = d.DoctorID
WHERE cr.ReportStatus IN ('Draft', 'Generated', 'Reviewed')
ORDER BY DaysOutstanding DESC;


-- =============================================================================
-- VIEW 4: v_EvidenceChainOfCustody
-- Evidence items with lab test status and custody chain
-- =============================================================================
CREATE OR REPLACE VIEW v_EvidenceChainOfCustody AS
SELECT
    e.EvidenceID,
    e.EvidenceNumber,
    e.EvidenceType,
    e.BarcodeNumber,
    e.CollectionDate,
    e.CollectedBy,
    e.StorageLocation,
    e.AnalysisStatus,
    e.DisposalStatus,
    e.LastHandledBy,
    e.LastHandledDate,
    e.ChainOfCustody,
    fc.CaseNumber,
    fc.CaseStatus,
    fc.Priority,
    p.FullName          AS PatientName,
    lt.TestID,
    lt.TestType,
    lt.TestStatus       AS LabTestStatus,
    lt.CompletionDate   AS LabCompletionDate,
    lt.TestResult,
    s.FullName          AS TechnicianName
FROM Evidence e
JOIN ForensicCase fc ON e.CaseID     = fc.CaseID
JOIN Patient      p  ON fc.PatientID = p.PatientID
LEFT JOIN LaboratoryTest lt ON e.EvidenceID   = lt.EvidenceID
LEFT JOIN Staff          s  ON lt.TechnicianID = s.StaffID;


-- =============================================================================
-- VIEW 5: v_MonthlyStatistics
-- Case count grouped by month, year and type
-- =============================================================================
CREATE OR REPLACE VIEW v_MonthlyStatistics AS
SELECT
    YEAR(fc.IncidentDate)     AS StatYear,
    MONTH(fc.IncidentDate)    AS StatMonth,
    MONTHNAME(fc.IncidentDate) AS MonthName,
    fc.CaseType,
    COUNT(*)                   AS TotalCases,
    SUM(CASE WHEN fc.CaseStatus = 'Completed' THEN 1 ELSE 0 END) AS CompletedCases,
    SUM(CASE WHEN fc.CaseStatus = 'Pending'   THEN 1 ELSE 0 END) AS PendingCases,
    SUM(CASE WHEN fc.CaseStatus = 'Submitted' THEN 1 ELSE 0 END) AS SubmittedCases,
    SUM(CASE WHEN fc.Priority   = 'Critical'  THEN 1 ELSE 0 END) AS CriticalCases,
    ROUND(AVG(DATEDIFF(IFNULL(fc.UpdatedAt, NOW()), fc.IncidentDate)), 1) AS AvgResolutionDays
FROM ForensicCase fc
GROUP BY StatYear, StatMonth, MonthName, fc.CaseType
ORDER BY StatYear DESC, StatMonth DESC;


-- =============================================================================
-- VIEW 6: v_DoctorCaseLoad
-- Current case workload per active doctor
-- =============================================================================
CREATE OR REPLACE VIEW v_DoctorCaseLoad AS
SELECT
    d.DoctorID,
    d.FullName          AS DoctorName,
    d.JMOType,
    d.Specialization,
    COUNT(fc.CaseID)    AS TotalCases,
    SUM(CASE WHEN fc.CaseStatus = 'Pending'           THEN 1 ELSE 0 END) AS PendingCases,
    SUM(CASE WHEN fc.CaseStatus = 'InProgress'        THEN 1 ELSE 0 END) AS InProgressCases,
    SUM(CASE WHEN fc.CaseStatus = 'Completed'         THEN 1 ELSE 0 END) AS CompletedCases,
    SUM(CASE WHEN fc.CaseType   = 'Autopsy'           THEN 1 ELSE 0 END) AS AutopsyCases,
    SUM(CASE WHEN fc.CaseType   = 'Clinical Forensic' THEN 1 ELSE 0 END) AS ClinicalCases,
    SUM(CASE WHEN fc.CaseType   = 'Clinical & Autopsy' THEN 1 ELSE 0 END) AS CombinedCases,
    MAX(fc.CreatedAt)   AS LastCaseDate
FROM Doctor d
LEFT JOIN ForensicCase fc ON d.DoctorID = fc.DoctorID
WHERE d.IsActive = TRUE
GROUP BY d.DoctorID, d.FullName, d.JMOType, d.Specialization
ORDER BY TotalCases DESC;


-- =============================================================================
-- VIEW 7: v_AutopsyDeathTypes
-- Death type distribution across all postmortems
-- =============================================================================
CREATE OR REPLACE VIEW v_AutopsyDeathTypes AS
SELECT
    pm.DeathType,
    COUNT(*)  AS CaseCount,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM Postmortem), 2) AS Percentage,
    MIN(pm.AutopsyDate) AS EarliestCase,
    MAX(pm.AutopsyDate) AS LatestCase,
    SUM(pm.PhotographsTaken)  AS TotalPhotographs,
    SUM(CASE WHEN pm.SpecimenCollected = TRUE THEN 1 ELSE 0 END) AS SpecimenCollectedCount
FROM Postmortem pm
GROUP BY pm.DeathType
ORDER BY CaseCount DESC;


-- =============================================================================
-- VIEW 8: v_PendingLabTests
-- Lab tests still in Pending or InProgress state
-- =============================================================================
CREATE OR REPLACE VIEW v_PendingLabTests AS
SELECT
    lt.TestID,
    lt.TestType,
    lt.TestStatus,
    lt.TestDate,
    lt.RequestedBy,
    lt.RequestedDate,
    DATEDIFF(CURDATE(), DATE(lt.TestDate)) AS DaysPending,
    e.EvidenceID,
    e.EvidenceNumber,
    e.EvidenceType,
    fc.CaseID,
    fc.CaseNumber,
    fc.Priority         AS CasePriority,
    p.FullName          AS PatientName,
    s.FullName          AS TechnicianName,
    s.ContactNo         AS TechnicianContact
FROM LaboratoryTest lt
JOIN Evidence     e  ON lt.EvidenceID   = e.EvidenceID
JOIN ForensicCase fc ON e.CaseID        = fc.CaseID
JOIN Patient      p  ON fc.PatientID    = p.PatientID
LEFT JOIN Staff   s  ON lt.TechnicianID = s.StaffID
WHERE lt.TestStatus IN ('Pending', 'InProgress')
ORDER BY fc.Priority DESC, lt.TestDate ASC;


-- =============================================================================
-- VIEW 9: v_OverdueCases
-- Cases open for more than 30 days
-- =============================================================================
CREATE OR REPLACE VIEW v_OverdueCases AS
SELECT
    fc.CaseID,
    fc.CaseNumber,
    fc.CaseType,
    fc.CaseStatus,
    fc.Priority,
    fc.IncidentDate,
    fc.PoliceReportNo,
    p.FullName          AS PatientName,
    p.District,
    d.FullName          AS AssignedDoctor,
    d.JMOType,
    DATEDIFF(CURDATE(), DATE(fc.IncidentDate)) AS DaysSinceIncident,
    DATEDIFF(CURDATE(), DATE(fc.CreatedAt))    AS DaysSinceCreation
FROM ForensicCase fc
JOIN Patient p ON fc.PatientID = p.PatientID
JOIN Doctor  d ON fc.DoctorID  = d.DoctorID
WHERE fc.CaseStatus NOT IN ('Completed','Closed','Archived','Submitted')
  AND DATEDIFF(CURDATE(), DATE(fc.IncidentDate)) > 30
ORDER BY DaysSinceIncident DESC;


-- =============================================================================
-- VIEW 10: v_AuditSummary
-- User action summary for the last 30 days
-- =============================================================================
CREATE OR REPLACE VIEW v_AuditSummary AS
SELECT
    al.UserID,
    al.Username,
    al.ActionType,
    al.ModelName,
    COUNT(*)          AS ActionCount,
    MIN(al.LoggedAt)  AS FirstAction,
    MAX(al.LoggedAt)  AS LastAction,
    COUNT(DISTINCT DATE(al.LoggedAt)) AS ActiveDays
FROM ActivityLog al
WHERE al.LoggedAt >= DATE_SUB(NOW(), INTERVAL 30 DAY)
GROUP BY al.UserID, al.Username, al.ActionType, al.ModelName
ORDER BY ActionCount DESC;


-- =============================================================================
-- VIEW 11: v_EvidenceByCase
-- Evidence summary per case
-- =============================================================================
CREATE OR REPLACE VIEW v_EvidenceByCase AS
SELECT
    fc.CaseID,
    fc.CaseNumber,
    fc.CaseType,
    p.FullName          AS PatientName,
    COUNT(e.EvidenceID) AS TotalEvidenceItems,
    SUM(CASE WHEN e.AnalysisStatus = 'Completed' THEN 1 ELSE 0 END) AS AnalyzedItems,
    SUM(CASE WHEN e.AnalysisStatus = 'Pending'   THEN 1 ELSE 0 END) AS PendingItems,
    SUM(CASE WHEN e.AnalysisStatus = 'Failed'    THEN 1 ELSE 0 END) AS FailedItems,
    SUM(CASE WHEN e.DisposalStatus = 'Stored'    THEN 1 ELSE 0 END) AS StoredItems,
    GROUP_CONCAT(DISTINCT e.EvidenceType ORDER BY e.EvidenceType SEPARATOR ', ') AS EvidenceTypes
FROM ForensicCase fc
JOIN Patient p ON fc.PatientID = p.PatientID
LEFT JOIN Evidence e ON fc.CaseID = e.CaseID
GROUP BY fc.CaseID, fc.CaseNumber, fc.CaseType, p.FullName;


-- =============================================================================
-- VIEW 12: v_ReportSubmissionTracker
-- Court report submission status tracker
-- =============================================================================
CREATE OR REPLACE VIEW v_ReportSubmissionTracker AS
SELECT
    cr.ReportID,
    cr.ReportType,
    cr.ReportStatus,
    fc.CaseNumber,
    fc.CaseType,
    p.FullName          AS PatientName,
    d.FullName          AS PreparingDoctor,
    cr.CourtName,
    cr.CourtCaseNumber,
    cr.MagistrateDistrict,
    cr.GeneratedAt,
    cr.SubmittedAt,
    cr.ReceivedAt,
    CASE
        WHEN cr.ReportStatus = 'Received'  THEN 'Complete'
        WHEN cr.ReportStatus = 'Submitted' THEN 'Awaiting Confirmation'
        WHEN cr.ReportStatus = 'Generated' THEN 'Ready for Submission'
        WHEN cr.ReportStatus = 'Reviewed'  THEN 'Under Review'
        WHEN cr.ReportStatus = 'Draft'     THEN 'In Preparation'
        ELSE 'Archived'
    END AS TrackingStatus,
    DATEDIFF(cr.SubmittedAt, cr.GeneratedAt) AS DaysToSubmit,
    DATEDIFF(cr.ReceivedAt,  cr.SubmittedAt) AS DaysToReceive
FROM CourtReport cr
JOIN ForensicCase fc ON cr.CaseID    = fc.CaseID
JOIN Patient      p  ON fc.PatientID = p.PatientID
JOIN Doctor       d  ON cr.DoctorID  = d.DoctorID
ORDER BY cr.GeneratedAt DESC;


-- =============================================================================
-- Verify views created
-- =============================================================================
SELECT TABLE_NAME AS ViewName
FROM INFORMATION_SCHEMA.VIEWS
WHERE TABLE_SCHEMA = 'forensic_medicine_db'
ORDER BY TABLE_NAME;

-- End of 02_views.sql
