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
