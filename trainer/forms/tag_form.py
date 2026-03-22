from django import forms
from orm.models import Tag

class TagForm(forms.ModelForm):
    name = forms.CharField(
        label="Tag Name",
        # widget - more for 'formatting' the gerrate html element
        widget=forms.TextInput(attrs={ "class": "form-control" })
    )

    class Meta:
        model = Tag
        fields = ["name"]
