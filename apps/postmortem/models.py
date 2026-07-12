from django.db import models
from apps.cases.models import ForensicCase
from apps.staff.models import Doctor


# ── Mortuary ──────────────────────────────────────────────────────────────────
class Mortuary(models.Model):
    """Represents a physical mortuary room/facility in the department."""

    STATUS_AVAILABLE   = 'Available'
    STATUS_OCCUPIED    = 'Occupied'
    STATUS_MAINTENANCE = 'Maintenance'
    STATUS_CLOSED      = 'Closed'

    STATUS_CHOICES = [
        (STATUS_AVAILABLE,   'Available'),
        (STATUS_OCCUPIED,    'Occupied'),
        (STATUS_MAINTENANCE, 'Under Maintenance'),
        (STATUS_CLOSED,      'Closed'),
    ]

    mortuary_id      = models.CharField(max_length=15, primary_key=True, editable=False)
    room_name        = models.CharField(max_length=100)
    room_number      = models.CharField(max_length=20, unique=True)
    location         = models.CharField(max_length=200, blank=True)
    capacity         = models.PositiveSmallIntegerField(default=1, help_text='Max number of bodies')
    current_occupancy = models.PositiveSmallIntegerField(default=0)
    refrigeration    = models.BooleanField(default=True)
    temperature_celsius = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    status           = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_AVAILABLE)
    notes            = models.TextField(blank=True)
    created_at       = models.DateTimeField(auto_now_add=True)
    updated_at       = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.mortuary_id:
            count = Mortuary.objects.count() + 1
            self.mortuary_id = f'MRT-{count:04d}'
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.room_name} ({self.room_number}) — {self.status}'

    class Meta:
        ordering     = ['room_number']
        verbose_name = 'Mortuary'
        verbose_name_plural = 'Mortuaries'


class Postmortem(models.Model):
    DEATH_NATURAL      = 'Natural'
    DEATH_ACCIDENTAL   = 'Accidental'
    DEATH_SUICIDAL     = 'Suicidal'
    DEATH_HOMICIDAL    = 'Homicidal'
    DEATH_UNDETERMINED = 'Undetermined'

    DEATH_TYPE_CHOICES = [
        (DEATH_NATURAL,      'Natural'),
        (DEATH_ACCIDENTAL,   'Accidental'),
        (DEATH_SUICIDAL,     'Suicidal'),
        (DEATH_HOMICIDAL,    'Homicidal'),
        (DEATH_UNDETERMINED, 'Undetermined'),
    ]
    REPORT_STATUS_CHOICES = [
        ('Pending',    'Pending'),
        ('InProgress', 'In Progress'),
        ('Completed',  'Completed'),
        ('Reviewed',   'Reviewed'),
    ]

    postmortem_id          = models.CharField(max_length=20, primary_key=True, editable=False)
    case                   = models.OneToOneField(ForensicCase, on_delete=models.PROTECT, related_name='postmortem')
    doctor                 = models.ForeignKey(Doctor, on_delete=models.PROTECT, related_name='postmortems')
    inquest_order_date     = models.DateField(null=True, blank=True)
    court_order_date       = models.DateField(null=True, blank=True)
    autopsy_date           = models.DateTimeField()
    autopsy_start_time     = models.TimeField(null=True, blank=True)
    autopsy_end_time       = models.TimeField(null=True, blank=True)
    autopsy_location       = models.CharField(max_length=300, blank=True)
    inquest_number         = models.CharField(max_length=50, blank=True)
    court_order_number     = models.CharField(max_length=50, blank=True)
    external_findings      = models.TextField(blank=True)
    internal_findings      = models.TextField(blank=True)
    organ_findings         = models.TextField(blank=True)
    immediate_cause        = models.CharField(max_length=300, blank=True, verbose_name='Immediate Cause of Death')
    cause_a                = models.CharField(max_length=300, blank=True, verbose_name='Cause A (Due to)')
    cause_b                = models.CharField(max_length=300, blank=True, verbose_name='Cause B (Due to)')
    cause_c                = models.CharField(max_length=300, blank=True, verbose_name='Cause C (Due to)')
    death_type             = models.CharField(max_length=20, choices=DEATH_TYPE_CHOICES)
    estimated_time_of_death = models.DateTimeField(null=True, blank=True)
    audio_recording_path   = models.CharField(max_length=500, blank=True)
    audio_duration_secs    = models.PositiveIntegerField(null=True, blank=True)
    photographs_taken      = models.PositiveSmallIntegerField(default=0)
    photograph_path        = models.CharField(max_length=500, blank=True)
    specimen_collected     = models.BooleanField(default=False)
    specimen_details       = models.TextField(blank=True)
    assistant_names        = models.CharField(max_length=500, blank=True)
    report_status          = models.CharField(max_length=20, choices=REPORT_STATUS_CHOICES, default='Pending')
    created_at             = models.DateTimeField(auto_now_add=True)
    updated_at             = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.postmortem_id:
            count = Postmortem.objects.count() + 1
            self.postmortem_id = f'PM-{count:05d}'
        super().save(*args, **kwargs)

    def __str__(self):
        return f'PM {self.postmortem_id} — {self.get_death_type_display()} — {self.case.case_number}'

    @property
    def death_type_badge(self):
        return {
            self.DEATH_NATURAL:      'badge-success',
            self.DEATH_ACCIDENTAL:   'badge-info',
            self.DEATH_SUICIDAL:     'badge-warning',
            self.DEATH_HOMICIDAL:    'badge-danger',
            self.DEATH_UNDETERMINED: 'badge-secondary',
        }.get(self.death_type, 'badge-secondary')

    class Meta:
        ordering     = ['-autopsy_date']
        verbose_name = 'Postmortem'
