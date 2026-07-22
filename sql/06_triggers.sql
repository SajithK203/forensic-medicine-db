-- =============================================================================
-- FORENSIC MEDICINE DEPARTMENT DATABASE SYSTEM
-- File        : 06_triggers.sql
-- Group       : 22
-- Members     : R.M.S.S.Kumara (E/22/203), A.W.H.Panchani (E/22/269),
--               K.D.Ashen (E/22/032), W.A.N.Gunathilaka (E/22/121)
-- Description : 8 Triggers for business rule enforcement and audit logging
-- Database    : MySQL 8.0 (forensic_medicine_db)
-- Run after   : 01_schema.sql, 02_views.sql, 03_stored_procedures.sql
-- =============================================================================

USE forensic_medicine_db;

DELIMITER $$

-- =============================================================================
-- TRIGGER 1: trg_AccountLockout
-- Purpose    : Automatically lock a user account after 5 consecutive
--              failed login attempts to prevent brute-force attacks.
-- Table      : accounts_customuser
-- Event      : AFTER UPDATE
-- =============================================================================
CREATE TRIGGER trg_AccountLockout
AFTER UPDATE ON accounts_customuser
FOR EACH ROW
BEGIN
    -- If login_attempts reaches 5 or more and account is not yet locked
    IF NEW.login_attempts >= 5 AND OLD.is_locked = FALSE THEN
        UPDATE accounts_customuser
        SET    is_locked = TRUE
        WHERE  id = NEW.id;
    END IF;
END$$


-- =============================================================================
-- TRIGGER 2: trg_CaseStatusChangeLog
-- Purpose    : Automatically write to the activity log whenever a forensic
--              case status is changed. Ensures full audit trail of case
--              lifecycle transitions for legal accountability.
-- Table      : cases_forensiccase
-- Event      : AFTER UPDATE
-- =============================================================================
CREATE TRIGGER trg_CaseStatusChangeLog
AFTER UPDATE ON cases_forensiccase
FOR EACH ROW
BEGIN
    -- Only fire when the case_status column actually changes
    IF OLD.case_status <> NEW.case_status THEN
        INSERT INTO core_activitylog (
            username,
            action_type,
            model_name,
            record_id,
            action_details,
            ip_address,
            logged_at
        )
        VALUES (
            'SYSTEM_TRIGGER',
            'UPDATE',
            'ForensicCase',
            NEW.case_id,
            CONCAT(
                'Case ', NEW.case_number,
                ' status changed from [', OLD.case_status,
                '] to [', NEW.case_status, ']'
            ),
            '127.0.0.1',
            NOW()
        );
    END IF;
END$$


-- =============================================================================
-- TRIGGER 3: trg_PreventCompletedEvidenceDeletion
-- Purpose    : Block deletion of any evidence item whose laboratory analysis
--              is already completed. Completed evidence may be referenced in
--              court reports and must be preserved for legal integrity.
-- Table      : evidence_evidence
-- Event      : BEFORE DELETE
-- =============================================================================
CREATE TRIGGER trg_PreventCompletedEvidenceDeletion
BEFORE DELETE ON evidence_evidence
FOR EACH ROW
BEGIN
    IF OLD.analysis_status = 'Completed' THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'DELETION BLOCKED: Evidence item with completed laboratory analysis cannot be deleted. It may be referenced in court reports.';
    END IF;
END$$


-- =============================================================================
-- TRIGGER 4: trg_LabTestCompleteUpdateEvidence
-- Purpose    : When a laboratory test status is updated to "Completed",
--              automatically update the parent evidence item's analysis_status
--              to "Completed" as well. Maintains data consistency.
-- Table      : evidence_laboratorytest
-- Event      : AFTER UPDATE
-- =============================================================================
CREATE TRIGGER trg_LabTestCompleteUpdateEvidence
AFTER UPDATE ON evidence_laboratorytest
FOR EACH ROW
BEGIN
    IF OLD.test_status <> 'Completed' AND NEW.test_status = 'Completed' THEN
        UPDATE evidence_evidence
        SET    analysis_status   = 'Completed',
               last_handled_date = NOW()
        WHERE  evidence_id = NEW.evidence_id;
    END IF;
END$$


-- =============================================================================
-- TRIGGER 5: trg_PreventDuplicatePostmortem
-- Purpose    : A forensic case can only have ONE postmortem examination.
--              This trigger prevents a second postmortem record being
--              inserted for the same case, which would be a data integrity error.
-- Table      : postmortem_postmortem
-- Event      : BEFORE INSERT
-- =============================================================================
CREATE TRIGGER trg_PreventDuplicatePostmortem
BEFORE INSERT ON postmortem_postmortem
FOR EACH ROW
BEGIN
    DECLARE v_existing_count INT DEFAULT 0;

    SELECT COUNT(*) INTO v_existing_count
    FROM   postmortem_postmortem
    WHERE  case_id = NEW.case_id;

    IF v_existing_count > 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'INTEGRITY ERROR: A postmortem record already exists for this forensic case. Only one postmortem is permitted per case.';
    END IF;
END$$


-- =============================================================================
-- TRIGGER 6: trg_CourtReportSubmissionLog
-- Purpose    : Automatically log a record in the activity log when a court
--              report's status changes to "Submitted". This creates a
--              non-repudiable legal record of submission timestamp.
-- Table      : reports_courtreport
-- Event      : AFTER UPDATE
-- =============================================================================
CREATE TRIGGER trg_CourtReportSubmissionLog
AFTER UPDATE ON reports_courtreport
FOR EACH ROW
BEGIN
    IF OLD.report_status <> 'Submitted' AND NEW.report_status = 'Submitted' THEN
        INSERT INTO core_activitylog (
            username,
            action_type,
            model_name,
            record_id,
            action_details,
            ip_address,
            logged_at
        )
        VALUES (
            'SYSTEM_TRIGGER',
            'UPDATE',
            'CourtReport',
            NEW.report_id,
            CONCAT(
                'Court Report [', NEW.report_id,
                '] for case linked to doctor [', NEW.doctor_id,
                '] submitted to [', NEW.court_name, '] at ', NOW()
            ),
            '127.0.0.1',
            NOW()
        );
    END IF;
END$$


-- =============================================================================
-- TRIGGER 7: trg_NewCaseNotification
-- Purpose    : Automatically create a system notification for the assigned
--              doctor whenever a new forensic case is created and assigned
--              to them. Ensures the doctor is alerted immediately.
-- Table      : cases_forensiccase
-- Event      : AFTER INSERT
-- =============================================================================
CREATE TRIGGER trg_NewCaseNotification
AFTER INSERT ON cases_forensiccase
FOR EACH ROW
BEGIN
    DECLARE v_user_id BIGINT DEFAULT NULL;

    -- Try to find the system user linked to the doctor
    SELECT au.id INTO v_user_id
    FROM   accounts_customuser au
    WHERE  au.is_active = TRUE
    LIMIT  1;

    -- Insert notification if we found a valid recipient
    IF v_user_id IS NOT NULL THEN
        INSERT INTO core_notification (
            recipient_id,
            notification_type,
            title,
            message,
            related_model,
            related_id,
            is_read,
            created_at
        )
        VALUES (
            v_user_id,
            'CASE',
            CONCAT('New Case Assigned: ', NEW.case_number),
            CONCAT(
                'A new forensic case (', NEW.case_number,
                ') of type [', NEW.case_type,
                '] has been created and assigned. Priority: ', NEW.priority
            ),
            'ForensicCase',
            NEW.case_id,
            FALSE,
            NOW()
        );
    END IF;
END$$


-- =============================================================================
-- TRIGGER 8: trg_EvidenceChainOfCustodyValidation
-- Purpose    : Before any chain-of-custody record is inserted, validate that
--              the referenced evidence item actually exists and is not already
--              marked for disposal. Prevents logging custody for disposed items.
-- Table      : evidence_evidencechainofcustody
-- Event      : BEFORE INSERT
-- =============================================================================
CREATE TRIGGER trg_EvidenceChainOfCustodyValidation
BEFORE INSERT ON evidence_evidencechainofcustody
FOR EACH ROW
BEGIN
    DECLARE v_disposal_status VARCHAR(25) DEFAULT '';

    SELECT disposal_status INTO v_disposal_status
    FROM   evidence_evidence
    WHERE  evidence_id = NEW.evidence_id;

    IF v_disposal_status IN ('Disposed', 'Destroyed') THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'CHAIN OF CUSTODY ERROR: Cannot log custody action for evidence that has already been disposed or destroyed.';
    END IF;
END$$

DELIMITER ;

-- =============================================================================
-- Verify all triggers were created successfully
-- =============================================================================
SELECT
    TRIGGER_NAME        AS TriggerName,
    EVENT_MANIPULATION  AS Event,
    EVENT_OBJECT_TABLE  AS TableName,
    ACTION_TIMING       AS Timing
FROM INFORMATION_SCHEMA.TRIGGERS
WHERE TRIGGER_SCHEMA = 'forensic_medicine_db'
ORDER BY EVENT_OBJECT_TABLE, ACTION_TIMING;

-- End of 06_triggers.sql
