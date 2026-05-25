from django import forms
from .models import Evidence, LaboratoryTest
from apps.staff.models import Staff

class EvidenceForm(forms.ModelForm):
    class Meta:
        model  = Evidence
        fields = ['case','evidence_type','evidence_description','collection_date',
                  'collected_by','storage_location','storage_temperature',
                  'storage_conditions','analysis_type','remarks']
        widgets = {
            'case':                  forms.Select(attrs={'class':'form-select'}),
            'evidence_type':         forms.TextInput(attrs={'class':'form-input','placeholder':'e.g. Blood sample, Clothing'}),
            'evidence_description':  forms.Textarea(attrs={'class':'form-input','rows':3}),
            'collection_date':       forms.DateTimeInput(attrs={'class':'form-input','type':'datetime-local'}),
            'collected_by':          forms.TextInput(attrs={'class':'form-input'}),
            'storage_location':      forms.TextInput(attrs={'class':'form-input','placeholder':'Room / Shelf / Freezer ID'}),
            'storage_temperature':   forms.TextInput(attrs={'class':'form-input','placeholder':'e.g. -20°C, 4°C, Room temp'}),
            'storage_conditions':    forms.TextInput(attrs={'class':'form-input'}),
            'analysis_type':         forms.TextInput(attrs={'class':'form-input','placeholder':'e.g. DNA, Toxicology, Histology'}),
            'remarks':               forms.Textarea(attrs={'class':'form-input','rows':2}),
        }

class LabTestForm(forms.ModelForm):
    class Meta:
        model  = LaboratoryTest
        fields = ['evidence','technician','test_type','test_description','test_date',
                  'requested_by','test_notes']
        widgets = {
            'evidence':         forms.Select(attrs={'class':'form-select'}),
            'technician':       forms.Select(attrs={'class':'form-select'}),
            'test_type':        forms.TextInput(attrs={'class':'form-input','placeholder':'e.g. PCR, Serology, Toxicology'}),
            'test_description': forms.TextInput(attrs={'class':'form-input'}),
            'test_date':        forms.DateTimeInput(attrs={'class':'form-input','type':'datetime-local'}),
            'requested_by':     forms.TextInput(attrs={'class':'form-input'}),
            'test_notes':       forms.Textarea(attrs={'class':'form-input','rows':2}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['technician'].queryset = Staff.objects.filter(staff_type='Laboratory', is_active=True)
