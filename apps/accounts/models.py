from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    ROLE_DOCTOR = 'Doctor'
    ROLE_LAB    = 'LabTechnician'
    ROLE_ADMIN  = 'Administrator'
    ROLE_VIEWER = 'Viewer'

    ROLE_CHOICES = [
        (ROLE_DOCTOR, 'Doctor'),
        (ROLE_LAB,    'Lab Technician'),
        (ROLE_ADMIN,  'Administrator'),
        (ROLE_VIEWER, 'Viewer'),
    ]

    role               = models.CharField(max_length=20, choices=ROLE_CHOICES, default=ROLE_VIEWER)
    login_attempts     = models.PositiveSmallIntegerField(default=0)
    is_locked          = models.BooleanField(default=False)
    must_change_password = models.BooleanField(default=False)
    last_login_ip      = models.GenericIPAddressField(null=True, blank=True)

    # ── Role helpers ──────────────────────────────────────────────────────────
    @property
    def is_doctor(self):        return self.role == self.ROLE_DOCTOR
    @property
    def is_lab_tech(self):      return self.role == self.ROLE_LAB
    @property
    def is_administrator(self): return self.role == self.ROLE_ADMIN
    @property
    def is_viewer(self):        return self.role == self.ROLE_VIEWER

    def get_role_badge(self):
        return {
            self.ROLE_DOCTOR: 'badge-doctor',
            self.ROLE_LAB:    'badge-lab',
            self.ROLE_ADMIN:  'badge-admin',
            self.ROLE_VIEWER: 'badge-viewer',
        }.get(self.role, 'badge-default')

    def get_role_icon(self):
        return {
            self.ROLE_DOCTOR: '🩺',
            self.ROLE_LAB:    '🧪',
            self.ROLE_ADMIN:  '⚙️',
            self.ROLE_VIEWER: '👁️',
        }.get(self.role, '👤')

    class Meta:
        verbose_name        = 'System User'
        verbose_name_plural = 'System Users'

    def __str__(self):
        return f'{self.username} ({self.get_role_display()})'
