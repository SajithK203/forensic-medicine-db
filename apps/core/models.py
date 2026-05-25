from django.db import models
from django.conf import settings


class ActivityLog(models.Model):
    ACTION_CHOICES = [
        ('LOGIN',   'Login'),
        ('LOGOUT',  'Logout'),
        ('CREATE',  'Create'),
        ('UPDATE',  'Update'),
        ('DELETE',  'Delete'),
        ('VIEW',    'View'),
        ('EXPORT',  'Export'),
        ('SUBMIT',  'Submit'),
        ('LOCK',    'Lock'),
        ('UNLOCK',  'Unlock'),
    ]

    user          = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
                                      null=True, related_name='activity_logs')
    username      = models.CharField(max_length=50)       # snapshot at log time
    action_type   = models.CharField(max_length=10, choices=ACTION_CHOICES)
    model_name    = models.CharField(max_length=50, blank=True)
    record_id     = models.CharField(max_length=30, blank=True)
    action_details = models.TextField(blank=True)
    ip_address    = models.GenericIPAddressField(null=True, blank=True)
    user_agent    = models.TextField(blank=True)
    logged_at     = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'[{self.logged_at:%Y-%m-%d %H:%M}] {self.username} — {self.action_type} {self.model_name}'

    class Meta:
        ordering = ['-logged_at']
        indexes  = [
            models.Index(fields=['user', 'logged_at']),
            models.Index(fields=['action_type']),
            models.Index(fields=['model_name']),
        ]
