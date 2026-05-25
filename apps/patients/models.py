from django.db import models


class Patient(models.Model):
    GENDER_CHOICES = [
        ('Male',    'Male'),
        ('Female',  'Female'),
        ('Other',   'Other'),
        ('Unknown', 'Unknown'),
    ]
    CIVIL_CHOICES = [
        ('Single',   'Single'),
        ('Married',  'Married'),
        ('Divorced', 'Divorced'),
        ('Widowed',  'Widowed'),
        ('Unknown',  'Unknown'),
    ]

    patient_id             = models.CharField(max_length=15, primary_key=True, editable=False)
    full_name              = models.CharField(max_length=100)
    nic_passport           = models.CharField(max_length=20, unique=True, verbose_name='NIC / Passport')
    date_of_birth          = models.DateField(null=True, blank=True)
    age                    = models.PositiveSmallIntegerField(null=True, blank=True)
    gender                 = models.CharField(max_length=10, choices=GENDER_CHOICES)
    address                = models.CharField(max_length=300, blank=True)
    district               = models.CharField(max_length=50, blank=True)
    contact_no             = models.CharField(max_length=15, blank=True)
    emergency_contact_name = models.CharField(max_length=100, blank=True)
    emergency_contact_no   = models.CharField(max_length=15, blank=True)
    photograph             = models.ImageField(upload_to='patients/photos/', null=True, blank=True)
    civil_status           = models.CharField(max_length=20, choices=CIVIL_CHOICES, blank=True)
    occupation             = models.CharField(max_length=100, blank=True)
    notes                  = models.TextField(blank=True)
    registered_at          = models.DateTimeField(auto_now_add=True)
    updated_at             = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.patient_id:
            count = Patient.objects.count() + 1
            self.patient_id = f'PAT-{count:04d}'
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.full_name} ({self.patient_id})'

    @property
    def total_cases(self):
        return self.cases.count()

    class Meta:
        ordering = ['-registered_at']
