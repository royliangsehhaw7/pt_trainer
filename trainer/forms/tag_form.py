from django import forms
from django.core.validators import MinLengthValidator
from orm.models import Tag


class TagForm(forms.ModelForm):
    name = forms.CharField(
        label="Tag Name",
        validators=[MinLengthValidator(10)],
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "maxlength": 80,
            "required": True
        })
    )

    class Meta:
        model = Tag
        fields = ["name"]