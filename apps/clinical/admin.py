from django.contrib import admin
from .models import ClinicalExamination


@admin.register(ClinicalExamination)
class ClinicalExaminationAdmin(admin.ModelAdmin):
    list_display  = ['exam_id', 'case', 'doctor', 'examination_date', 'consciousness']
    list_filter   = ['consciousness', 'investigation_required', 'referral_required']
    search_fields = ['exam_id', 'case__case_number']
    ordering      = ['-examination_date']
    readonly_fields = ['exam_id', 'created_at', 'updated_at']
