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
    age = forms.IntegerField(
        label="Age",
        widget=forms.NumberInput(attrs={"class": "form-control"})
    )
    height = forms.DecimalField(
        label="Height",
        widget=forms.NumberInput(attrs={"class": "form-control"})
    )    
    weight = forms.DecimalField(
        label="Weight",
        widget=forms.NumberInput(attrs={"class": "form-control"})
    )
    goals = forms.CharField(
        label="Goals",
        widget=forms.Textarea(attrs={"class":"form-control", "rows": 3})
    )
    preferred_times = forms.CharField(
        label = "Preferred Times",
        widget= forms.Textarea(attrs={"class":"form-control", "rows": 2})
    )

    class Meta:
        model = Client
        fields=["name","email","age","weight","height","goals","preferred_times"]