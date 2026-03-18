from django import forms
from django.core.validators import MinLengthValidator, MinValueValidator
from orm.models import Exercise, Tag

class ExerciseForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.none(),  # will set dynamically in __init__
        widget=forms.CheckboxSelectMultiple()
        # widget=forms.CheckboxSelectMultiple(attrs={"class": "btn-check"})
    )

    def_sets = forms.IntegerField(
        label="Number of Sets",
        validators=[MinValueValidator(0)],
        # widgets will add the element attributes
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "min": 0,
            "max": 100,
            "type" :"number",
        })
    )
    def_reps = forms.IntegerField(
        label="Number of Sets",
        validators=[MinValueValidator(10)],
        # widgets will add the element attributes
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "min": 0,
            "max": 100,
            "type" :"number",
            "required": True
        })
    )    
    def_weight = forms.IntegerField(
        label="Number of Sets",
        validators=[MinValueValidator(10)],
        # widgets will add the element attributes
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "min": 0,
            "max": 100,
            "type" :"number",
            "required": True
        })
    )
    def_duration = forms.IntegerField(
        label="Number of Sets",
        validators=[MinValueValidator(10)],
        # widgets will add the element attributes
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "min": 0,
            "max": 100,
            "type" :"number",
            "required": True
        })
    )        


    # option 1
    # name = forms.TextInput(attrs={"class": "form-control", "placeholder": "Exercise name"})

    class Meta:
        model = Exercise
        fields = ["name", "instructions", "def_sets", "def_reps", "def_weight", "def_duration", "tags"]
        widgets = {
            # option 2
            "name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Exercise Name"}
            ),
            "instructions": forms.Textarea(
                attrs={"class": "form-control", "rows": 3, "placeholder": "Instructions"}
            ),
        }

    def __init__(self, *args, **kwargs):
        # **kwargs = {'instance': instance, 'trainer': trainer'} from the views for edit/add

        # have to remote this trainer from **kwargs
        # we use this trainer to filter exercises for this trainer only (Saas)
        trainer = kwargs.pop("trainer", None)
        # when calling superclass/parent, **kwargs can be only one item
        # we have remove the trainer from **kwargs using pop above
        super().__init__(*args, **kwargs)

        if trainer:
            # this will create a list of tags when used in the template
            self.fields['tags'].queryset = Tag.objects.filter(trainer=trainer)



        # # Apply Bootstrap invalid class automatically
        # for field_name, field in self.fields.items():
        #     if self.errors.get(field_name):
        #         existing = field.widget.attrs.get("class", "")
        #         field.widget.attrs["class"] = (existing + " is-invalid").strip()