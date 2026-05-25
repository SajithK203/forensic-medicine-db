from django.contrib import admin
from .models import Postmortem


@admin.register(Postmortem)
class PostmortemAdmin(admin.ModelAdmin):
    list_display  = ['postmortem_id', 'case', 'doctor', 'autopsy_date', 'death_type', 'report_status']
    list_filter   = ['death_type', 'report_status']
    search_fields = ['postmortem_id', 'case__case_number']
    ordering      = ['-autopsy_date']
    readonly_fields = ['postmortem_id', 'created_at', 'updated_at']
