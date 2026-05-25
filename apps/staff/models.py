from django.db import models
import uuid


def _next_id(prefix, model):
    """Generate next sequential ID: PREFIX-XXXX"""
    count = model.objects.count() + 1
    return f'{prefix}-{count:04d}'


# ── Staff ──────────────────────────────────────────────────────────────────────
class Staff(models.Model):
    TYPE_DOCTOR = 'Doctor'
    TYPE_LAB    = 'Laboratory'
    TYPE_ADMIN  = 'Administrative'
    TYPE_CLERK  = 'Clerical'

    TYPE_CHOICES = [
        (TYPE_DOCTOR, 'Doctor'),
        (TYPE_LAB,    'Laboratory'),
        (TYPE_ADMIN,  'Administrative'),
        (TYPE_CLERK,  'Clerical'),
    ]

    staff_id    = models.CharField(max_length=15, primary_key=True, editable=False)
    full_name   = models.CharField(max_length=100)
    staff_type  = models.CharField(max_length=20, choices=TYPE_CHOICES)
    department  = models.CharField(max_length=100, default='Forensic Medicine')
    designation = models.CharField(max_length=100, blank=True)
    contact_no  = models.CharField(max_length=15, blank=True)
    email       = models.EmailField(unique=True, null=True, blank=True)
    join_date   = models.DateField(null=True, blank=True)
    is_active   = models.BooleanField(default=True)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.staff_id:
            self.staff_id = _next_id('STF', Staff)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.full_name} ({self.get_staff_type_display()})'

    class Meta:
        verbose_name_plural = 'Staff'
        ordering = ['full_name']


# ── Doctor ─────────────────────────────────────────────────────────────────────
class Doctor(models.Model):
    JMO_CONSULTANT = 'Consultant JMO'
    JMO_SENIOR     = 'Senior JMO'
    JMO_JUNIOR     = 'Junior JMO'

    JMO_CHOICES = [
        (JMO_CONSULTANT, 'Consultant JMO'),
        (JMO_SENIOR,     'Senior JMO'),
        (JMO_JUNIOR,     'Junior JMO'),
    ]

    doctor_id         = models.CharField(max_length=15, primary_key=True, editable=False)
    staff             = models.OneToOneField(Staff, on_delete=models.SET_NULL, null=True, blank=True,
                                             related_name='doctor_profile')
    full_name         = models.CharField(max_length=100)
    nmc_number        = models.CharField(max_length=20, unique=True)
    qualification     = models.CharField(max_length=100, blank=True)
    specialization    = models.CharField(max_length=100, blank=True)
    jmo_type          = models.CharField(max_length=20, choices=JMO_CHOICES)
    license_number    = models.CharField(max_length=50, unique=True, null=True, blank=True)
    department        = models.CharField(max_length=100, default='Forensic Medicine')
    office_contact_no = models.CharField(max_length=15, blank=True)
    signature_path    = models.ImageField(upload_to='doctors/signatures/', null=True, blank=True)
    is_active         = models.BooleanField(default=True)
    created_at        = models.DateTimeField(auto_now_add=True)
    updated_at        = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.doctor_id:
            self.doctor_id = _next_id('DOC', Doctor)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Dr. {self.full_name} — {self.get_jmo_type_display()}'

    class Meta:
        ordering = ['full_name']
