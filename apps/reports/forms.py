from django import forms
from .models import CourtReport
from apps.staff.models import Doctor

class CourtReportForm(forms.ModelForm):
    class Meta:
        model  = CourtReport
        fields = ['case','doctor','report_type','report_title','report_content',
                  'report_conclusions','recommended_investigations','court_name',
                  'court_case_number','magistrate_district','judge_name',
                  'lawyer_details','report_status','remarks']
        widgets = {
            'case':                       forms.Select(attrs={'class':'form-select'}),
            'doctor':                     forms.Select(attrs={'class':'form-select'}),
            'report_type':                forms.Select(attrs={'class':'form-select'}),
            'report_title':               forms.TextInput(attrs={'class':'form-input'}),
            'report_content':             forms.Textarea(attrs={'class':'form-input','rows':8}),
            'report_conclusions':         forms.Textarea(attrs={'class':'form-input','rows':4}),
            'recommended_investigations': forms.Textarea(attrs={'class':'form-input','rows':3}),
            'court_name':                 forms.TextInput(attrs={'class':'form-input','placeholder':'e.g. Colombo Magistrate Court'}),
            'court_case_number':          forms.TextInput(attrs={'class':'form-input'}),
            'magistrate_district':        forms.TextInput(attrs={'class':'form-input'}),
            'judge_name':                 forms.TextInput(attrs={'class':'form-input'}),
            'lawyer_details':             forms.TextInput(attrs={'class':'form-input'}),
            'report_status':              forms.Select(attrs={'class':'form-select'}),
            'remarks':                    forms.Textarea(attrs={'class':'form-input','rows':2}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['doctor'].queryset = Doctor.objects.filter(is_active=True)
