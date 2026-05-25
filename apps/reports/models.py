from django.db import models
from apps.cases.models import ForensicCase
from apps.staff.models import Doctor


class CourtReport(models.Model):
    TYPE_MLR      = 'MLR'
    TYPE_PMR      = 'PMR'
    TYPE_COMBINED = 'Combined'

    STATUS_DRAFT     = 'Draft'
    STATUS_GENERATED = 'Generated'
    STATUS_REVIEWED  = 'Reviewed'
    STATUS_SUBMITTED = 'Submitted'
    STATUS_RECEIVED  = 'Received'
    STATUS_ARCHIVED  = 'Archived'

    TYPE_CHOICES = [
        (TYPE_MLR,      'MLR — Medico-Legal Report'),
        (TYPE_PMR,      'PMR — Postmortem Report'),
        (TYPE_COMBINED, 'Combined (MLR + PMR)'),
    ]
    STATUS_CHOICES = [
        (STATUS_DRAFT,     'Draft'),
        (STATUS_GENERATED, 'Generated'),
        (STATUS_REVIEWED,  'Reviewed'),
        (STATUS_SUBMITTED, 'Submitted'),
        (STATUS_RECEIVED,  'Received'),
        (STATUS_ARCHIVED,  'Archived'),
    ]

    report_id                 = models.CharField(max_length=20, primary_key=True, editable=False)
    case                      = models.ForeignKey(ForensicCase, on_delete=models.PROTECT, related_name='court_reports')
    doctor                    = models.ForeignKey(Doctor, on_delete=models.PROTECT, related_name='court_reports')
    report_type               = models.CharField(max_length=10, choices=TYPE_CHOICES)
    report_title              = models.CharField(max_length=300, blank=True)
    report_content            = models.TextField(blank=True)
    report_conclusions        = models.TextField(blank=True)
    recommended_investigations = models.TextField(blank=True)
    court_name                = models.CharField(max_length=300, blank=True)
    court_case_number         = models.CharField(max_length=50,  blank=True)
    magistrate_district       = models.CharField(max_length=100, blank=True)
    judge_name                = models.CharField(max_length=100, blank=True)
    lawyer_details            = models.CharField(max_length=300, blank=True)
    report_status             = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_DRAFT)
    generated_at              = models.DateTimeField(auto_now_add=True)
    submitted_at              = models.DateTimeField(null=True, blank=True)
    received_at               = models.DateTimeField(null=True, blank=True)
    submission_proof_path     = models.CharField(max_length=500, blank=True)
    digital_signature_path    = models.CharField(max_length=500, blank=True)
    approved_by               = models.CharField(max_length=100, blank=True)
    approved_at               = models.DateTimeField(null=True, blank=True)
    remarks                   = models.TextField(blank=True)
    created_at                = models.DateTimeField(auto_now_add=True)
    updated_at                = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.report_id:
            count = CourtReport.objects.count() + 1
            self.report_id = f'RPT-{count:05d}'
        super().save(*args, **kwargs)

    @property
    def status_badge(self):
        return {
            self.STATUS_DRAFT:     'badge-secondary',
            self.STATUS_GENERATED: 'badge-info',
            self.STATUS_REVIEWED:  'badge-primary',
            self.STATUS_SUBMITTED: 'badge-warning',
            self.STATUS_RECEIVED:  'badge-success',
            self.STATUS_ARCHIVED:  'badge-dark',
        }.get(self.report_status, 'badge-secondary')

    def __str__(self):
        return f'{self.report_id} — {self.get_report_type_display()} ({self.report_status})'

    class Meta:
        ordering     = ['-generated_at']
        verbose_name = 'Court Report'
