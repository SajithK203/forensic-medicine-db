from django.db import models
from django.utils import timezone
from apps.patients.models import Patient
from apps.staff.models import Doctor


class ForensicCase(models.Model):
    TYPE_CLINICAL  = 'Clinical Forensic'
    TYPE_AUTOPSY   = 'Autopsy'
    TYPE_BOTH      = 'Clinical & Autopsy'

    STATUS_PENDING    = 'Pending'
    STATUS_INPROGRESS = 'InProgress'
    STATUS_COMPLETED  = 'Completed'
    STATUS_SUBMITTED  = 'Submitted'
    STATUS_CLOSED     = 'Closed'
    STATUS_ARCHIVED   = 'Archived'

    PRIORITY_LOW      = 'Low'
    PRIORITY_MEDIUM   = 'Medium'
    PRIORITY_HIGH     = 'High'
    PRIORITY_CRITICAL = 'Critical'

    TYPE_CHOICES = [
        (TYPE_CLINICAL, 'Clinical Forensic'),
        (TYPE_AUTOPSY,  'Autopsy'),
        (TYPE_BOTH,     'Clinical & Autopsy'),
    ]
    STATUS_CHOICES = [
        (STATUS_PENDING,    'Pending'),
        (STATUS_INPROGRESS, 'In Progress'),
        (STATUS_COMPLETED,  'Completed'),
        (STATUS_SUBMITTED,  'Submitted'),
        (STATUS_CLOSED,     'Closed'),
        (STATUS_ARCHIVED,   'Archived'),
    ]
    PRIORITY_CHOICES = [
        (PRIORITY_LOW,      'Low'),
        (PRIORITY_MEDIUM,   'Medium'),
        (PRIORITY_HIGH,     'High'),
        (PRIORITY_CRITICAL, 'Critical'),
    ]

    case_id           = models.CharField(max_length=20, primary_key=True, editable=False)
    case_number       = models.CharField(max_length=30, unique=True, editable=False)
    patient           = models.ForeignKey(Patient, on_delete=models.PROTECT, related_name='cases')
    doctor            = models.ForeignKey(Doctor,  on_delete=models.PROTECT, related_name='cases')
    case_type         = models.CharField(max_length=30, choices=TYPE_CHOICES)
    incident_date     = models.DateTimeField()
    incident_location = models.CharField(max_length=300, blank=True)
    incident_type     = models.CharField(max_length=100, blank=True)
    police_report_no  = models.CharField(max_length=50,  blank=True)
    court_case_no     = models.CharField(max_length=50,  blank=True)
    case_status       = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
    priority          = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default=PRIORITY_MEDIUM)
    case_notes        = models.TextField(blank=True)
    created_at        = models.DateTimeField(auto_now_add=True)
    updated_at        = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.case_id:
            count = ForensicCase.objects.count() + 1
            self.case_id = f'CASE-{count:05d}'
        if not self.case_number:
            year  = timezone.now().year
            count = ForensicCase.objects.filter(incident_date__year=year).count() + 1
            self.case_number = f'FMD-{year}-{count:04d}'
        super().save(*args, **kwargs)

    # ── Status helpers ────────────────────────────────────────────────────────
    @property
    def status_badge(self):
        return {
            self.STATUS_PENDING:    'badge-warning',
            self.STATUS_INPROGRESS: 'badge-info',
            self.STATUS_COMPLETED:  'badge-success',
            self.STATUS_SUBMITTED:  'badge-primary',
            self.STATUS_CLOSED:     'badge-secondary',
            self.STATUS_ARCHIVED:   'badge-dark',
        }.get(self.case_status, 'badge-secondary')

    @property
    def priority_badge(self):
        return {
            self.PRIORITY_LOW:      'badge-muted',
            self.PRIORITY_MEDIUM:   'badge-info',
            self.PRIORITY_HIGH:     'badge-warning',
            self.PRIORITY_CRITICAL: 'badge-danger',
        }.get(self.priority, 'badge-info')

    def __str__(self):
        return f'{self.case_number} — {self.patient.full_name}'

    class Meta:
        ordering      = ['-created_at']
        verbose_name  = 'Forensic Case'


# ── CaseNote ──────────────────────────────────────────────────────────────────
class CaseNote(models.Model):
    """Timestamped notes added by staff on a forensic case over time."""

    NOTE_TYPE_GENERAL   = 'General'
    NOTE_TYPE_MEDICAL   = 'Medical'
    NOTE_TYPE_LEGAL     = 'Legal'
    NOTE_TYPE_FOLLOWUP  = 'FollowUp'
    NOTE_TYPE_INTERNAL  = 'Internal'

    NOTE_TYPE_CHOICES = [
        (NOTE_TYPE_GENERAL,  'General'),
        (NOTE_TYPE_MEDICAL,  'Medical'),
        (NOTE_TYPE_LEGAL,    'Legal'),
        (NOTE_TYPE_FOLLOWUP, 'Follow-Up'),
        (NOTE_TYPE_INTERNAL, 'Internal'),
    ]

    note_id     = models.CharField(max_length=15, primary_key=True, editable=False)
    case        = models.ForeignKey(ForensicCase, on_delete=models.CASCADE, related_name='notes')
    author      = models.CharField(max_length=100)
    note_type   = models.CharField(max_length=20, choices=NOTE_TYPE_CHOICES, default=NOTE_TYPE_GENERAL)
    note_text   = models.TextField()
    is_private  = models.BooleanField(default=False, help_text='Private notes are only visible to doctors')
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.note_id:
            count = CaseNote.objects.count() + 1
            self.note_id = f'CN-{count:05d}'
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.note_id} — {self.case.case_number} [{self.note_type}]'

    class Meta:
        ordering     = ['-created_at']
        verbose_name = 'Case Note'


# ── WitnessStatement ──────────────────────────────────────────────────────────
class WitnessStatement(models.Model):
    """Records witness statements collected in relation to a forensic case."""

    STATEMENT_VERBAL  = 'Verbal'
    STATEMENT_WRITTEN = 'Written'
    STATEMENT_RECORDED = 'Recorded'

    STATEMENT_TYPE_CHOICES = [
        (STATEMENT_VERBAL,   'Verbal'),
        (STATEMENT_WRITTEN,  'Written'),
        (STATEMENT_RECORDED, 'Audio/Video Recorded'),
    ]

    statement_id      = models.CharField(max_length=15, primary_key=True, editable=False)
    case              = models.ForeignKey(ForensicCase, on_delete=models.PROTECT, related_name='witness_statements')
    witness_name      = models.CharField(max_length=100)
    witness_nic       = models.CharField(max_length=20, blank=True, verbose_name='NIC / ID Number')
    witness_contact   = models.CharField(max_length=15, blank=True)
    witness_address   = models.TextField(blank=True)
    relationship_to_case = models.CharField(max_length=100, blank=True,
                                            help_text='e.g. Eyewitness, Relative, Police Officer')
    statement_type    = models.CharField(max_length=20, choices=STATEMENT_TYPE_CHOICES, default=STATEMENT_WRITTEN)
    statement_text    = models.TextField()
    statement_date    = models.DateTimeField()
    recorded_by       = models.CharField(max_length=100, blank=True)
    recording_path    = models.CharField(max_length=500, blank=True)
    is_verified       = models.BooleanField(default=False)
    verified_by       = models.CharField(max_length=100, blank=True)
    created_at        = models.DateTimeField(auto_now_add=True)
    updated_at        = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.statement_id:
            count = WitnessStatement.objects.count() + 1
            self.statement_id = f'WS-{count:05d}'
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.statement_id} — {self.witness_name} ({self.case.case_number})'

    class Meta:
        ordering     = ['-statement_date']
        verbose_name = 'Witness Statement'

