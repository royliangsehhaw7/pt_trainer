from django import forms
from django.core.validators import MinLengthValidator, MinValueValidator
from orm.models import Exercise, Tag

class ExerciseForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        # queryset = Tag.objects.all(),
        queryset=Tag.objects.none(),        # have to pass in filtered tags based on trainer
        # widget=forms.CheckboxSelectMultiple()
        widget=forms.CheckboxSelectMultiple(attrs={"class": "btn-check"})
    )

    # --- these are just default which can be changed when actually create workouts
    def_sets = forms.IntegerField(
        label="Number of Sets",
        initial=0,
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    def_reps = forms.IntegerField(
        label="Number of Sets",
        initial=0,
        widget=forms.TextInput(attrs={"class": "form-control"})
    )    
    def_weight = forms.IntegerField(
        label="Number of Sets",
        initial=0,
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    def_duration = forms.IntegerField(
        label="Number of Sets",
        initial=0,
        widget=forms.TextInput(attrs={"class": "form-control"})
    )        

    class Meta:
        model = Exercise
        fields = ["name", "instructions", "def_sets", "def_reps", "def_weight", "def_duration", "tags"]
        widgets = {
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
        trainer_tags = kwargs.pop("trainer_tags", None)
        # when calling superclass/parent, **kwargs can be only one item
        # we have remove the trainer from **kwargs using pop above
        super().__init__(*args, **kwargs)

        if trainer_tags:
            # this will create a list of tags when used in the template
            self.fields['tags'].queryset = trainer_tags

        # # Apply Bootstrap invalid class automatically
        # for field_name, field in self.fields.items():
        #     if self.errors.get(field_name):
        #         existing = field.widget.attrs.get("class", "")
        #         field.widget.attrs["class"] = (existing + " is-invalid").strip()