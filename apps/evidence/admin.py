from django.contrib import admin
from .models import Evidence, LaboratoryTest, EvidenceChainOfCustody


class LabTestInline(admin.TabularInline):
    model  = LaboratoryTest
    extra  = 0
    fields = ['test_id', 'test_type', 'test_date', 'test_status']
    readonly_fields = ['test_id']


@admin.register(Evidence)
class EvidenceAdmin(admin.ModelAdmin):
    list_display  = ['evidence_number', 'case', 'evidence_type', 'barcode_number', 'analysis_status', 'disposal_status']
    list_filter   = ['analysis_status', 'disposal_status']
    search_fields = ['evidence_number', 'barcode_number', 'case__case_number']
    ordering      = ['-collection_date']
    readonly_fields = ['evidence_id', 'evidence_number', 'barcode_number', 'created_at', 'updated_at']
    inlines       = [LabTestInline]


@admin.register(LaboratoryTest)
class LaboratoryTestAdmin(admin.ModelAdmin):
    list_display  = ['test_id', 'evidence', 'test_type', 'test_date', 'test_status']
    list_filter   = ['test_status']
    search_fields = ['test_id', 'evidence__evidence_number']
    ordering      = ['-test_date']
    readonly_fields = ['test_id', 'created_at', 'updated_at']


@admin.register(EvidenceChainOfCustody)
class EvidenceChainOfCustodyAdmin(admin.ModelAdmin):
    list_display  = ['custody_id', 'evidence', 'action', 'handled_by', 'action_datetime', 'signature_obtained']
    list_filter   = ['action', 'signature_obtained']
    search_fields = ['custody_id', 'evidence__evidence_number', 'handled_by']
    ordering      = ['-action_datetime']
    readonly_fields = ['custody_id', 'created_at']
