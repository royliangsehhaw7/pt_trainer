from django import forms
from django.forms import inlineformset_factory

from orm.models import Client, Workout, WorkoutExercise

"""
--- https://www.geeksforgeeks.org/python/add-forms-dynamically-in-django-using-formset-and-javascript/
--- https://www.brennantymrak.com/articles/django-dynamic-formsets-javascript
--- https://ianwaldron.com/blog/add-form-to-django-formset-dynamically-with-javascript/
"""


class WorkoutForm(forms.ModelForm):
    client = forms.ModelChoiceField(
        # queryset = Client.objects.all(),
        queryset=Client.objects.none(),        # have to pass in filtered tags based on trainer
        widget= forms.Select(attrs={
            'class': 'form-control',
            'hx-get': '/client/info/',
            'hx-target': '#client-container',
            'hx-trigger': 'change'
        })
    )
    
    # AI: in django form, how could i add a simple select dropdown with range from 1 t 5
    exercise_count = forms.ChoiceField(
        label="No of exercises",
        required=False,
        choices=[{i, str(i)} for i in range(1, 6)],         # needs key value pair (display, value)
        widget= forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Workout
        fields = ['is_completed', 'trainer_review', 'client_remarks', 'client', 'ai_feedback']
        labels = {
            'trainer_review': 'Trainer Review',
            "client_remarks": 'Client Remarks'
        }
        widgets = {
            'trainer_review': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'client_remarks': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'ai_feedback': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'readonly': True})
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
            self.fields['client'].queryset = Client.objects.filter(trainer=trainer)

        
        # when editing, have to disable the client selection
        if self.instance and self.instance.pk:
            self.fields['client'].disabled = True
            # self.fields['client'].initial = self.instance.client
            # self.fields['client'].widget.attrs['readonly'] = True
            # self.fields['client'].required = False
            # self.fields['client'].widget.attrs['class'] = 'form-control-plaintext border-bottom fw-bold'   
            # 

class ExerciseForm(forms.ModelForm):
    class Meta:
        model = WorkoutExercise
        fields = [
            'exercise', 'pre_sets', 'pre_reps', 'pre_weight', 'pre_duration', 
            'actual_sets', 'actual_reps', 'actual_weight', 'actual_duration', 'is_done'
        ]
        widgets = {
            'exercise': forms.Select(attrs={'class': 'form-control'}),
            'actual_sets': forms.NumberInput(attrs={'class': 'form-control'}),
            'actual_reps': forms.NumberInput(attrs={'class': 'form-control'}),
            'actual_weight': forms.NumberInput(attrs={'class': 'form-control'}),
            'actual_duration': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_done': forms.CheckboxInput(attrs={'class': 'form-check-input', 'role': 'switch'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # all the prescribe exercise values are to be marked non editable
        if self.instance and self.instance.pk:
            readonly_fields = ['exercise', 'pre_sets', 'pre_reps', 'pre_weight', 'pre_duration']
            
            for field_name in readonly_fields:
                if field_name in self.fields:
                    self.fields[field_name].disabled = True
                    self.fields[field_name].widget.attrs['readonly'] = True
                    self.fields[field_name].required = False
                    self.fields[field_name].widget.attrs['class'] = 'form-control'



# this is for the empty / new rows
ExerciseFormSet = inlineformset_factory(
    Workout,
    WorkoutExercise,
    form=ExerciseForm,
    extra=0,
    can_delete=True
)