from django.db import models
from apps.cases.models import ForensicCase
from apps.staff.models import Doctor


class ClinicalExamination(models.Model):
    CONSCIOUSNESS_CHOICES = [
        ('Alert',       'Alert'),
        ('Confused',    'Confused'),
        ('Drowsy',      'Drowsy'),
        ('Unconscious', 'Unconscious'),
        ('Unknown',     'Unknown'),
    ]

    exam_id               = models.CharField(max_length=20, primary_key=True, editable=False)
    case                  = models.ForeignKey(ForensicCase, on_delete=models.PROTECT, related_name='clinical_examinations')
    doctor                = models.ForeignKey(Doctor,       on_delete=models.PROTECT, related_name='clinical_examinations')
    examination_date      = models.DateTimeField()
    examination_type      = models.CharField(max_length=100, blank=True)
    time_of_examination   = models.TimeField(null=True, blank=True)
    general_condition     = models.CharField(max_length=200, blank=True)
    consciousness         = models.CharField(max_length=20, choices=CONSCIOUSNESS_CHOICES, blank=True)
    nutritional_status    = models.CharField(max_length=100, blank=True)
    photographs_taken     = models.PositiveSmallIntegerField(default=0)
    photograph_path       = models.CharField(max_length=500, blank=True)
    injury_details        = models.TextField(blank=True)
    wound_description     = models.TextField(blank=True)
    examination_findings  = models.TextField(blank=True)
    causative_weapon      = models.CharField(max_length=100, blank=True)
    investigation_required = models.BooleanField(default=False)
    investigation_type    = models.CharField(max_length=200, blank=True)
    referral_required     = models.BooleanField(default=False)
    referral_department   = models.CharField(max_length=100, blank=True)
    referral_reason       = models.CharField(max_length=300, blank=True)
    officer_notes         = models.TextField(blank=True)
    created_at            = models.DateTimeField(auto_now_add=True)
    updated_at            = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.exam_id:
            count = ClinicalExamination.objects.count() + 1
            self.exam_id = f'CE-{count:05d}'
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Exam {self.exam_id} — Case {self.case.case_number}'

    class Meta:
        ordering     = ['-examination_date']
        verbose_name = 'Clinical Examination'


# ── Appointment ───────────────────────────────────────────────────────────────
class Appointment(models.Model):
    """Schedules examinations and meetings between patients, doctors and cases."""

    STATUS_SCHEDULED  = 'Scheduled'
    STATUS_CONFIRMED  = 'Confirmed'
    STATUS_COMPLETED  = 'Completed'
    STATUS_CANCELLED  = 'Cancelled'
    STATUS_NOSHOW     = 'NoShow'

    TYPE_CLINICAL     = 'ClinicalExam'
    TYPE_FOLLOWUP     = 'FollowUp'
    TYPE_COURT        = 'CourtAppearance'
    TYPE_CONSULTATION = 'Consultation'

    STATUS_CHOICES = [
        (STATUS_SCHEDULED,  'Scheduled'),
        (STATUS_CONFIRMED,  'Confirmed'),
        (STATUS_COMPLETED,  'Completed'),
        (STATUS_CANCELLED,  'Cancelled'),
        (STATUS_NOSHOW,     'No Show'),
    ]
    TYPE_CHOICES = [
        (TYPE_CLINICAL,     'Clinical Examination'),
        (TYPE_FOLLOWUP,     'Follow-Up'),
        (TYPE_COURT,        'Court Appearance'),
        (TYPE_CONSULTATION, 'Consultation'),
    ]

    appointment_id   = models.CharField(max_length=15, primary_key=True, editable=False)
    case             = models.ForeignKey(ForensicCase, on_delete=models.PROTECT, related_name='appointments')
    doctor           = models.ForeignKey(Doctor, on_delete=models.PROTECT, related_name='appointments')
    appointment_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default=TYPE_CLINICAL)
    scheduled_date   = models.DateTimeField()
    duration_minutes = models.PositiveSmallIntegerField(default=30)
    location         = models.CharField(max_length=200, blank=True)
    status           = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_SCHEDULED)
    reason           = models.CharField(max_length=300, blank=True)
    notes            = models.TextField(blank=True)
    created_at       = models.DateTimeField(auto_now_add=True)
    updated_at       = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.appointment_id:
            count = Appointment.objects.count() + 1
            self.appointment_id = f'APT-{count:05d}'
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.appointment_id} — {self.case.case_number} on {self.scheduled_date:%Y-%m-%d}'

    class Meta:
        ordering     = ['-scheduled_date']
        verbose_name = 'Appointment'

