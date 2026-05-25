from django import forms
from .models import ClinicalExamination
from apps.cases.models import ForensicCase
from apps.staff.models import Doctor

class ClinicalExaminationForm(forms.ModelForm):
    class Meta:
        model  = ClinicalExamination
        fields = ['case','doctor','examination_date','examination_type','time_of_examination',
                  'general_condition','consciousness','nutritional_status','photographs_taken',
                  'injury_details','wound_description','examination_findings','causative_weapon',
                  'investigation_required','investigation_type','referral_required',
                  'referral_department','referral_reason','officer_notes']
        widgets = {
            'case':                  forms.Select(attrs={'class':'form-select'}),
            'doctor':                forms.Select(attrs={'class':'form-select'}),
            'examination_date':      forms.DateTimeInput(attrs={'class':'form-input','type':'datetime-local'}),
            'examination_type':      forms.TextInput(attrs={'class':'form-input'}),
            'time_of_examination':   forms.TimeInput(attrs={'class':'form-input','type':'time'}),
            'general_condition':     forms.TextInput(attrs={'class':'form-input'}),
            'consciousness':         forms.Select(attrs={'class':'form-select'}),
            'nutritional_status':    forms.TextInput(attrs={'class':'form-input'}),
            'photographs_taken':     forms.NumberInput(attrs={'class':'form-input','min':0}),
            'injury_details':        forms.Textarea(attrs={'class':'form-input','rows':4}),
            'wound_description':     forms.Textarea(attrs={'class':'form-input','rows':3}),
            'examination_findings':  forms.Textarea(attrs={'class':'form-input','rows':5}),
            'causative_weapon':      forms.TextInput(attrs={'class':'form-input'}),
            'investigation_type':    forms.TextInput(attrs={'class':'form-input'}),
            'referral_department':   forms.TextInput(attrs={'class':'form-input'}),
            'referral_reason':       forms.TextInput(attrs={'class':'form-input'}),
            'officer_notes':         forms.Textarea(attrs={'class':'form-input','rows':3}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['doctor'].queryset = Doctor.objects.filter(is_active=True)
