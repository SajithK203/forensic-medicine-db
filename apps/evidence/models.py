from django.db import models
import random, string
from apps.cases.models import ForensicCase
from apps.staff.models import Staff


def _gen_barcode():
    """Generate a unique FMD barcode."""
    chars = ''.join(random.choices(string.digits, k=8))
    return f'FMD{chars}'


class Evidence(models.Model):
    ANALYSIS_CHOICES = [
        ('Pending',    'Pending'),
        ('InProgress', 'In Progress'),
        ('Completed',  'Completed'),
        ('Failed',     'Failed'),
        ('Disputed',   'Disputed'),
    ]
    DISPOSAL_CHOICES = [
        ('Stored',            'Stored'),
        ('ReturnedToPolice',  'Returned to Police'),
        ('Destroyed',         'Destroyed'),
        ('Unknown',           'Unknown'),
    ]

    evidence_id          = models.CharField(max_length=20, primary_key=True, editable=False)
    evidence_number      = models.CharField(max_length=50, unique=True, editable=False)
    case                 = models.ForeignKey(ForensicCase, on_delete=models.PROTECT, related_name='evidence_items')
    evidence_type        = models.CharField(max_length=100)
    evidence_description = models.TextField(blank=True)
    collection_date      = models.DateTimeField()
    collected_by         = models.CharField(max_length=100, blank=True)
    storage_location     = models.CharField(max_length=300, blank=True)
    storage_temperature  = models.CharField(max_length=50,  blank=True)
    storage_conditions   = models.CharField(max_length=300, blank=True)
    barcode_number       = models.CharField(max_length=100, unique=True, blank=True)
    qr_code_data         = models.CharField(max_length=500, blank=True)
    chain_of_custody     = models.TextField(blank=True)
    last_handled_by      = models.CharField(max_length=100, blank=True)
    last_handled_date    = models.DateTimeField(null=True, blank=True)
    analysis_status      = models.CharField(max_length=20, choices=ANALYSIS_CHOICES, default='Pending')
    analysis_type        = models.CharField(max_length=200, blank=True)
    analysis_result      = models.TextField(blank=True)
    disposal_status      = models.CharField(max_length=25, choices=DISPOSAL_CHOICES, default='Stored')
    disposal_date        = models.DateTimeField(null=True, blank=True)
    disposal_approved_by = models.CharField(max_length=100, blank=True)
    remarks              = models.TextField(blank=True)
    created_at           = models.DateTimeField(auto_now_add=True)
    updated_at           = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        from django.utils import timezone
        if not self.evidence_id:
            count = Evidence.objects.count() + 1
            ev_id = f'EV-{count:05d}'
            while Evidence.objects.filter(evidence_id=ev_id).exists():
                count += 1
                ev_id = f'EV-{count:05d}'
            self.evidence_id = ev_id
        if not self.evidence_number:
            year  = timezone.now().year
            count = Evidence.objects.filter(evidence_number__startswith=f'EVN-{year}-').count() + 1
            ev_num = f'EVN-{year}-{count:03d}'
            while Evidence.objects.filter(evidence_number=ev_num).exists():
                count += 1
                ev_num = f'EVN-{year}-{count:03d}'
            self.evidence_number = ev_num
        if not self.barcode_number:
            bc = _gen_barcode()
            while Evidence.objects.filter(barcode_number=bc).exists():
                bc = _gen_barcode()
            self.barcode_number = bc
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.evidence_number} — {self.evidence_type}'

    class Meta:
        ordering     = ['-collection_date']
        verbose_name = 'Evidence'
        verbose_name_plural = 'Evidence'


class LaboratoryTest(models.Model):
    STATUS_CHOICES = [
        ('Pending',    'Pending'),
        ('InProgress', 'In Progress'),
        ('Completed',  'Completed'),
        ('Failed',     'Failed'),
        ('OnHold',     'On Hold'),
    ]

    test_id             = models.CharField(max_length=20, primary_key=True, editable=False)
    evidence            = models.ForeignKey(Evidence, on_delete=models.PROTECT, related_name='lab_tests')
    technician          = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, blank=True,
                                            related_name='lab_tests')
    test_type           = models.CharField(max_length=100)
    test_description    = models.CharField(max_length=300, blank=True)
    requested_date      = models.DateTimeField(null=True, blank=True)
    requested_by        = models.CharField(max_length=100, blank=True)
    test_date           = models.DateTimeField()
    completion_date     = models.DateTimeField(null=True, blank=True)
    test_result         = models.TextField(blank=True)
    result_interpretation = models.TextField(blank=True)
    test_status         = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    reference_number    = models.CharField(max_length=50, blank=True)
    test_notes          = models.TextField(blank=True)
    certificate_issued  = models.BooleanField(default=False)
    certificate_path    = models.CharField(max_length=500, blank=True)
    report_path         = models.CharField(max_length=500, blank=True)
    created_at          = models.DateTimeField(auto_now_add=True)
    updated_at          = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.test_id:
            count = LaboratoryTest.objects.count() + 1
            self.test_id = f'LT-{count:05d}'
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.test_id} — {self.test_type}'

    class Meta:
        ordering     = ['-test_date']
        verbose_name = 'Laboratory Test'
