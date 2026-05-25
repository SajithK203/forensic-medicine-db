from django import forms
from .models import Postmortem
from apps.cases.models import ForensicCase
from apps.staff.models import Doctor

class PostmortemForm(forms.ModelForm):
    class Meta:
        model  = Postmortem
        fields = ['case','doctor','inquest_order_date','court_order_date','autopsy_date',
                  'autopsy_start_time','autopsy_end_time','autopsy_location','inquest_number',
                  'court_order_number','external_findings','internal_findings','organ_findings',
                  'immediate_cause','cause_a','cause_b','cause_c','death_type',
                  'estimated_time_of_death','photographs_taken','specimen_collected',
                  'specimen_details','assistant_names','report_status']
        widgets = {
            'case':                  forms.Select(attrs={'class':'form-select'}),
            'doctor':                forms.Select(attrs={'class':'form-select'}),
            'inquest_order_date':    forms.DateInput(attrs={'class':'form-input','type':'date'}),
            'court_order_date':      forms.DateInput(attrs={'class':'form-input','type':'date'}),
            'autopsy_date':          forms.DateTimeInput(attrs={'class':'form-input','type':'datetime-local'}),
            'autopsy_start_time':    forms.TimeInput(attrs={'class':'form-input','type':'time'}),
            'autopsy_end_time':      forms.TimeInput(attrs={'class':'form-input','type':'time'}),
            'autopsy_location':      forms.TextInput(attrs={'class':'form-input','placeholder':'Mortuary / Hospital'}),
            'inquest_number':        forms.TextInput(attrs={'class':'form-input'}),
            'court_order_number':    forms.TextInput(attrs={'class':'form-input'}),
            'external_findings':     forms.Textarea(attrs={'class':'form-input','rows':4}),
            'internal_findings':     forms.Textarea(attrs={'class':'form-input','rows':4}),
            'organ_findings':        forms.Textarea(attrs={'class':'form-input','rows':3}),
            'immediate_cause':       forms.TextInput(attrs={'class':'form-input','placeholder':'Immediate cause of death'}),
            'cause_a':               forms.TextInput(attrs={'class':'form-input','placeholder':'Due to (a)'}),
            'cause_b':               forms.TextInput(attrs={'class':'form-input','placeholder':'Due to (b)'}),
            'cause_c':               forms.TextInput(attrs={'class':'form-input','placeholder':'Due to (c)'}),
            'death_type':            forms.Select(attrs={'class':'form-select'}),
            'estimated_time_of_death': forms.DateTimeInput(attrs={'class':'form-input','type':'datetime-local'}),
            'photographs_taken':     forms.NumberInput(attrs={'class':'form-input','min':0}),
            'specimen_details':      forms.Textarea(attrs={'class':'form-input','rows':2}),
            'assistant_names':       forms.TextInput(attrs={'class':'form-input'}),
            'report_status':         forms.Select(attrs={'class':'form-select'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['doctor'].queryset = Doctor.objects.filter(is_active=True)
        # Only autopsy cases
        self.fields['case'].queryset = ForensicCase.objects.filter(
            case_type__in=['Autopsy','Clinical & Autopsy'])
