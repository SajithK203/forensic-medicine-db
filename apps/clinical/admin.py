from django.contrib import admin
from .models import ClinicalExamination, Appointment


@admin.register(ClinicalExamination)
class ClinicalExaminationAdmin(admin.ModelAdmin):
    list_display  = ['exam_id', 'case', 'doctor', 'examination_date', 'consciousness']
    list_filter   = ['consciousness', 'investigation_required', 'referral_required']
    search_fields = ['exam_id', 'case__case_number']
    ordering      = ['-examination_date']
    readonly_fields = ['exam_id', 'created_at', 'updated_at']


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display  = ['appointment_id', 'case', 'doctor', 'appointment_type', 'scheduled_date', 'status']
    list_filter   = ['appointment_type', 'status']
    search_fields = ['appointment_id', 'case__case_number', 'doctor__full_name']
    ordering      = ['-scheduled_date']
    readonly_fields = ['appointment_id', 'created_at', 'updated_at']
