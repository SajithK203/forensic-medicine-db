from django.contrib import admin
from .models import ForensicCase, CaseNote, WitnessStatement


@admin.register(ForensicCase)
class ForensicCaseAdmin(admin.ModelAdmin):
    list_display  = ['case_number', 'patient', 'doctor', 'case_type', 'case_status', 'priority', 'incident_date']
    list_filter   = ['case_type', 'case_status', 'priority']
    search_fields = ['case_number', 'patient__full_name', 'police_report_no']
    ordering      = ['-created_at']
    readonly_fields = ['case_id', 'case_number', 'created_at', 'updated_at']


@admin.register(CaseNote)
class CaseNoteAdmin(admin.ModelAdmin):
    list_display  = ['note_id', 'case', 'author', 'note_type', 'is_private', 'created_at']
    list_filter   = ['note_type', 'is_private']
    search_fields = ['note_id', 'case__case_number', 'author']
    ordering      = ['-created_at']
    readonly_fields = ['note_id', 'created_at', 'updated_at']


@admin.register(WitnessStatement)
class WitnessStatementAdmin(admin.ModelAdmin):
    list_display  = ['statement_id', 'case', 'witness_name', 'statement_type', 'statement_date', 'is_verified']
    list_filter   = ['statement_type', 'is_verified']
    search_fields = ['statement_id', 'case__case_number', 'witness_name', 'witness_nic']
    ordering      = ['-statement_date']
    readonly_fields = ['statement_id', 'created_at', 'updated_at']
