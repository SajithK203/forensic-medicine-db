from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta, date, datetime
import random


class Command(BaseCommand):
    help = 'Seed initial sample data — staff, patients, cases, evidence, reports'

    def handle(self, *args, **options):
        self.stdout.write(self.style.MIGRATE_HEADING('\n[*] Seeding Forensic Medicine DB...\n'))

        from django.contrib.auth import get_user_model
        from apps.staff.models     import Staff, Doctor
        from apps.patients.models  import Patient
        from apps.cases.models     import ForensicCase
        from apps.clinical.models  import ClinicalExamination
        from apps.postmortem.models import Postmortem
        from apps.evidence.models  import Evidence, LaboratoryTest
        from apps.reports.models   import CourtReport

        User = get_user_model()

        # ── 1. Users ────────────────────────────────────────────────────────
        def make_user(username, password, role, first, last, email):
            if not User.objects.filter(username=username).exists():
                u = User.objects.create_user(
                    username=username, password=password,
                    first_name=first, last_name=last,
                    email=email, role=role)
                self.stdout.write(f'  [+] User  {username} / {password}  [{role}]')
                return u
            return User.objects.get(username=username)

        make_user('admin',    'Admin@123',  'Administrator', 'System',   'Admin',         'admin@fmd.lk')
        make_user('dr_perera','Doctor@123', 'Doctor',        'Samantha', 'Perera',        'dr.perera@fmd.lk')
        make_user('dr_silva', 'Doctor@123', 'Doctor',        'Nimal',    'Silva',         'dr.silva@fmd.lk')
        make_user('lab_tech', 'Lab@123',    'LabTechnician', 'Nuwan',    'Karunaratne',   'lab@fmd.lk')
        make_user('viewer',   'View@123',   'Viewer',        'Saman',    'Dissanayake',   'viewer@fmd.lk')

        # ── 2. Staff ────────────────────────────────────────────────────────
        staff_data = [
            ('Dr. Samantha Perera',      'Doctor',         'Head of Forensic Medicine', '0112345001', 'dr.perera@fmd.lk'),
            ('Dr. Nimal Silva',          'Doctor',         'Consultant JMO',            '0112345002', 'dr.silva@fmd.lk'),
            ('Dr. Kumari Bandara',       'Doctor',         'Senior JMO',                '0112345003', 'dr.kumari@fmd.lk'),
            ('Dr. Asanka Jayawardena',   'Doctor',         'Junior JMO',                '0112345004', 'dr.asanka@fmd.lk'),
            ('Dr. Dilani Wickramasinghe','Doctor',         'Senior JMO',                '0112345005', 'dr.dilani@fmd.lk'),
            ('Nuwan Karunaratne',        'Laboratory',     'Chief Lab Technician',      '0112345006', 'nuwan.lab@fmd.lk'),
            ('Chamari Herath',           'Laboratory',     'Lab Technician',            '0112345007', 'chamari.lab@fmd.lk'),
            ('Lakshmi Ranasinghe',       'Administrative', 'Administrative Officer',    '0112345008', 'lakshmi@fmd.lk'),
            ('Roshan Dissanayake',       'Administrative', 'Data Entry Clerk',          '0112345009', 'roshan@fmd.lk'),
            ('Sameera Rajapaksa',        'Clerical',       'Office Clerk',              '0112345010', 'sameera@fmd.lk'),
        ]
        staff_objs = []
        for (name, stype, desig, phone, email) in staff_data:
            s, _ = Staff.objects.get_or_create(
                email=email,
                defaults=dict(full_name=name, staff_type=stype, designation=desig,
                              contact_no=phone, join_date=date(2018, 1, 15), is_active=True))
            staff_objs.append(s)
        self.stdout.write(f'  [+] Staff  ({len(staff_objs)} records)')

        # ── 3. Doctors ──────────────────────────────────────────────────────
        doctor_data = [
            (staff_objs[0], 'Samantha Perera',       'NMC-2001-001', 'MBBS, MD (Forensic)', 'Forensic Pathology',  'Consultant JMO', 'LIC-001'),
            (staff_objs[1], 'Nimal Silva',            'NMC-2005-042', 'MBBS, DFM',           'Forensic Medicine',   'Senior JMO',     'LIC-002'),
            (staff_objs[2], 'Kumari Bandara',         'NMC-2010-187', 'MBBS',                'Clinical Forensic',   'Senior JMO',     'LIC-003'),
            (staff_objs[3], 'Asanka Jayawardena',     'NMC-1998-023', 'MBBS, MD',            'Forensic Pathology',  'Consultant JMO', 'LIC-004'),
            (staff_objs[4], 'Dilani Wickramasinghe',  'NMC-2008-156', 'MBBS, DFM',           'Clinical Forensic',   'Junior JMO',     'LIC-005'),
        ]
        doctor_objs = []
        for (stf, name, nmc, qual, spec, jtype, lic) in doctor_data:
            d, _ = Doctor.objects.get_or_create(
                nmc_number=nmc,
                defaults=dict(staff=stf, full_name=name, qualification=qual,
                              specialization=spec, jmo_type=jtype, license_number=lic,
                              office_contact_no=stf.contact_no, is_active=True))
            doctor_objs.append(d)
        self.stdout.write(f'  [+] Doctors ({len(doctor_objs)} records)')

        # ── 4. Patients ──────────────────────────────────────────────────────
        now = timezone.now()
        patient_data = [
            ('Kamal Perera',       '851234567V',  date(1985, 3, 12), 40, 'Male',   '27 Galle Rd, Colombo 3', 'Colombo',      '0771234001', 'Married',  'Accountant'),
            ('Sithara Fernando',   '920456789V',  date(1992, 7, 22), 32, 'Female', '14 Kandy Rd, Gampaha',   'Gampaha',      '0771234002', 'Single',   'Teacher'),
            ('Rohan Jayawardena',  '780234567V',  date(1978, 11, 5), 46, 'Male',   '88 Main St, Kandy',      'Kandy',        '0771234003', 'Married',  'Farmer'),
            ('Nirmala Dissanayake','198905678901', date(1989, 2, 28), 36, 'Female', '33 Beach Rd, Galle',     'Galle',        '0771234004', 'Married',  'Nurse'),
            ('Ajith Bandara',      '720123456V',  date(1972, 8, 15), 52, 'Male',   '7 Temple Rd, Kandy',     'Kandy',        '0771234005', 'Married',  'Driver'),
            ('Priyanka Herath',    '199512345678', date(1995, 4, 10), 30, 'Female', '22 Hill St, Nuwara Eliya','Nuwara Eliya', '0771234006', 'Single',   'Student'),
            ('Mahinda Senanayake', '650456123V',  date(1965, 9, 3),  59, 'Male',   '5 Harbour Rd, Hambantota','Hambantota',   '0771234007', 'Widowed',  'Fisherman'),
            ('Dilrukshi Fonseka',  '880789456V',  date(1988, 12, 20),36, 'Female', '45 Fort Rd, Jaffna',     'Jaffna',       '0771234008', 'Married',  'Clerk'),
            ('Chaminda Rathnayake','750678901V',  date(1975, 6, 18), 49, 'Male',   '11 Lake Rd, Kurunegala', 'Kurunegala',   '0771234009', 'Married',  'Mechanic'),
            ('Sandya Weerasekara', '199023456789', date(1990, 1, 7),  35, 'Female', '67 Park Rd, Ratnapura',  'Ratnapura',    '0771234010', 'Single',   'Beautician'),
        ]
        patient_objs = []
        for (name, nic, dob, age, gender, addr, dist, phone, civil, occ) in patient_data:
            p, _ = Patient.objects.get_or_create(
                nic_passport=nic,
                defaults=dict(full_name=name, date_of_birth=dob, age=age, gender=gender,
                              address=addr, district=dist, contact_no=phone,
                              civil_status=civil, occupation=occ))
            patient_objs.append(p)
        self.stdout.write(f'  [+] Patients ({len(patient_objs)} records)')

        # ── 5. Forensic Cases ────────────────────────────────────────────────
        case_data = [
            (patient_objs[0], doctor_objs[0], 'Clinical Forensic',  now - timedelta(days=35),  'Colombo',        'Assault',          'B/COL/3456/2026', '',              'InProgress', 'High'),
            (patient_objs[1], doctor_objs[1], 'Clinical Forensic',  now - timedelta(days=10),  'Gampaha',        'Road Accident',     'B/GAM/1234/2026', '',              'Completed',  'Medium'),
            (patient_objs[2], doctor_objs[0], 'Autopsy',            now - timedelta(days=3),   'Kandy Mortuary', 'Suspicious Death',  'B/KDY/0789/2026', 'HC/KDY/12/26', 'InProgress', 'Critical'),
            (patient_objs[3], doctor_objs[2], 'Clinical & Autopsy', now - timedelta(days=15),  'Galle',          'Drowning',          'B/GAL/2345/2026', '',              'Completed',  'High'),
            (patient_objs[4], doctor_objs[3], 'Autopsy',            now - timedelta(days=20),  'Kandy',          'Sudden Death',      'B/KDY/0345/2026', 'MC/KDY/08/26', 'Closed',     'Medium'),
            (patient_objs[5], doctor_objs[1], 'Clinical Forensic',  now - timedelta(days=2),   'Nuwara Eliya',   'Domestic Violence', 'B/NE/0456/2026',  '',              'Pending',    'High'),
            (patient_objs[6], doctor_objs[4], 'Autopsy',            now - timedelta(days=42),  'Hambantota',     'Found Dead',        'B/HAM/1890/2026', 'MC/HAM/05/26', 'InProgress', 'Medium'),
            (patient_objs[7], doctor_objs[0], 'Clinical Forensic',  now - timedelta(days=12),  'Jaffna',         'Sexual Assault',    'B/JAF/0234/2026', 'HC/JAF/22/26', 'Submitted',  'Critical'),
            (patient_objs[8], doctor_objs[2], 'Clinical Forensic',  now - timedelta(days=30),  'Kurunegala',     'Workplace Injury',  'B/KUR/0567/2026', '',              'Completed',  'Low'),
            (patient_objs[9], doctor_objs[3], 'Clinical & Autopsy', now - timedelta(days=45),  'Ratnapura',      'Poisoning',         'B/RAT/0123/2026', 'HC/RAT/18/26', 'Closed',     'High'),
        ]
        case_objs = []
        for (pat, doc, ctype, idate, iloc, itype, police_no, court_no, status, priority) in case_data:
            existing = ForensicCase.objects.filter(police_report_no=police_no).first() if police_no else None
            if not existing:
                c = ForensicCase(
                    patient=pat, doctor=doc, case_type=ctype, incident_date=idate,
                    incident_location=iloc, incident_type=itype, police_report_no=police_no,
                    court_case_no=court_no, case_status=status, priority=priority,
                    case_notes=f'Initial case notes for {itype} case.')
                c.save()
                case_objs.append(c)
            else:
                case_objs.append(existing)
        self.stdout.write(f'  [+] Cases  ({len(case_objs)} records)')

        # ── 6. Clinical Examinations ──────────────────────────────────────────
        clinical_cases = [c for c in case_objs if c.case_type in ['Clinical Forensic', 'Clinical & Autopsy']]
        exam_objs = []
        for i, case in enumerate(clinical_cases[:5]):
            if not ClinicalExamination.objects.filter(case=case).exists():
                e = ClinicalExamination(
                    case=case, doctor=case.doctor,
                    examination_date=case.incident_date + timedelta(hours=2),
                    examination_type='Medico-Legal Examination',
                    general_condition=['Good', 'Fair', 'Poor', 'Critical', 'Stable'][i % 5],
                    consciousness=['Alert', 'Alert', 'Confused', 'Alert', 'Drowsy'][i % 5],
                    injury_details='Multiple bruises and lacerations noted on examination.',
                    wound_description='Blunt force trauma injuries consistent with the history.',
                    examination_findings='Findings are consistent with the alleged mechanism of injury.',
                    photographs_taken=random.randint(4, 20))
                e.save()
                exam_objs.append(e)
        self.stdout.write(f'  [+] Clinical Exams ({len(exam_objs)} records)')

        # ── 7. Postmortems ──────────────────────────────────────────────────
        autopsy_cases = [c for c in case_objs if c.case_type in ['Autopsy', 'Clinical & Autopsy']]
        pm_objs = []
        death_types = ['Homicidal', 'Accidental', 'Natural', 'Undetermined', 'Accidental']
        causes = [
            ('Haemorrhagic shock',         'Blunt force head trauma', '', ''),
            ('Asphyxia',                   'Drowning',                '', ''),
            ('Cardiac arrest',             'Coronary artery disease', '', ''),
            ('Multi-organ failure',        'Poisoning',              'Toxic substance ingestion', ''),
            ('Cardiorespiratory failure',  'Natural causes',          '', ''),
        ]
        for i, case in enumerate(autopsy_cases[:5]):
            if not Postmortem.objects.filter(case=case).exists():
                imm, a, b, c_ = causes[i % len(causes)]
                pm = Postmortem(
                    case=case, doctor=case.doctor,
                    autopsy_date=case.incident_date + timedelta(days=1),
                    autopsy_location='Teaching Hospital Mortuary',
                    death_type=death_types[i % len(death_types)],
                    immediate_cause=imm, cause_a=a, cause_b=b, cause_c=c_,
                    external_findings='Body well-nourished. Injuries as described.',
                    internal_findings='Internal organs examined. Significant findings noted.',
                    photographs_taken=random.randint(10, 25),
                    specimen_collected=True,
                    specimen_details='Blood, urine, and tissue samples collected.',
                    report_status='Completed')
                pm.save()
                pm_objs.append(pm)
        self.stdout.write(f'  [+] Postmortems ({len(pm_objs)} records)')

        # ── 8. Evidence ──────────────────────────────────────────────────────
        ev_types = [
            ('Blood Sample',  'Venous blood sample collected for toxicology.',       '-20°C Freezer', 'DNA, Toxicology'),
            ('Clothing',      'Torn clothing with suspected blood stains.',           'Room Temp',     'Serology'),
            ('Hair Sample',   'Hair follicles collected from scene.',                '4°C Fridge',    'DNA Analysis'),
            ('Swab Sample',   'Buccal swab and wound swab collected.',               '4°C Fridge',    'DNA, Microbiology'),
            ('Fingernail Clippings', 'Clippings from all 10 fingers.',              '4°C Fridge',    'DNA'),
            ('Urine Sample',  'Urine sample for drug/alcohol screening.',            '4°C Fridge',    'Toxicology'),
            ('Weapon (Knife)','Kitchen knife recovered at scene, possible weapon.',  'Secure Room',   'Fingerprint, DNA'),
            ('Photographs',   'Scene photographs printed and sealed.',               'Dry Room',      'None'),
        ]
        ev_objs = []
        for i, case in enumerate(case_objs[:8]):
            etype, edesc, storage, analysis = ev_types[i % len(ev_types)]
            if not Evidence.objects.filter(case=case, evidence_type=etype).exists():
                ev = Evidence(
                    case=case, evidence_type=etype, evidence_description=edesc,
                    collection_date=case.incident_date + timedelta(hours=1),
                    collected_by=case.doctor.full_name,
                    storage_location=f'Forensic Lab — {storage}',
                    storage_temperature=storage,
                    analysis_type=analysis,
                    analysis_status=random.choice(['Pending', 'Pending', 'InProgress', 'Completed']))
                ev.save()
                ev_objs.append(ev)
        self.stdout.write(f'  [+] Evidence ({len(ev_objs)} records)')

        # ── 9. Lab Tests ─────────────────────────────────────────────────────
        lab_staff = staff_objs[5]  # Nuwan Karunaratne — Lab technician
        lt_objs = []
        test_types = ['Blood Alcohol Test', 'DNA Profiling', 'Toxicology Screen', 'Serology Test', 'Histology']
        for i, ev in enumerate(ev_objs[:5]):
            if not LaboratoryTest.objects.filter(evidence=ev).exists():
                lt = LaboratoryTest(
                    evidence=ev, technician=lab_staff,
                    test_type=test_types[i % len(test_types)],
                    test_date=ev.collection_date + timedelta(days=1),
                    requested_by=ev.case.doctor.full_name,
                    test_status=random.choice(['Pending', 'InProgress', 'Completed']),
                    test_notes='Standard protocol followed.')
                lt.save()
                lt_objs.append(lt)
        self.stdout.write(f'  [+] Lab Tests ({len(lt_objs)} records)')

        # ── 10. Court Reports ────────────────────────────────────────────────
        report_data = [
            (case_objs[7], doctor_objs[0], 'MLR', 'Medico-Legal Report — Sexual Assault',
             'High Court Colombo', 'HC/JAF/22/26', 'Submitted'),
            (case_objs[1], doctor_objs[1], 'MLR', 'Medico-Legal Report — Road Accident',
             'Gampaha Magistrate Court', 'MC/GAM/45/26', 'Generated'),
            (case_objs[4], doctor_objs[3], 'PMR', 'Postmortem Report — Sudden Death',
             'Kandy Magistrate Court', 'MC/KDY/08/26', 'Received'),
            (case_objs[9], doctor_objs[3], 'PMR', 'Postmortem Report — Poisoning',
             'High Court Ratnapura', 'HC/RAT/18/26', 'Reviewed'),
            (case_objs[3], doctor_objs[2], 'Combined', 'MLR + PMR — Drowning Case',
             'Galle Magistrate Court', 'MC/GAL/67/26', 'Draft'),
        ]
        rpt_objs = []
        for (case, doc, rtype, title, court, court_no, status) in report_data:
            if not CourtReport.objects.filter(case=case, report_type=rtype).exists():
                rpt = CourtReport(
                    case=case, doctor=doc, report_type=rtype, report_title=title,
                    court_name=court, court_case_number=court_no, report_status=status,
                    report_content=f'This {rtype} is prepared regarding {case.incident_type} case {case.case_number}.',
                    report_conclusions='Findings are consistent with the history provided.',
                    magistrate_district=case.incident_location)
                if status == 'Submitted':
                    rpt.submitted_at = now - timedelta(days=2)
                rpt.save()
                rpt_objs.append(rpt)
        self.stdout.write(f'  [+] Court Reports ({len(rpt_objs)} records)')

        # ── Done ─────────────────────────────────────────────────────────────
        self.stdout.write(self.style.SUCCESS('\n[DONE] Seeding complete!\n'))
        self.stdout.write('   Login credentials:')
        self.stdout.write('   +-------------+-------------+---------------+')
        self.stdout.write('   |  Username   |  Password   |  Role         |')
        self.stdout.write('   +-------------+-------------+---------------+')
        self.stdout.write('   |  admin      |  Admin@123  |  Administrator|')
        self.stdout.write('   |  dr_perera  |  Doctor@123 |  Doctor       |')
        self.stdout.write('   |  dr_silva   |  Doctor@123 |  Doctor       |')
        self.stdout.write('   |  lab_tech   |  Lab@123    |  LabTechnician|')
        self.stdout.write('   |  viewer     |  View@123   |  Viewer       |')
        self.stdout.write('   +-------------+-------------+---------------+\n')

