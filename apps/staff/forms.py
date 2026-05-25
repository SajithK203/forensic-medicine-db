from django import forms
from .models import Staff, Doctor

class StaffForm(forms.ModelForm):
    class Meta:
        model  = Staff
        fields = ['full_name','staff_type','department','designation','contact_no','email','join_date','is_active']
        widgets = {
            'full_name':   forms.TextInput(attrs={'class':'form-input'}),
            'staff_type':  forms.Select(attrs={'class':'form-select'}),
            'department':  forms.TextInput(attrs={'class':'form-input'}),
            'designation': forms.TextInput(attrs={'class':'form-input'}),
            'contact_no':  forms.TextInput(attrs={'class':'form-input'}),
            'email':       forms.EmailInput(attrs={'class':'form-input'}),
            'join_date':   forms.DateInput(attrs={'class':'form-input','type':'date'}),
        }

class DoctorForm(forms.ModelForm):
    class Meta:
        model  = Doctor
        fields = ['staff','full_name','nmc_number','qualification','specialization',
                  'jmo_type','license_number','office_contact_no','signature_path','is_active']
        widgets = {
            'staff':            forms.Select(attrs={'class':'form-select'}),
            'full_name':        forms.TextInput(attrs={'class':'form-input'}),
            'nmc_number':       forms.TextInput(attrs={'class':'form-input','placeholder':'NMC Registration No.'}),
            'qualification':    forms.TextInput(attrs={'class':'form-input','placeholder':'e.g. MBBS, MD'}),
            'specialization':   forms.TextInput(attrs={'class':'form-input','placeholder':'e.g. Forensic Pathology'}),
            'jmo_type':         forms.Select(attrs={'class':'form-select'}),
            'license_number':   forms.TextInput(attrs={'class':'form-input'}),
            'office_contact_no': forms.TextInput(attrs={'class':'form-input'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['staff'].queryset = Staff.objects.filter(staff_type='Doctor', is_active=True)
