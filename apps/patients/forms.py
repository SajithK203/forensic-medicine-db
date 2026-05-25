from django import forms
from .models import Patient

DISTRICTS = [('', 'All Districts'), ('Colombo','Colombo'), ('Gampaha','Gampaha'),
 ('Kalutara','Kalutara'), ('Kandy','Kandy'), ('Matale','Matale'), ('Nuwara Eliya','Nuwara Eliya'),
 ('Galle','Galle'), ('Matara','Matara'), ('Hambantota','Hambantota'), ('Jaffna','Jaffna'),
 ('Mannar','Mannar'), ('Vavuniya','Vavuniya'), ('Batticaloa','Batticaloa'),
 ('Ampara','Ampara'), ('Trincomalee','Trincomalee'), ('Kurunegala','Kurunegala'),
 ('Puttalam','Puttalam'), ('Anuradhapura','Anuradhapura'), ('Polonnaruwa','Polonnaruwa'),
 ('Badulla','Badulla'), ('Moneragala','Moneragala'), ('Ratnapura','Ratnapura'), ('Kegalle','Kegalle')]

class PatientForm(forms.ModelForm):
    district = forms.ChoiceField(choices=DISTRICTS, required=False)

    class Meta:
        model  = Patient
        fields = ['full_name','nic_passport','date_of_birth','age','gender',
                  'address','district','contact_no','emergency_contact_name',
                  'emergency_contact_no','photograph','civil_status','occupation','notes']
        widgets = {
            'full_name':              forms.TextInput(attrs={'class':'form-input','placeholder':'Full Name'}),
            'nic_passport':           forms.TextInput(attrs={'class':'form-input','placeholder':'NIC or Passport No.'}),
            'date_of_birth':          forms.DateInput(attrs={'class':'form-input','type':'date'}),
            'age':                    forms.NumberInput(attrs={'class':'form-input','min':0,'max':150}),
            'gender':                 forms.Select(attrs={'class':'form-select'}),
            'address':                forms.Textarea(attrs={'class':'form-input','rows':2}),
            'contact_no':             forms.TextInput(attrs={'class':'form-input','placeholder':'+94 XX XXX XXXX'}),
            'emergency_contact_name': forms.TextInput(attrs={'class':'form-input'}),
            'emergency_contact_no':   forms.TextInput(attrs={'class':'form-input','placeholder':'+94 XX XXX XXXX'}),
            'civil_status':           forms.Select(attrs={'class':'form-select'}),
            'occupation':             forms.TextInput(attrs={'class':'form-input'}),
            'notes':                  forms.Textarea(attrs={'class':'form-input','rows':3}),
        }
