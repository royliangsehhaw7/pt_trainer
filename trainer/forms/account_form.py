from django import forms
from django.contrib.auth import get_user_model

UserTrainer = get_user_model()      # will get from settings.py AUTH_USER_MODEL

class AccountForm(forms.ModelForm):
    # this two are only for form input and NOT for updating (eg password must be encrtyped first)
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
        required=False
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}),
        required=False
    )

    class Meta:
        model = UserTrainer
        fields = ['first_name', 'last_name', 'email', 'username']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email / Username'}),
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'})
        }

    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password:
            if password != confirm_password:
                self.add_error('confirm_password', "Passwords do not match")
        
        return cleaned_data