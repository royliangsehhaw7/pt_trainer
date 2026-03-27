from django import forms
from django.forms import inlineformset_factory

from orm.models import Workout, WorkoutExercise

class WorkoutForm(forms.ModelForm):
    trainer_review = forms.CharField(
        label = "Trainer Review",
        required = False,
        widget= forms.Textarea(attrs = {'class': 'form-control', 'rows': 3})
    )
    client_remarks = forms.CharField(
        label = "Trainer Review",
        required = False,
        widget= forms.Textarea(attrs = {'class': 'form-control', 'rows': 3})
    )


    class Meta:
        model = Workout
        fields = ['client', 'scheduled_date', 'is_completed', 'trainer_review', 'client_remarks']
        widgets = {
            'client': forms.Select(attrs={'class': 'form-control'}),
            'scheduled_date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            # 'trainer_review': forms.Textarea(attrs={'class': 'form-control'}),
            # 'client_remarks': forms.Textarea(attrs={'class': 'form-control'}),
        }

ExerciseFormSet = inlineformset_factory(
    Workout,
    WorkoutExercise,
    fields=(
        'exercise',
        'pre_sets', 'pre_reps', 'pre_weight', 'pre_duration', 
        'actual_sets', 'actual_reps', 'actual_weight', 'actual_duration',
        'is_done', 
    ),
    widgets={
        'exercise': forms.Select(attrs={
            'class': 'form-control',
            'style': 'pointer-events: none; background-color: gray;',
            'tabindex': '-1'
        }),
        'pre_sets': forms.NumberInput(attrs={'class': 'form-control', 'value': '0'}),
        'pre_reps': forms.NumberInput(attrs={'class': 'form-control', 'value': '0'}),
        'pre_weight': forms.NumberInput(attrs={'class': 'form-control', 'value': '0'}),
        'pre_duration': forms.NumberInput(attrs={'class': 'form-control', 'value': '0'}),
        'actual_sets': forms.NumberInput(attrs={'class': 'form-control', 'value': '0'}),
        'actual_reps': forms.NumberInput(attrs={'class': 'form-control', 'value': '0'}),
        'actual_weight': forms.NumberInput(attrs={'class': 'form-control', 'value': '0'}),
        'actual_duration': forms.NumberInput(attrs={'class': 'form-control', 'value': '0'}),
        'is_done': forms.CheckboxInput(attrs={'class': 'form-check-input', 'value': '0'}),
    },
    extra=0,
    min_num=0,
    validate_min=True,   
    can_delete=True
)