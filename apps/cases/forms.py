from django import forms
from .models import ForensicCase
from apps.patients.models import Patient
from apps.staff.models    import Doctor


class CaseForm(forms.ModelForm):
    class Meta:
        model  = ForensicCase
        fields = ['patient','doctor','case_type','incident_date','incident_location',
                  'incident_type','police_report_no','court_case_no','priority','case_notes']
        widgets = {
            'patient':          forms.Select(attrs={'class':'form-select'}),
            'doctor':           forms.Select(attrs={'class':'form-select'}),
            'case_type':        forms.Select(attrs={'class':'form-select'}),
            'incident_date':    forms.DateTimeInput(attrs={'class':'form-input','type':'datetime-local'}),
            'incident_location':forms.TextInput(attrs={'class':'form-input','placeholder':'Location of incident'}),
            'incident_type':    forms.TextInput(attrs={'class':'form-input','placeholder':'e.g. Road accident, Assault'}),
            'police_report_no': forms.TextInput(attrs={'class':'form-input'}),
            'court_case_no':    forms.TextInput(attrs={'class':'form-input'}),
            'priority':         forms.Select(attrs={'class':'form-select'}),
            'case_notes':       forms.Textarea(attrs={'class':'form-input','rows':3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['doctor'].queryset = Doctor.objects.filter(is_active=True)


class CaseStatusForm(forms.ModelForm):
    class Meta:
        model  = ForensicCase
        fields = ['case_status']
        widgets = {'case_status': forms.Select(attrs={'class':'form-select'})}
