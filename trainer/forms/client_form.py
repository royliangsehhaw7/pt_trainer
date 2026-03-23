from django import forms
from orm.models import Client


class ClientForm(forms.ModelForm):
    # --- option 1
    # class Meta:
    #     model = Client
    #     fields = ['name', 'email']
    #     labels = {
    #         "name":"XXXXXXXXXX",
    #         "email":"YYYYYYYYY"
    #     }
    #     widgets = {
    #         "name": forms.TextInput(
    #             attrs={"class": "form-control", "placeholder": "Client's Name"}
    #         ),
    #         "email": forms.EmailInput(
    #             attrs={"class": "form-control", "placeholder": "Client's Email"}
    #         ),
    #     }

    # --- option 2
    name = forms.CharField(
        label="C Name",
        widget=forms.TextInput(attrs={"class":"form-control", "placeholder":"placeholder for name"})
    )
    email = forms.CharField(
        label="C Email",
        widget=forms.EmailInput(attrs={"class":"form-control", "placeholder":"placeholder for email"})
    )

    class Meta:
        model = Client
        fields=["name","email"]