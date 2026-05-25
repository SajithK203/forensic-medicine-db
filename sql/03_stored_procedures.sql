-- =============================================================================
-- FORENSIC MEDICINE DEPARTMENT DATABASE SYSTEM
-- File        : 03_stored_procedures.sql
-- Description : 17 stored procedures for core business logic
-- Run after   : 01_schema.sql
-- =============================================================================

USE forensic_medicine_db;

DELIMITER $$

-- =============================================================================
-- SP 1: sp_GenerateCaseNumber
-- Generates next sequential case number: FMD-YYYY-XXXX
-- =============================================================================
CREATE PROCEDURE sp_GenerateCaseNumber(OUT p_CaseNumber VARCHAR(30))
BEGIN
    DECLARE v_Year    CHAR(4);
    DECLARE v_Count   INT;
    DECLARE v_Seq     VARCHAR(4);

    SET v_Year  = YEAR(CURDATE());
    SELECT COUNT(*) + 1 INTO v_Count
    FROM ForensicCase
    WHERE YEAR(IncidentDate) = v_Year;

    SET v_Seq = LPAD(v_Count, 4, '0');
    SET p_CaseNumber = CONCAT('FMD-', v_Year, '-', v_Seq);
END$$


-- =============================================================================
-- SP 2: sp_GeneratePatientID
-- Generates next sequential patient ID: PAT-XXXX
-- =============================================================================
CREATE PROCEDURE sp_GeneratePatientID(OUT p_PatientID VARCHAR(15))
BEGIN
    DECLARE v_Count INT;

    SELECT COUNT(*) + 1 INTO v_Count FROM Patient;
    SET p_PatientID = CONCAT('PAT-', LPAD(v_Count, 4, '0'));
END$$


-- =============================================================================
-- SP 3: sp_RegisterPatient
-- Validates NIC uniqueness and inserts new patient
-- =============================================================================
CREATE PROCEDURE sp_RegisterPatient(
    IN  p_FullName              VARCHAR(100),
    IN  p_NICPassport           VARCHAR(20),
    IN  p_DateOfBirth           DATE,
    IN  p_Age                   TINYINT,
    IN  p_Gender                VARCHAR(10),
    IN  p_Address               VARCHAR(300),
    IN  p_District              VARCHAR(50),
    IN  p_ContactNo             VARCHAR(15),
    IN  p_EmergencyContactName  VARCHAR(100),
    IN  p_EmergencyContactNo    VARCHAR(15),
    IN  p_CivilStatus           VARCHAR(20),
    IN  p_Occupation            VARCHAR(100),
    OUT p_PatientID             VARCHAR(15),
    OUT p_StatusCode            INT,
    OUT p_Message               VARCHAR(200)
)
BEGIN
    DECLARE v_Exists INT DEFAULT 0;

    -- Check NIC uniqueness
    SELECT COUNT(*) INTO v_Exists FROM Patient WHERE NICPassport = p_NICPassport;

    IF v_Exists > 0 THEN
        SET p_PatientID  = NULL;
        SET p_StatusCode = -1;
        SET p_Message    = CONCAT('Patient with NIC/Passport ', p_NICPassport, ' already exists.');
    ELSE
        CALL sp_GeneratePatientID(p_PatientID);

        INSERT INTO Patient (
            PatientID, FullName, NICPassport, DateOfBirth, Age, Gender,
            Address, District, ContactNo, EmergencyContactName,
            EmergencyContactNo, CivilStatus, Occupation
        ) VALUES (
            p_PatientID, p_FullName, p_NICPassport, p_DateOfBirth, p_Age, p_Gender,
            p_Address, p_District, p_ContactNo, p_EmergencyContactName,
            p_EmergencyContactNo, p_CivilStatus, p_Occupation
        );

        SET p_StatusCode = 1;
        SET p_Message    = CONCAT('Patient registered successfully with ID: ', p_PatientID);
    END IF;
END$$


-- =============================================================================
-- SP 4: sp_CreateCase
-- Creates a new forensic case with auto-generated case number
-- =============================================================================
CREATE PROCEDURE sp_CreateCase(
    IN  p_PatientID        VARCHAR(15),
    IN  p_DoctorID         VARCHAR(15),
    IN  p_CaseType         VARCHAR(30),
    IN  p_IncidentDate     DATETIME,
    IN  p_IncidentLocation VARCHAR(300),
    IN  p_IncidentType     VARCHAR(100),
    IN  p_PoliceReportNo   VARCHAR(50),
    IN  p_Priority         VARCHAR(10),
    IN  p_CaseNotes        LONGTEXT,
    OUT p_CaseID           VARCHAR(20),
    OUT p_CaseNumber       VARCHAR(30),
    OUT p_StatusCode       INT,
    OUT p_Message          VARCHAR(200)
)
BEGIN
    DECLARE v_PatientExists INT DEFAULT 0;
    DECLARE v_DoctorExists  INT DEFAULT 0;
    DECLARE v_SeqNum        INT;

    SELECT COUNT(*) INTO v_PatientExists FROM Patient WHERE PatientID = p_PatientID;
    SELECT COUNT(*) INTO v_DoctorExists  FROM Doctor  WHERE DoctorID  = p_DoctorID AND IsActive = TRUE;

    IF v_PatientExists = 0 THEN
        SET p_CaseID     = NULL;
        SET p_CaseNumber = NULL;
        SET p_StatusCode = -1;
        SET p_Message    = 'Patient not found.';

    ELSEIF v_DoctorExists = 0 THEN
        SET p_CaseID     = NULL;
        SET p_CaseNumber = NULL;
        SET p_StatusCode = -2;
        SET p_Message    = 'Doctor not found or inactive.';

    ELSE
        -- Generate CaseNumber
        CALL sp_GenerateCaseNumber(p_CaseNumber);

        -- Generate CaseID
        SELECT COUNT(*) + 1 INTO v_SeqNum FROM ForensicCase;
        SET p_CaseID = CONCAT('CASE-', LPAD(v_SeqNum, 5, '0'));

        INSERT INTO ForensicCase (
            CaseID, CaseNumber, PatientID, DoctorID, CaseType,
            IncidentDate, IncidentLocation, IncidentType,
            PoliceReportNo, Priority, CaseNotes
        ) VALUES (
            p_CaseID, p_CaseNumber, p_PatientID, p_DoctorID, p_CaseType,
            p_IncidentDate, p_IncidentLocation, p_IncidentType,
            p_PoliceReportNo, p_Priority, p_CaseNotes
        );

        SET p_StatusCode = 1;
        SET p_Message    = CONCAT('Case created: ', p_CaseNumber);
    END IF;
END$$


-- =============================================================================
-- SP 5: sp_UpdateCaseStatus
-- Updates case status with validation of allowed transitions
-- =============================================================================
CREATE PROCEDURE sp_UpdateCaseStatus(
    IN  p_CaseID     VARCHAR(20),
    IN  p_NewStatus  VARCHAR(20),
    IN  p_ChangedBy  VARCHAR(50),
    OUT p_StatusCode INT,
    OUT p_Message    VARCHAR(200)
)
BEGIN
    DECLARE v_CurrentStatus VARCHAR(20);
    DECLARE v_Allowed       INT DEFAULT 0;

    SELECT CaseStatus INTO v_CurrentStatus FROM ForensicCase WHERE CaseID = p_CaseID;

    IF v_CurrentStatus IS NULL THEN
        SET p_StatusCode = -1;
        SET p_Message    = 'Case not found.';
    ELSE
        -- Validate transition
        SET v_Allowed = CASE
            WHEN v_CurrentStatus = 'Pending'    AND p_NewStatus IN ('InProgress','Closed')          THEN 1
            WHEN v_CurrentStatus = 'InProgress' AND p_NewStatus IN ('Completed','Pending')           THEN 1
            WHEN v_CurrentStatus = 'Completed'  AND p_NewStatus IN ('Submitted','InProgress')        THEN 1
            WHEN v_CurrentStatus = 'Submitted'  AND p_NewStatus IN ('Closed','Completed')            THEN 1
            WHEN v_CurrentStatus = 'Closed'     AND p_NewStatus = 'Archived'                        THEN 1
            ELSE 0
        END;

        IF v_Allowed = 0 THEN
            SET p_StatusCode = -2;
            SET p_Message    = CONCAT('Invalid transition: ', v_CurrentStatus, ' -> ', p_NewStatus);
        ELSE
            UPDATE ForensicCase
            SET CaseStatus = p_NewStatus,
                CaseNotes  = CONCAT(IFNULL(CaseNotes,''), '\n[', NOW(), '] Status changed to ', p_NewStatus, ' by ', p_ChangedBy)
            WHERE CaseID = p_CaseID;

            SET p_StatusCode = 1;
            SET p_Message    = CONCAT('Status updated to: ', p_NewStatus);
        END IF;
    END IF;
END$$


-- =============================================================================
-- SP 6: sp_AddEvidence
-- Adds evidence item with auto-generated barcode
-- =============================================================================
CREATE PROCEDURE sp_AddEvidence(
    IN  p_CaseID              VARCHAR(20),
    IN  p_EvidenceType        VARCHAR(100),
    IN  p_EvidenceDescription LONGTEXT,
    IN  p_CollectionDate      DATETIME,
    IN  p_CollectedBy         VARCHAR(100),
    IN  p_StorageLocation     VARCHAR(300),
    IN  p_StorageConditions   VARCHAR(300),
    OUT p_EvidenceID          VARCHAR(20),
    OUT p_EvidenceNumber      VARCHAR(50),
    OUT p_BarcodeNumber       VARCHAR(100),
    OUT p_StatusCode          INT,
    OUT p_Message             VARCHAR(200)
)
BEGIN
    DECLARE v_SeqNum INT;
    DECLARE v_Year   CHAR(4);

    SELECT COUNT(*) INTO v_SeqNum FROM Evidence WHERE CaseID = p_CaseID;
    SET v_Year        = YEAR(CURDATE());
    SET v_SeqNum      = v_SeqNum + 1;

    -- Generate IDs
    SELECT CONCAT('EV-', LPAD((SELECT COUNT(*)+1 FROM Evidence), 5, '0')) INTO p_EvidenceID;
    SET p_EvidenceNumber = CONCAT('EVN-', v_Year, '-', LPAD(v_SeqNum, 3, '0'));
    SET p_BarcodeNumber  = CONCAT('FMD', v_Year, LPAD(FLOOR(RAND()*999999), 6, '0'));

    INSERT INTO Evidence (
        EvidenceID, CaseID, EvidenceNumber, EvidenceType, EvidenceDescription,
        CollectionDate, CollectedBy, StorageLocation, StorageConditions, BarcodeNumber
    ) VALUES (
        p_EvidenceID, p_CaseID, p_EvidenceNumber, p_EvidenceType, p_EvidenceDescription,
        p_CollectionDate, p_CollectedBy, p_StorageLocation, p_StorageConditions, p_BarcodeNumber
    );

    SET p_StatusCode = 1;
    SET p_Message    = CONCAT('Evidence added: ', p_EvidenceNumber, ' | Barcode: ', p_BarcodeNumber);
END$$


-- =============================================================================
-- SP 7: sp_AddChainOfCustody
-- Appends a chain-of-custody entry for an evidence item
-- =============================================================================
CREATE PROCEDURE sp_AddChainOfCustody(
    IN  p_EvidenceID     VARCHAR(20),
    IN  p_HandledBy      VARCHAR(100),
    IN  p_Purpose        VARCHAR(200),
    OUT p_StatusCode     INT,
    OUT p_Message        VARCHAR(200)
)
BEGIN
    DECLARE v_Exists INT DEFAULT 0;
    DECLARE v_Entry  TEXT;

    SELECT COUNT(*) INTO v_Exists FROM Evidence WHERE EvidenceID = p_EvidenceID;

    IF v_Exists = 0 THEN
        SET p_StatusCode = -1;
        SET p_Message    = 'Evidence not found.';
    ELSE
        SET v_Entry = CONCAT('[', NOW(), '] Handled by: ', p_HandledBy, ' | Purpose: ', p_Purpose);

        UPDATE Evidence
        SET ChainOfCustody  = CONCAT(IFNULL(ChainOfCustody, ''), '\n', v_Entry),
            LastHandledBy   = p_HandledBy,
            LastHandledDate = NOW()
        WHERE EvidenceID = p_EvidenceID;

        SET p_StatusCode = 1;
        SET p_Message    = 'Chain of custody updated.';
    END IF;
END$$


-- =============================================================================
-- SP 8: sp_SubmitCourtReport
-- Marks a court report as submitted and records the date
-- =============================================================================
CREATE PROCEDURE sp_SubmitCourtReport(
    IN  p_ReportID       VARCHAR(20),
    IN  p_SubmittedBy    VARCHAR(100),
    IN  p_CourtName      VARCHAR(300),
    IN  p_CourtCaseNo    VARCHAR(50),
    OUT p_StatusCode     INT,
    OUT p_Message        VARCHAR(200)
)
BEGIN
    DECLARE v_Status VARCHAR(20);

    SELECT ReportStatus INTO v_Status FROM CourtReport WHERE ReportID = p_ReportID;

    IF v_Status IS NULL THEN
        SET p_StatusCode = -1;
        SET p_Message    = 'Report not found.';
    ELSEIF v_Status NOT IN ('Generated','Reviewed') THEN
        SET p_StatusCode = -2;
        SET p_Message    = CONCAT('Cannot submit report in status: ', v_Status);
    ELSE
        UPDATE CourtReport
        SET ReportStatus   = 'Submitted',
            SubmittedAt    = NOW(),
            ApprovedBy     = p_SubmittedBy,
            CourtName      = IFNULL(p_CourtName, CourtName),
            CourtCaseNumber= IFNULL(p_CourtCaseNo, CourtCaseNumber)
        WHERE ReportID = p_ReportID;

        SET p_StatusCode = 1;
        SET p_Message    = CONCAT('Report ', p_ReportID, ' submitted successfully at ', NOW());
    END IF;
END$$


-- =============================================================================
-- SP 9: sp_LockUserAccount
-- Locks a user account after too many failed login attempts
-- =============================================================================
CREATE PROCEDURE sp_LockUserAccount(
    IN  p_Username   VARCHAR(50),
    OUT p_StatusCode INT,
    OUT p_Message    VARCHAR(200)
)
BEGIN
    DECLARE v_Exists INT DEFAULT 0;

    SELECT COUNT(*) INTO v_Exists FROM SystemUser WHERE Username = p_Username;

    IF v_Exists = 0 THEN
        SET p_StatusCode = -1;
        SET p_Message    = 'User not found.';
    ELSE
        UPDATE SystemUser
        SET IsLocked = TRUE, LoginAttempts = LoginAttempts + 1
        WHERE Username = p_Username;

        SET p_StatusCode = 1;
        SET p_Message    = CONCAT('User account locked: ', p_Username);
    END IF;
END$$


-- =============================================================================
-- SP 10: sp_UnlockUserAccount
-- Unlocks a user account and resets login attempts
-- =============================================================================
CREATE PROCEDURE sp_UnlockUserAccount(
    IN  p_Username   VARCHAR(50),
    OUT p_StatusCode INT,
    OUT p_Message    VARCHAR(200)
)
BEGIN
    UPDATE SystemUser
    SET IsLocked = FALSE, LoginAttempts = 0
    WHERE Username = p_Username;

    IF ROW_COUNT() = 0 THEN
        SET p_StatusCode = -1;
        SET p_Message    = 'User not found.';
    ELSE
        SET p_StatusCode = 1;
        SET p_Message    = CONCAT('User unlocked: ', p_Username);
    END IF;
END$$


-- =============================================================================
-- SP 11: sp_GetPatientHistory
-- Returns all cases and reports for a given patient
-- =============================================================================
CREATE PROCEDURE sp_GetPatientHistory(
    IN p_PatientID VARCHAR(15)
)
BEGIN
    -- Basic patient info
    SELECT PatientID, FullName, NICPassport, DateOfBirth, Age, Gender, District
    FROM Patient
    WHERE PatientID = p_PatientID;

    -- All cases
    SELECT fc.CaseID, fc.CaseNumber, fc.CaseType, fc.CaseStatus,
           fc.IncidentDate, fc.IncidentLocation, d.FullName AS DoctorName, fc.CreatedAt
    FROM ForensicCase fc
    JOIN Doctor d ON fc.DoctorID = d.DoctorID
    WHERE fc.PatientID = p_PatientID
    ORDER BY fc.IncidentDate DESC;

    -- All court reports
    SELECT cr.ReportID, cr.ReportType, cr.ReportStatus, cr.GeneratedAt,
           cr.SubmittedAt, cr.CourtName, fc.CaseNumber
    FROM CourtReport cr
    JOIN ForensicCase fc ON cr.CaseID = fc.CaseID
    WHERE fc.PatientID = p_PatientID
    ORDER BY cr.GeneratedAt DESC;
END$$


-- =============================================================================
-- SP 12: sp_SearchCases
-- Searches cases by keyword across patient name, case number, location
-- =============================================================================
CREATE PROCEDURE sp_SearchCases(
    IN p_Keyword   VARCHAR(100),
    IN p_CaseType  VARCHAR(30),
    IN p_Status    VARCHAR(20),
    IN p_FromDate  DATE,
    IN p_ToDate    DATE
)
BEGIN
    SELECT
        fc.CaseID,
        fc.CaseNumber,
        fc.CaseType,
        fc.CaseStatus,
        fc.Priority,
        fc.IncidentDate,
        fc.IncidentLocation,
        p.FullName    AS PatientName,
        p.NICPassport,
        d.FullName    AS DoctorName
    FROM ForensicCase fc
    JOIN Patient p ON fc.PatientID = p.PatientID
    JOIN Doctor  d ON fc.DoctorID  = d.DoctorID
    WHERE
        (p_Keyword  IS NULL OR (
            p.FullName         LIKE CONCAT('%', p_Keyword, '%') OR
            fc.CaseNumber      LIKE CONCAT('%', p_Keyword, '%') OR
            fc.IncidentLocation LIKE CONCAT('%', p_Keyword, '%') OR
            p.NICPassport      LIKE CONCAT('%', p_Keyword, '%')
        ))
        AND (p_CaseType IS NULL OR fc.CaseType   = p_CaseType)
        AND (p_Status   IS NULL OR fc.CaseStatus = p_Status)
        AND (p_FromDate IS NULL OR DATE(fc.IncidentDate) >= p_FromDate)
        AND (p_ToDate   IS NULL OR DATE(fc.IncidentDate) <= p_ToDate)
    ORDER BY fc.IncidentDate DESC
    LIMIT 100;
END$$


-- =============================================================================
-- SP 13: sp_CloseCase
-- Validates all requirements and closes a case
-- =============================================================================
CREATE PROCEDURE sp_CloseCase(
    IN  p_CaseID     VARCHAR(20),
    IN  p_ClosedBy   VARCHAR(50),
    OUT p_StatusCode INT,
    OUT p_Message    VARCHAR(200)
)
BEGIN
    DECLARE v_Status       VARCHAR(20);
    DECLARE v_PendingEvid  INT DEFAULT 0;
    DECLARE v_PendingLab   INT DEFAULT 0;

    SELECT CaseStatus INTO v_Status FROM ForensicCase WHERE CaseID = p_CaseID;

    IF v_Status IS NULL THEN
        SET p_StatusCode = -1; SET p_Message = 'Case not found.';

    ELSEIF v_Status NOT IN ('Completed', 'Submitted') THEN
        SET p_StatusCode = -2; SET p_Message = CONCAT('Case must be Completed or Submitted to close. Current: ', v_Status);

    ELSE
        -- Check pending evidence
        SELECT COUNT(*) INTO v_PendingEvid
        FROM Evidence WHERE CaseID = p_CaseID AND AnalysisStatus IN ('Pending','InProgress');

        -- Check pending lab tests
        SELECT COUNT(*) INTO v_PendingLab
        FROM LaboratoryTest lt JOIN Evidence e ON lt.EvidenceID = e.EvidenceID
        WHERE e.CaseID = p_CaseID AND lt.TestStatus IN ('Pending','InProgress');

        IF v_PendingEvid > 0 THEN
            SET p_StatusCode = -3; SET p_Message = CONCAT(v_PendingEvid, ' evidence item(s) still pending analysis.');
        ELSEIF v_PendingLab > 0 THEN
            SET p_StatusCode = -4; SET p_Message = CONCAT(v_PendingLab, ' lab test(s) still pending completion.');
        ELSE
            UPDATE ForensicCase
            SET CaseStatus = 'Closed',
                CaseNotes  = CONCAT(IFNULL(CaseNotes,''), '\n[', NOW(), '] Case closed by ', p_ClosedBy)
            WHERE CaseID = p_CaseID;

            SET p_StatusCode = 1; SET p_Message = CONCAT('Case ', p_CaseID, ' closed successfully.');
        END IF;
    END IF;
END$$


-- =============================================================================
-- SP 14: sp_GenerateMonthlyReport
-- Returns case statistics for a given month/year
-- =============================================================================
CREATE PROCEDURE sp_GenerateMonthlyReport(
    IN p_Year  INT,
    IN p_Month INT
)
BEGIN
    -- Overall stats
    SELECT
        COUNT(*)  AS TotalCases,
        SUM(CASE WHEN CaseType   = 'Clinical Forensic'  THEN 1 ELSE 0 END) AS ClinicalCases,
        SUM(CASE WHEN CaseType   = 'Autopsy'             THEN 1 ELSE 0 END) AS AutopsyCases,
        SUM(CASE WHEN CaseType   = 'Clinical & Autopsy'  THEN 1 ELSE 0 END) AS CombinedCases,
        SUM(CASE WHEN CaseStatus = 'Completed'           THEN 1 ELSE 0 END) AS CompletedCases,
        SUM(CASE WHEN CaseStatus = 'Pending'             THEN 1 ELSE 0 END) AS PendingCases,
        SUM(CASE WHEN Priority   = 'Critical'            THEN 1 ELSE 0 END) AS CriticalCases
    FROM ForensicCase
    WHERE YEAR(IncidentDate) = p_Year AND MONTH(IncidentDate) = p_Month;

    -- Death type breakdown (autopsy cases)
    SELECT pm.DeathType, COUNT(*) AS Count
    FROM Postmortem pm
    JOIN ForensicCase fc ON pm.CaseID = fc.CaseID
    WHERE YEAR(fc.IncidentDate) = p_Year AND MONTH(fc.IncidentDate) = p_Month
    GROUP BY pm.DeathType ORDER BY Count DESC;

    -- District breakdown
    SELECT p.District, COUNT(*) AS CaseCount
    FROM ForensicCase fc JOIN Patient p ON fc.PatientID = p.PatientID
    WHERE YEAR(fc.IncidentDate) = p_Year AND MONTH(fc.IncidentDate) = p_Month
    GROUP BY p.District ORDER BY CaseCount DESC;

    -- Doctor workload for the month
    SELECT d.FullName AS Doctor, d.JMOType, COUNT(*) AS CasesHandled
    FROM ForensicCase fc JOIN Doctor d ON fc.DoctorID = d.DoctorID
    WHERE YEAR(fc.IncidentDate) = p_Year AND MONTH(fc.IncidentDate) = p_Month
    GROUP BY d.DoctorID, d.FullName, d.JMOType ORDER BY CasesHandled DESC;
END$$


-- =============================================================================
-- SP 15: sp_GetDoctorWorkload
-- Full workload report for a specific doctor
-- =============================================================================
CREATE PROCEDURE sp_GetDoctorWorkload(IN p_DoctorID VARCHAR(15))
BEGIN
    SELECT
        d.DoctorID, d.FullName, d.JMOType, d.Specialization,
        COUNT(fc.CaseID) AS TotalAllTime,
        SUM(CASE WHEN YEAR(fc.IncidentDate) = YEAR(CURDATE()) THEN 1 ELSE 0 END) AS ThisYear,
        SUM(CASE WHEN MONTH(fc.IncidentDate) = MONTH(CURDATE())
                  AND YEAR(fc.IncidentDate)  = YEAR(CURDATE())  THEN 1 ELSE 0 END) AS ThisMonth,
        SUM(CASE WHEN fc.CaseStatus IN ('Pending','InProgress') THEN 1 ELSE 0 END) AS ActiveCases,
        SUM(CASE WHEN fc.CaseType = 'Autopsy' THEN 1 ELSE 0 END) AS AutopsyTotal,
        SUM(CASE WHEN fc.CaseType = 'Clinical Forensic' THEN 1 ELSE 0 END) AS ClinicalTotal
    FROM Doctor d
    LEFT JOIN ForensicCase fc ON d.DoctorID = fc.DoctorID
    WHERE d.DoctorID = p_DoctorID
    GROUP BY d.DoctorID, d.FullName, d.JMOType, d.Specialization;
END$$


-- =============================================================================
-- SP 16: sp_ArchiveOldCases
-- Archives cases that have been Closed for more than 6 months
-- =============================================================================
CREATE PROCEDURE sp_ArchiveOldCases(
    OUT p_ArchivedCount INT,
    OUT p_Message       VARCHAR(200)
)
BEGIN
    UPDATE ForensicCase
    SET CaseStatus = 'Archived'
    WHERE CaseStatus = 'Closed'
      AND UpdatedAt <= DATE_SUB(NOW(), INTERVAL 6 MONTH);

    SET p_ArchivedCount = ROW_COUNT();
    SET p_Message       = CONCAT(p_ArchivedCount, ' case(s) archived.');
END$$


-- =============================================================================
-- SP 17: sp_LogActivity
-- Inserts an activity log entry
-- =============================================================================
CREATE PROCEDURE sp_LogActivity(
    IN p_UserID      VARCHAR(15),
    IN p_Username    VARCHAR(50),
    IN p_ActionType  VARCHAR(20),
    IN p_ModelName   VARCHAR(50),
    IN p_RecordID    VARCHAR(20),
    IN p_Details     TEXT,
    IN p_IPAddress   VARCHAR(45)
)
BEGIN
    INSERT INTO ActivityLog (UserID, Username, ActionType, ModelName, RecordID, ActionDetails, IPAddress)
    VALUES (p_UserID, p_Username, p_ActionType, p_ModelName, p_RecordID, p_Details, p_IPAddress);
END$$

DELIMITER ;

-- =============================================================================
-- List all stored procedures
-- =============================================================================
SELECT ROUTINE_NAME AS ProcedureName, ROUTINE_TYPE AS Type
FROM INFORMATION_SCHEMA.ROUTINES
WHERE ROUTINE_SCHEMA = 'forensic_medicine_db'
ORDER BY ROUTINE_NAME;

-- End of 03_stored_procedures.sql
