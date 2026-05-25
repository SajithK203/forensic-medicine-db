from django.contrib import admin
from .models import CourtReport


@admin.register(CourtReport)
class CourtReportAdmin(admin.ModelAdmin):
    list_display  = ['report_id', 'case', 'report_type', 'report_status', 'doctor', 'generated_at', 'submitted_at']
    list_filter   = ['report_type', 'report_status']
    search_fields = ['report_id', 'case__case_number', 'court_name']
    ordering      = ['-generated_at']
    readonly_fields = ['report_id', 'created_at', 'updated_at']
