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


# ── Notification ──────────────────────────────────────────────────────────────
class Notification(models.Model):
    """System notifications delivered to individual users."""

    TYPE_INFO     = 'Info'
    TYPE_WARNING  = 'Warning'
    TYPE_ALERT    = 'Alert'
    TYPE_SYSTEM   = 'System'

    TYPE_CHOICES = [
        (TYPE_INFO,    'Information'),
        (TYPE_WARNING, 'Warning'),
        (TYPE_ALERT,   'Alert'),
        (TYPE_SYSTEM,  'System'),
    ]

    notification_id = models.AutoField(primary_key=True)
    recipient       = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                        related_name='notifications')
    notification_type = models.CharField(max_length=10, choices=TYPE_CHOICES, default=TYPE_INFO)
    title           = models.CharField(max_length=200)
    message         = models.TextField()
    related_model   = models.CharField(max_length=50, blank=True,
                                       help_text='Name of the model this notification relates to')
    related_id      = models.CharField(max_length=30, blank=True,
                                       help_text='PK of the related record')
    is_read         = models.BooleanField(default=False)
    read_at         = models.DateTimeField(null=True, blank=True)
    created_at      = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'[{self.notification_type}] {self.title} → {self.recipient.username}'

    class Meta:
        ordering = ['-created_at']
        indexes  = [
            models.Index(fields=['recipient', 'is_read']),
            models.Index(fields=['created_at']),
        ]
        verbose_name = 'Notification'

