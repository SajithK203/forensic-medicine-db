from django.contrib import admin
from .models import ForensicCase


@admin.register(ForensicCase)
class ForensicCaseAdmin(admin.ModelAdmin):
    list_display  = ['case_number', 'patient', 'doctor', 'case_type', 'case_status', 'priority', 'incident_date']
    list_filter   = ['case_type', 'case_status', 'priority']
    search_fields = ['case_number', 'patient__full_name', 'police_report_no']
    ordering      = ['-created_at']
    readonly_fields = ['case_id', 'case_number', 'created_at', 'updated_at']
