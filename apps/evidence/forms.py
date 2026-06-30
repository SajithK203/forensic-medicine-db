from django import forms
from .models import Evidence, LaboratoryTest
from apps.staff.models import Staff


class EvidenceForm(forms.ModelForm):
    class Meta:
        model  = Evidence
        fields = ['case', 'evidence_type', 'evidence_description', 'collection_date',
                  'collected_by', 'storage_location', 'storage_temperature',
                  'storage_conditions', 'analysis_type', 'remarks']
        widgets = {
            'case':                  forms.Select(attrs={'class': 'form-select'}),
            'evidence_type':         forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g. Blood sample, Clothing, Swab'}),
            'evidence_description':  forms.Textarea(attrs={'class': 'form-input', 'rows': 3}),
            'collection_date':       forms.DateTimeInput(attrs={'class': 'form-input', 'type': 'datetime-local'}),
            'collected_by':          forms.TextInput(attrs={'class': 'form-input'}),
            'storage_location':      forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Room / Shelf / Freezer ID'}),
            'storage_temperature':   forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g. -20°C, 4°C, Room temp'}),
            'storage_conditions':    forms.TextInput(attrs={'class': 'form-input'}),
            'analysis_type':         forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g. DNA, Toxicology, Histology'}),
            'remarks':               forms.Textarea(attrs={'class': 'form-input', 'rows': 2}),
        }


# ── Used when CREATING a new lab test (Doctor/Admin assigns test) ──────────────
class LabTestCreateForm(forms.ModelForm):
    """Only the fields needed to open/request a lab test."""
    class Meta:
        model  = LaboratoryTest
        fields = ['evidence', 'technician', 'test_type', 'test_description',
                  'test_date', 'requested_by', 'test_notes']
        widgets = {
            'evidence':         forms.Select(attrs={'class': 'form-select'}),
            'technician':       forms.Select(attrs={'class': 'form-select'}),
            'test_type':        forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g. PCR, DNA Profiling, Toxicology Screen'}),
            'test_description': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Brief description of what to test'}),
            'test_date':        forms.DateTimeInput(attrs={'class': 'form-input', 'type': 'datetime-local'}),
            'requested_by':     forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Doctor / JMO name'}),
            'test_notes':       forms.Textarea(attrs={'class': 'form-input', 'rows': 2, 'placeholder': 'Any special instructions for the lab'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['technician'].queryset = Staff.objects.filter(staff_type='Laboratory', is_active=True)
        self.fields['technician'].required = False


# ── Used when ENTERING RESULTS (Lab Technician fills this in) ─────────────────
class LabTestResultForm(forms.ModelForm):
    """Fields the lab technician fills in after running the test."""
    class Meta:
        model  = LaboratoryTest
        fields = ['test_status', 'completion_date', 'test_result',
                  'result_interpretation', 'reference_number', 'test_notes']
        widgets = {
            'test_status':           forms.Select(attrs={'class': 'form-select'}),
            'completion_date':       forms.DateTimeInput(attrs={'class': 'form-input', 'type': 'datetime-local'}),
            'test_result':           forms.Textarea(attrs={'class': 'form-input', 'rows': 4,
                                     'placeholder': 'e.g. Blood Alcohol: 0.08 mg/L\nDNA profile: Matched reference sample XYZ'}),
            'result_interpretation': forms.Textarea(attrs={'class': 'form-input', 'rows': 3,
                                     'placeholder': 'e.g. Result is consistent with intoxication at time of incident.'}),
            'reference_number':      forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Lab reference / accession number'}),
            'test_notes':            forms.Textarea(attrs={'class': 'form-input', 'rows': 2,
                                     'placeholder': 'Any additional notes or observations'}),
        }


# ── Backward-compat alias (used in views for edit) ───────────────────────────
LabTestForm = LabTestCreateForm
