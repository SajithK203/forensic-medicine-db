from django.contrib import admin
from .models import ActivityLog


@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display  = ['logged_at', 'username', 'action_type', 'model_name', 'record_id', 'ip_address']
    list_filter   = ['action_type', 'model_name']
    search_fields = ['username', 'record_id', 'action_details']
    ordering      = ['-logged_at']
    readonly_fields = [f.name for f in ActivityLog._meta.fields]  # All fields read-only

    def has_add_permission(self, request):      return False
    def has_change_permission(self, request, obj=None): return False
    def has_delete_permission(self, request, obj=None): return request.user.is_superuser
