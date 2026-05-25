-- =============================================================================
-- FORENSIC MEDICINE DEPARTMENT DATABASE SYSTEM
-- File        : 01_schema.sql
-- Description : Complete database schema - all tables, constraints, indexes
-- Database    : MySQL 8.0
-- Encoding    : utf8mb4 / utf8mb4_unicode_ci
-- =============================================================================

-- Create and select database
CREATE DATABASE IF NOT EXISTS forensic_medicine_db
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE forensic_medicine_db;

-- Enforce strict SQL mode for this session
SET SESSION sql_mode = 'STRICT_TRANS_TABLES,NO_ZERO_DATE,NO_ZERO_IN_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- Disable FK checks during creation (re-enable at end)
SET FOREIGN_KEY_CHECKS = 0;

-- =============================================================================
-- TABLE: Staff
-- Base table for all department personnel
-- =============================================================================
CREATE TABLE IF NOT EXISTS Staff (
    StaffID         VARCHAR(15)  NOT NULL,
    FullName        VARCHAR(100) NOT NULL,
    StaffType       ENUM('Doctor','Laboratory','Administrative','Clerical') NOT NULL,
    Department      VARCHAR(100) NOT NULL DEFAULT 'Forensic Medicine',
    Designation     VARCHAR(100),
    ContactNo       VARCHAR(15),
    Email           VARCHAR(100),
    JoinDate        DATE,
    IsActive        BOOLEAN      NOT NULL DEFAULT TRUE,
    CreatedAt       TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UpdatedAt       TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    CONSTRAINT pk_Staff            PRIMARY KEY (StaffID),
    CONSTRAINT uq_Staff_Email      UNIQUE (Email),
    CONSTRAINT chk_Staff_Email     CHECK (Email IS NULL OR Email LIKE '%@%.%'),
    CONSTRAINT chk_Staff_Contact   CHECK (ContactNo IS NULL OR LENGTH(ContactNo) >= 7),

    INDEX idx_Staff_Type   (StaffType),
    INDEX idx_Staff_Active (IsActive)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
  COMMENT='Base personnel table for all department staff';


-- =============================================================================
-- TABLE: Doctor
-- Doctors and JMOs performing examinations
-- =============================================================================
CREATE TABLE IF NOT EXISTS Doctor (
    DoctorID        VARCHAR(15)  NOT NULL,
    StaffID         VARCHAR(15),
    FullName        VARCHAR(100) NOT NULL,
    NMCNumber       VARCHAR(20)  NOT NULL,
    Qualification   VARCHAR(100),
    Specialization  VARCHAR(100),
    JMOType         ENUM('Consultant JMO','Senior JMO','Junior JMO') NOT NULL,
    LicenseNumber   VARCHAR(50),
    Department      VARCHAR(100) NOT NULL DEFAULT 'Forensic Medicine',
    OfficeContactNo VARCHAR(15),
    SignaturePath   VARCHAR(500),
    IsActive        BOOLEAN      NOT NULL DEFAULT TRUE,
    CreatedAt       TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UpdatedAt       TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    CONSTRAINT pk_Doctor            PRIMARY KEY (DoctorID),
    CONSTRAINT uq_Doctor_NMC       UNIQUE (NMCNumber),
    CONSTRAINT uq_Doctor_License   UNIQUE (LicenseNumber),
    CONSTRAINT fk_Doctor_Staff     FOREIGN KEY (StaffID) REFERENCES Staff(StaffID) ON UPDATE CASCADE ON DELETE SET NULL,
    CONSTRAINT chk_Doctor_NMC      CHECK (LENGTH(NMCNumber) >= 4),

    INDEX idx_Doctor_Active  (IsActive),
    INDEX idx_Doctor_JMOType (JMOType)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
  COMMENT='Doctors and JMOs who conduct examinations and autopsies';


-- =============================================================================
-- TABLE: Patient
-- All individuals examined by the department
-- =============================================================================
CREATE TABLE IF NOT EXISTS Patient (
    PatientID           VARCHAR(15)  NOT NULL,
    FullName            VARCHAR(100) NOT NULL,
    NICPassport         VARCHAR(20)  NOT NULL,
    DateOfBirth         DATE,
    Age                 TINYINT UNSIGNED,
    Gender              ENUM('Male','Female','Other','Unknown') NOT NULL,
    Address             VARCHAR(300),
    District            VARCHAR(50),
    ContactNo           VARCHAR(15),
    EmergencyContactName VARCHAR(100),
    EmergencyContactNo  VARCHAR(15),
    PhotographPath      VARCHAR(500),
    CivilStatus         ENUM('Single','Married','Divorced','Widowed','Unknown'),
    Occupation          VARCHAR(100),
    Notes               LONGTEXT,
    RegisteredAt        TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UpdatedAt           TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    CONSTRAINT pk_Patient           PRIMARY KEY (PatientID),
    CONSTRAINT uq_Patient_NIC       UNIQUE (NICPassport),
    CONSTRAINT chk_Patient_DOB      CHECK (DateOfBirth IS NULL OR DateOfBirth < CURDATE()),
    CONSTRAINT chk_Patient_Age      CHECK (Age IS NULL OR Age BETWEEN 0 AND 150),

    INDEX idx_Patient_Name       (FullName),
    INDEX idx_Patient_DOB        (DateOfBirth),
    INDEX idx_Patient_District   (District),
    FULLTEXT INDEX ft_Patient_Name (FullName)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
  COMMENT='All individuals examined by the forensic medicine department';


-- =============================================================================
-- TABLE: ForensicCase
-- Central case record linking patient, doctor, and case details
-- (Named ForensicCase to avoid reserved word conflict with MySQL 'CASE')
-- =============================================================================
CREATE TABLE IF NOT EXISTS ForensicCase (
    CaseID          VARCHAR(20)  NOT NULL,
    CaseNumber      VARCHAR(30)  NOT NULL,
    PatientID       VARCHAR(15)  NOT NULL,
    DoctorID        VARCHAR(15)  NOT NULL,
    CaseType        ENUM('Clinical Forensic','Autopsy','Clinical & Autopsy') NOT NULL,
    IncidentDate    DATETIME     NOT NULL,
    IncidentLocation VARCHAR(300),
    IncidentType    VARCHAR(100),
    PoliceReportNo  VARCHAR(50),
    CourtCaseNo     VARCHAR(50),
    CaseStatus      ENUM('Pending','InProgress','Completed','Submitted','Closed','Archived') NOT NULL DEFAULT 'Pending',
    Priority        ENUM('Low','Medium','High','Critical')                                   NOT NULL DEFAULT 'Medium',
    CaseNotes       LONGTEXT,
    CreatedAt       TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UpdatedAt       TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    CONSTRAINT pk_ForensicCase          PRIMARY KEY (CaseID),
    CONSTRAINT uq_ForensicCase_Number   UNIQUE (CaseNumber),
    CONSTRAINT fk_ForensicCase_Patient  FOREIGN KEY (PatientID) REFERENCES Patient(PatientID)  ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_ForensicCase_Doctor   FOREIGN KEY (DoctorID)  REFERENCES Doctor(DoctorID)    ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT chk_ForensicCase_Date    CHECK (IncidentDate <= CURRENT_TIMESTAMP),

    INDEX idx_FC_PatientID   (PatientID),
    INDEX idx_FC_DoctorID    (DoctorID),
    INDEX idx_FC_Status      (CaseStatus),
    INDEX idx_FC_Type        (CaseType),
    INDEX idx_FC_Incident    (IncidentDate),
    INDEX idx_FC_Priority    (Priority),
    FULLTEXT INDEX ft_FC_Notes (CaseNotes)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
  COMMENT='Central forensic case record — links patient, doctor and case metadata';


-- =============================================================================
-- TABLE: ClinicalExamination
-- Records of clinical forensic examinations (MLEF)
-- =============================================================================
CREATE TABLE IF NOT EXISTS ClinicalExamination (
    ExaminationID       VARCHAR(20)  NOT NULL,
    CaseID              VARCHAR(20)  NOT NULL,
    DoctorID            VARCHAR(15)  NOT NULL,
    ExaminationDate     DATETIME     NOT NULL,
    ExaminationType     VARCHAR(100),
    TimeOfExamination   TIME,
    GeneralCondition    VARCHAR(200),
    Consciousness       ENUM('Alert','Confused','Drowsy','Unconscious','Unknown'),
    NutritionalStatus   VARCHAR(100),
    PhotographsTaken    SMALLINT UNSIGNED NOT NULL DEFAULT 0,
    PhotographPath      VARCHAR(500),
    InjuryDetails       LONGTEXT,
    WoundDescription    LONGTEXT,
    ExaminationFindings LONGTEXT,
    CausativeWeapon     VARCHAR(100),
    InvestigationRequired BOOLEAN NOT NULL DEFAULT FALSE,
    InvestigationType   VARCHAR(200),
    ReferralRequired    BOOLEAN NOT NULL DEFAULT FALSE,
    ReferralDepartment  VARCHAR(100),
    ReferralReason      VARCHAR(300),
    OfficerNotes        LONGTEXT,
    CreatedAt           TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UpdatedAt           TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    CONSTRAINT pk_ClinicalExam         PRIMARY KEY (ExaminationID),
    CONSTRAINT fk_ClinicalExam_Case    FOREIGN KEY (CaseID)    REFERENCES ForensicCase(CaseID)  ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_ClinicalExam_Doctor  FOREIGN KEY (DoctorID)  REFERENCES Doctor(DoctorID)      ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT chk_ClinicalExam_Photos CHECK (PhotographsTaken >= 0),

    INDEX idx_CE_CaseID  (CaseID),
    INDEX idx_CE_DoctorID (DoctorID),
    INDEX idx_CE_Date    (ExaminationDate)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
  COMMENT='Clinical forensic examination records (MLEF form data)';


-- =============================================================================
-- TABLE: Postmortem
-- Autopsy / postmortem examination records
-- =============================================================================
CREATE TABLE IF NOT EXISTS Postmortem (
    PostmortemID            VARCHAR(20)  NOT NULL,
    CaseID                  VARCHAR(20)  NOT NULL,
    DoctorID                VARCHAR(15)  NOT NULL,
    InquestOrderDate        DATE,
    CourtOrderDate          DATE,
    AutopsyDate             DATETIME     NOT NULL,
    AutopsyStartTime        TIME,
    AutopsyEndTime          TIME,
    AutopsyLocation         VARCHAR(300),
    InquestNumber           VARCHAR(50),
    CourtOrderNumber        VARCHAR(50),
    ExternalFindings        LONGTEXT,
    InternalFindings        LONGTEXT,
    OrganFindings           LONGTEXT,
    ImmediateCauseOfDeath   VARCHAR(300),
    CauseOfDeathA           VARCHAR(300),
    CauseOfDeathB           VARCHAR(300),
    CauseOfDeathC           VARCHAR(300),
    DeathType               ENUM('Natural','Accidental','Suicidal','Homicidal','Undetermined') NOT NULL,
    EstimatedTimeOfDeath    DATETIME,
    AudioRecordingPath      VARCHAR(500),
    AudioDurationSecs       INT UNSIGNED,
    PhotographsTaken        SMALLINT UNSIGNED NOT NULL DEFAULT 0,
    PhotographPath          VARCHAR(500),
    SpecimenCollected       BOOLEAN      NOT NULL DEFAULT FALSE,
    SpecimenDetails         LONGTEXT,
    AssistantNames          VARCHAR(500),
    ReportStatus            ENUM('Pending','InProgress','Completed','Reviewed') NOT NULL DEFAULT 'Pending',
    CreatedAt               TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UpdatedAt               TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    CONSTRAINT pk_Postmortem           PRIMARY KEY (PostmortemID),
    CONSTRAINT uq_Postmortem_Case      UNIQUE (CaseID),
    CONSTRAINT fk_Postmortem_Case      FOREIGN KEY (CaseID)   REFERENCES ForensicCase(CaseID)  ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_Postmortem_Doctor    FOREIGN KEY (DoctorID) REFERENCES Doctor(DoctorID)      ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT chk_PM_AutopsyDate      CHECK (AutopsyDate >= '2000-01-01'),

    INDEX idx_PM_CaseID     (CaseID),
    INDEX idx_PM_DoctorID   (DoctorID),
    INDEX idx_PM_AutopsyDate (AutopsyDate),
    INDEX idx_PM_DeathType   (DeathType),
    INDEX idx_PM_Status      (ReportStatus)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
  COMMENT='Autopsy and postmortem examination records';


-- =============================================================================
-- TABLE: Evidence
-- Forensic evidence items collected and tracked
-- =============================================================================
CREATE TABLE IF NOT EXISTS Evidence (
    EvidenceID          VARCHAR(20)  NOT NULL,
    CaseID              VARCHAR(20)  NOT NULL,
    EvidenceNumber      VARCHAR(50)  NOT NULL,
    EvidenceType        VARCHAR(100) NOT NULL,
    EvidenceDescription LONGTEXT,
    CollectionDate      DATETIME     NOT NULL,
    CollectedBy         VARCHAR(100),
    StorageLocation     VARCHAR(300),
    StorageTemperature  VARCHAR(50),
    StorageConditions   VARCHAR(300),
    BarcodeNumber       VARCHAR(100),
    QRCodeData          VARCHAR(500),
    ChainOfCustody      LONGTEXT,
    LastHandledBy       VARCHAR(100),
    LastHandledDate     DATETIME,
    AnalysisStatus      ENUM('Pending','InProgress','Completed','Failed','Disputed') NOT NULL DEFAULT 'Pending',
    AnalysisType        VARCHAR(200),
    AnalysisResult      LONGTEXT,
    DisposalStatus      ENUM('Stored','ReturnedToPolice','Destroyed','Unknown')      NOT NULL DEFAULT 'Stored',
    DisposalDate        DATETIME,
    DisposalApprovedBy  VARCHAR(100),
    Remarks             LONGTEXT,
    CreatedAt           TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UpdatedAt           TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    CONSTRAINT pk_Evidence              PRIMARY KEY (EvidenceID),
    CONSTRAINT uq_Evidence_Number       UNIQUE (EvidenceNumber),
    CONSTRAINT uq_Evidence_Barcode      UNIQUE (BarcodeNumber),
    CONSTRAINT fk_Evidence_Case         FOREIGN KEY (CaseID) REFERENCES ForensicCase(CaseID) ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT chk_Evidence_Collection  CHECK (CollectionDate <= CURRENT_TIMESTAMP),

    INDEX idx_Ev_CaseID        (CaseID),
    INDEX idx_Ev_Type          (EvidenceType),
    INDEX idx_Ev_AnalysisStatus (AnalysisStatus),
    INDEX idx_Ev_DisposalStatus (DisposalStatus)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
  COMMENT='Forensic evidence items — collection, storage, chain of custody';


-- =============================================================================
-- TABLE: LaboratoryTest
-- Lab tests performed on evidence samples
-- =============================================================================
CREATE TABLE IF NOT EXISTS LaboratoryTest (
    TestID              VARCHAR(20)  NOT NULL,
    EvidenceID          VARCHAR(20)  NOT NULL,
    TechnicianID        VARCHAR(15),
    TestType            VARCHAR(100) NOT NULL,
    TestDescription     VARCHAR(300),
    RequestedDate       DATETIME,
    RequestedBy         VARCHAR(100),
    TestDate            DATETIME     NOT NULL,
    CompletionDate      DATETIME,
    TestResult          LONGTEXT,
    ResultInterpretation LONGTEXT,
    TestStatus          ENUM('Pending','InProgress','Completed','Failed','OnHold') NOT NULL DEFAULT 'Pending',
    ReferenceNumber     VARCHAR(50),
    TestNotes           LONGTEXT,
    CertificateIssued   BOOLEAN      NOT NULL DEFAULT FALSE,
    CertificatePath     VARCHAR(500),
    ReportPath          VARCHAR(500),
    CreatedAt           TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UpdatedAt           TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    CONSTRAINT pk_LabTest          PRIMARY KEY (TestID),
    CONSTRAINT fk_LabTest_Evidence FOREIGN KEY (EvidenceID)   REFERENCES Evidence(EvidenceID) ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_LabTest_Tech     FOREIGN KEY (TechnicianID) REFERENCES Staff(StaffID)       ON UPDATE CASCADE ON DELETE SET NULL,
    CONSTRAINT chk_LabTest_Dates   CHECK (CompletionDate IS NULL OR CompletionDate >= TestDate),

    INDEX idx_LT_EvidenceID (EvidenceID),
    INDEX idx_LT_TechID     (TechnicianID),
    INDEX idx_LT_TestDate   (TestDate),
    INDEX idx_LT_Status     (TestStatus)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
  COMMENT='Laboratory tests performed on forensic evidence samples';


-- =============================================================================
-- TABLE: CourtReport
-- MLR and PMR reports for court submission
-- =============================================================================
CREATE TABLE IF NOT EXISTS CourtReport (
    ReportID                VARCHAR(20)  NOT NULL,
    CaseID                  VARCHAR(20)  NOT NULL,
    DoctorID                VARCHAR(15)  NOT NULL,
    ReportType              ENUM('MLR','PMR','Combined') NOT NULL,
    ReportTitle             VARCHAR(300),
    ReportContent           LONGTEXT,
    ReportConclusions       LONGTEXT,
    RecommendedInvestigations LONGTEXT,
    CourtName               VARCHAR(300),
    CourtCaseNumber         VARCHAR(50),
    MagistrateDistrict      VARCHAR(100),
    JudgeName               VARCHAR(100),
    LawyerDetails           VARCHAR(300),
    ReportStatus            ENUM('Draft','Generated','Reviewed','Submitted','Received','Archived') NOT NULL DEFAULT 'Draft',
    GeneratedAt             DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    SubmittedAt             DATETIME,
    ReceivedAt              DATETIME,
    SubmissionProofPath     VARCHAR(500),
    DigitalSignaturePath    VARCHAR(500),
    ApprovedBy              VARCHAR(100),
    ApprovedAt              DATETIME,
    Remarks                 LONGTEXT,
    CreatedAt               TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UpdatedAt               TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    CONSTRAINT pk_CourtReport          PRIMARY KEY (ReportID),
    CONSTRAINT fk_CourtReport_Case     FOREIGN KEY (CaseID)   REFERENCES ForensicCase(CaseID) ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_CourtReport_Doctor   FOREIGN KEY (DoctorID) REFERENCES Doctor(DoctorID)     ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT chk_CR_SubmitDate       CHECK (SubmittedAt IS NULL OR SubmittedAt >= GeneratedAt),

    INDEX idx_CR_CaseID    (CaseID),
    INDEX idx_CR_DoctorID  (DoctorID),
    INDEX idx_CR_Status    (ReportStatus),
    INDEX idx_CR_Type      (ReportType),
    INDEX idx_CR_Submitted (SubmittedAt)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
  COMMENT='Medico-legal and postmortem reports for court submission';


-- =============================================================================
-- TABLE: SystemUser
-- Login accounts for all system users
-- (Named SystemUser to avoid MySQL reserved word 'USER')
-- =============================================================================
CREATE TABLE IF NOT EXISTS SystemUser (
    UserID              VARCHAR(15)  NOT NULL,
    StaffID             VARCHAR(15)  NOT NULL,
    Username            VARCHAR(50)  NOT NULL,
    PasswordHash        VARCHAR(255) NOT NULL,
    Role                ENUM('Doctor','LabTechnician','Administrator','Viewer') NOT NULL,
    LastLoginAt         DATETIME,
    LastLoginIP         VARCHAR(45),
    LoginAttempts       TINYINT UNSIGNED NOT NULL DEFAULT 0,
    IsLocked            BOOLEAN      NOT NULL DEFAULT FALSE,
    IsActive            BOOLEAN      NOT NULL DEFAULT TRUE,
    PasswordExpiry      DATE,
    MustChangePassword  BOOLEAN      NOT NULL DEFAULT FALSE,
    CreatedAt           TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UpdatedAt           TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CreatedBy           VARCHAR(15),

    CONSTRAINT pk_SystemUser         PRIMARY KEY (UserID),
    CONSTRAINT uq_SystemUser_Staff   UNIQUE (StaffID),
    CONSTRAINT uq_SystemUser_Name    UNIQUE (Username),
    CONSTRAINT fk_SystemUser_Staff   FOREIGN KEY (StaffID) REFERENCES Staff(StaffID) ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT chk_SU_Username       CHECK (LENGTH(Username) >= 4),
    CONSTRAINT chk_SU_Attempts       CHECK (LoginAttempts >= 0 AND LoginAttempts <= 10),

    INDEX idx_SU_Username (Username),
    INDEX idx_SU_Role     (Role),
    INDEX idx_SU_Active   (IsActive)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
  COMMENT='System login accounts with RBAC roles';


-- =============================================================================
-- TABLE: ActivityLog
-- Comprehensive audit trail for all system actions
-- =============================================================================
CREATE TABLE IF NOT EXISTS ActivityLog (
    LogID           BIGINT       NOT NULL AUTO_INCREMENT,
    UserID          VARCHAR(15)  NOT NULL,
    Username        VARCHAR(50)  NOT NULL,
    ActionType      ENUM('LOGIN','LOGOUT','CREATE','UPDATE','DELETE','VIEW','EXPORT','SUBMIT','LOCK','UNLOCK') NOT NULL,
    ModelName       VARCHAR(50),
    RecordID        VARCHAR(20),
    ActionDetails   TEXT,
    IPAddress       VARCHAR(45),
    UserAgent       VARCHAR(500),
    LoggedAt        TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT pk_ActivityLog        PRIMARY KEY (LogID),
    CONSTRAINT fk_ActivityLog_User   FOREIGN KEY (UserID) REFERENCES SystemUser(UserID) ON UPDATE CASCADE ON DELETE RESTRICT,

    INDEX idx_AL_UserID     (UserID),
    INDEX idx_AL_ActionType (ActionType),
    INDEX idx_AL_ModelName  (ModelName),
    INDEX idx_AL_LoggedAt   (LoggedAt)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
  COMMENT='Full audit trail of all system user actions';


-- Re-enable FK checks
SET FOREIGN_KEY_CHECKS = 1;

-- =============================================================================
-- Confirmation
-- =============================================================================
SELECT
    TABLE_NAME            AS `Table`,
    TABLE_ROWS            AS `Est. Rows`,
    TABLE_COMMENT         AS `Description`
FROM
    INFORMATION_SCHEMA.TABLES
WHERE
    TABLE_SCHEMA = 'forensic_medicine_db'
ORDER BY
    TABLE_NAME;

-- End of 01_schema.sql
