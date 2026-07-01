from django import forms
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Username',
            'autofocus': True,
            'id': 'id_username',
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'Password',
            'id': 'id_password',
        })
    )


class ProfileEditForm(forms.Form):
    """Allow users to update their own name, email, and optionally change password."""

    first_name = forms.CharField(
        max_length=150,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'First name',
            'id': 'id_first_name',
        }),
        label='First Name',
    )
    last_name = forms.CharField(
        max_length=150,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Last name',
            'id': 'id_last_name',
        }),
        label='Last Name',
    )
    email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={
            'class': 'form-input',
            'placeholder': 'Email address',
            'id': 'id_email',
        }),
        label='Email Address',
    )

    # ── Password change (all three required together if any is filled) ────────
    current_password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'Current password',
            'id': 'id_current_password',
            'autocomplete': 'current-password',
        }),
        label='Current Password',
    )
    new_password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'New password (min 8 characters)',
            'id': 'id_new_password',
            'autocomplete': 'new-password',
        }),
        label='New Password',
    )
    confirm_password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'Confirm new password',
            'id': 'id_confirm_password',
            'autocomplete': 'new-password',
        }),
        label='Confirm New Password',
    )

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        if user:
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial  = user.last_name
            self.fields['email'].initial      = user.email

    def clean(self):
        cleaned = super().clean()
        current = cleaned.get('current_password')
        new_pw  = cleaned.get('new_password')
        confirm = cleaned.get('confirm_password')

        # If any password field is touched, validate all three
        if any([current, new_pw, confirm]):
            if not current:
                self.add_error('current_password', 'Enter your current password to change it.')
            elif not self.user.check_password(current):
                self.add_error('current_password', 'Current password is incorrect.')

            if not new_pw:
                self.add_error('new_password', 'Enter a new password.')
            else:
                try:
                    validate_password(new_pw, self.user)
                except ValidationError as e:
                    self.add_error('new_password', list(e.messages))

            if new_pw and confirm and new_pw != confirm:
                self.add_error('confirm_password', 'Passwords do not match.')

        return cleaned
