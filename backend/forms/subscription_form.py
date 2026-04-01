from django import forms
from django.contrib.auth.models import Group

from orm.models import UserTrainer as Trainer

class SubscriptionForm(forms.ModelForm):
    first_name = forms.CharField(
        label = "First Name",
        widget = forms.TextInput(attrs={"class": "form-control"})
    )
    last_name = forms.CharField(
        label  = "Last Name",
        widget =forms.TextInput(attrs={"class": "form-control"})
    )
    email = forms.CharField(
        label = "Email",
        widget = forms.TextInput(attrs={"class": "form-control"})
    )
    is_active = forms.BooleanField(
        label = "IsActive",
        required = False,            # must set this, as all boolean fields are marked as required
        widget = forms.CheckboxInput(attrs={"class": "form-check-input"})
    )

    # ===== These two are forms only fields =====
    # DO NOT ADD TO META FIELDS LIST IF NOT IT WILL LOOK FOR FIELDS IN TO MODEL
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    #REF: https://www.guguweb.com/2014/09/10/group-combo-box-django-user-profile-form/
    group = forms.ModelChoiceField(
        queryset=Group.objects.all(), 
        required=True,
        widget = forms.Select(attrs={"class": "form-control"})
    )

    class Meta:
        model = Trainer
        fields = ["email", "first_name", "last_name", "group", "is_active"]
        labels ={
            "password":"Password",
            # "confirm-password": "Confirm Password"
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match")
        
        return cleaned_data
