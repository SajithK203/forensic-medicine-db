-- ============================================================
-- Forensic Medicine Department — Sample Data
-- File: sql/04_sample_data.sql
-- Database: forensic_medicine_db
-- Description: Realistic Sri Lankan sample data for all tables
-- ============================================================

USE forensic_medicine_db;
SET FOREIGN_KEY_CHECKS = 0;

-- ── Staff ────────────────────────────────────────────────────
INSERT IGNORE INTO apps_staff_staff
  (staff_id, full_name, staff_type, department, designation, contact_no, email, join_date, is_active, created_at, updated_at)
VALUES
  ('STF-0001','Dr. Samantha Perera',      'Doctor',        'Forensic Medicine','Head of Forensic Medicine', '0112345001','dr.perera@fmd.lk','2018-01-15',1,NOW(),NOW()),
  ('STF-0002','Dr. Nimal Silva',          'Doctor',        'Forensic Medicine','Consultant JMO',            '0112345002','dr.silva@fmd.lk', '2015-06-01',1,NOW(),NOW()),
  ('STF-0003','Dr. Kumari Bandara',       'Doctor',        'Forensic Medicine','Senior JMO',                '0112345003','dr.kumari@fmd.lk','2020-03-10',1,NOW(),NOW()),
  ('STF-0004','Dr. Asanka Jayawardena',   'Doctor',        'Forensic Medicine','Consultant JMO',            '0112345004','dr.asanka@fmd.lk','2010-09-01',1,NOW(),NOW()),
  ('STF-0005','Dr. Dilani Wickramasinghe','Doctor',        'Forensic Medicine','Junior JMO',                '0112345005','dr.dilani@fmd.lk','2022-07-20',1,NOW(),NOW()),
  ('STF-0006','Nuwan Karunaratne',        'Laboratory',    'Forensic Lab',     'Chief Lab Technician',      '0112345006','nuwan@fmd.lk',   '2017-04-12',1,NOW(),NOW()),
  ('STF-0007','Chamari Herath',           'Laboratory',    'Forensic Lab',     'Lab Technician',            '0112345007','chamari@fmd.lk', '2019-11-05',1,NOW(),NOW()),
  ('STF-0008','Lakshmi Ranasinghe',       'Administrative','Administration',   'Administrative Officer',    '0112345008','lakshmi@fmd.lk', '2016-02-28',1,NOW(),NOW()),
  ('STF-0009','Roshan Dissanayake',       'Administrative','Administration',   'Data Entry Clerk',          '0112345009','roshan@fmd.lk',  '2021-08-01',1,NOW(),NOW()),
  ('STF-0010','Sameera Rajapaksa',        'Clerical',      'Administration',   'Office Clerk',              '0112345010','sameera@fmd.lk', '2023-01-10',1,NOW(),NOW());

-- ── Doctors ──────────────────────────────────────────────────
INSERT IGNORE INTO apps_staff_doctor
  (doctor_id, staff_id, full_name, nmc_number, qualification, specialization, jmo_type, license_number, department, office_contact_no, is_active, created_at, updated_at)
VALUES
  ('DOC-0001','STF-0001','Samantha Perera',     'NMC-2001-001','MBBS, MD (Forensic)','Forensic Pathology', 'Consultant JMO','LIC-001','Forensic Medicine','0112345001',1,NOW(),NOW()),
  ('DOC-0002','STF-0002','Nimal Silva',          'NMC-2005-042','MBBS, DFM',          'Forensic Medicine',  'Senior JMO',    'LIC-002','Forensic Medicine','0112345002',1,NOW(),NOW()),
  ('DOC-0003','STF-0003','Kumari Bandara',       'NMC-2010-187','MBBS',               'Clinical Forensic',  'Senior JMO',    'LIC-003','Forensic Medicine','0112345003',1,NOW(),NOW()),
  ('DOC-0004','STF-0004','Asanka Jayawardena',   'NMC-1998-023','MBBS, MD',           'Forensic Pathology', 'Consultant JMO','LIC-004','Forensic Medicine','0112345004',1,NOW(),NOW()),
  ('DOC-0005','STF-0005','Dilani Wickramasinghe','NMC-2008-156','MBBS, DFM',          'Clinical Forensic',  'Junior JMO',    'LIC-005','Forensic Medicine','0112345005',1,NOW(),NOW());

-- ── Patients ─────────────────────────────────────────────────
INSERT IGNORE INTO apps_patients_patient
  (patient_id, full_name, nic_passport, date_of_birth, age, gender, address, district, contact_no, civil_status, occupation, notes, registered_at, updated_at)
VALUES
  ('PAT-0001','Kamal Perera',       '851234567V',   '1985-03-12',40,'Male',  '27 Galle Rd, Colombo 3',      'Colombo',     '0771234001','Married', 'Accountant','',NOW(),NOW()),
  ('PAT-0002','Sithara Fernando',   '920456789V',   '1992-07-22',32,'Female','14 Kandy Rd, Gampaha',        'Gampaha',     '0771234002','Single',  'Teacher',  '',NOW(),NOW()),
  ('PAT-0003','Rohan Jayawardena',  '780234567V',   '1978-11-05',46,'Male',  '88 Main St, Kandy',           'Kandy',       '0771234003','Married', 'Farmer',   '',NOW(),NOW()),
  ('PAT-0004','Nirmala Dissanayake','198905678901', '1989-02-28',36,'Female','33 Beach Rd, Galle',          'Galle',       '0771234004','Married', 'Nurse',    '',NOW(),NOW()),
  ('PAT-0005','Ajith Bandara',      '720123456V',   '1972-08-15',52,'Male',  '7 Temple Rd, Kandy',          'Kandy',       '0771234005','Married', 'Driver',   '',NOW(),NOW()),
  ('PAT-0006','Priyanka Herath',    '199512345678', '1995-04-10',30,'Female','22 Hill St, Nuwara Eliya',    'Nuwara Eliya','0771234006','Single',  'Student',  '',NOW(),NOW()),
  ('PAT-0007','Mahinda Senanayake', '650456123V',   '1965-09-03',59,'Male',  '5 Harbour Rd, Hambantota',    'Hambantota',  '0771234007','Widowed', 'Fisherman','',NOW(),NOW()),
  ('PAT-0008','Dilrukshi Fonseka',  '880789456V',   '1988-12-20',36,'Female','45 Fort Rd, Jaffna',          'Jaffna',      '0771234008','Married', 'Clerk',    '',NOW(),NOW()),
  ('PAT-0009','Chaminda Rathnayake','750678901V',   '1975-06-18',49,'Male',  '11 Lake Rd, Kurunegala',      'Kurunegala',  '0771234009','Married', 'Mechanic', '',NOW(),NOW()),
  ('PAT-0010','Sandya Weerasekara', '199023456789', '1990-01-07',35,'Female','67 Park Rd, Ratnapura',       'Ratnapura',   '0771234010','Single',  'Beautician','',NOW(),NOW());

SET FOREIGN_KEY_CHECKS = 1;
-- NOTE: ForensicCase, ClinicalExamination, Postmortem, Evidence, etc.
-- are best seeded via: python manage.py seed_data
-- (handles auto-generated IDs and FK relations correctly)
