from django.contrib import admin
from .models import Patient


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display  = ['patient_id', 'full_name', 'nic_passport', 'gender', 'district', 'registered_at']
    list_filter   = ['gender', 'district', 'civil_status']
    search_fields = ['patient_id', 'full_name', 'nic_passport']
    ordering      = ['-registered_at']
    readonly_fields = ['patient_id', 'registered_at', 'updated_at']
