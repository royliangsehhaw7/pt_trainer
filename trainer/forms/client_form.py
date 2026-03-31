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
        label="Name",
        widget=forms.TextInput(attrs={"class":"form-control"})
    )
    email = forms.CharField(
        label="Email",
        widget=forms.EmailInput(attrs={"class":"form-control"})
    )
    age = forms.IntegerField(
        label="Age",
        widget=forms.NumberInput(attrs={"class": "form-control", "value": "10"})
    )
    height = forms.DecimalField(
        label="Height (m)",
        widget=forms.NumberInput(attrs={"class": "form-control", "value": "0"})
    )    
    weight = forms.DecimalField(
        label="Weight (kg)",
        widget=forms.NumberInput(attrs={"class": "form-control", "value": "0"})
    )
    goals = forms.CharField(
        label="Goals",
        widget=forms.Textarea(attrs={"class":"form-control", "rows": 3})
    )
    preferred_times = forms.ChoiceField(
        choices = Client.PREFERRED_TIMES,
        widget = forms.Select(attrs={"class":"form-control"})
    )

    # preferred_times = forms.CharField(
    #     label = "Preferred Times",
    #     widget= forms.Textarea(attrs={"class":"form-control", "rows": 2})
    # )

    class Meta:
        model = Client
        fields=["name","email","age","weight","height","goals","preferred_times"]