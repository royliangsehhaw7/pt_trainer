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
            'scheduled_date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'client': forms.Select(attrs={'class': 'form-control'}),
            # 'trainer_review': forms.Textarea(attrs={'class': 'form-control'}),
            # 'client_remarks': forms.Textarea(attrs={'class': 'form-control'}),
        }
    
ExerciseFormSet = inlineformset_factory(
    Workout,
    WorkoutExercise,
    fields=(
        'exercise',
        'pre_sets', 
        'pre_reps', 
        'pre_weight', 
        'pre_duration', 
        'is_done', 
        'actual_sets', 
        'actual_reps', 
        'actual_weight', 
        'actual_duration'
    ),
    widgets={
        'exercise': forms.Select(attrs={'class': 'form-control'}),
        'pre_sets': forms.NumberInput(attrs={'class': 'form-control'}),
        'pre_reps': forms.NumberInput(attrs={'class': 'form-control'}),
        'pre_weight': forms.NumberInput(attrs={'class': 'form-control'}),
        'pre_duration': forms.NumberInput(attrs={'class': 'form-control'}),
        'actual_sets': forms.NumberInput(attrs={'class': 'form-control'}),
        'actual_reps': forms.NumberInput(attrs={'class': 'form-control'}),
        'actual_weight': forms.NumberInput(attrs={'class': 'form-control'}),
        'actual_duration': forms.NumberInput(attrs={'class': 'form-control'}),
        'is_done': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
    },
    extra=0,
    can_delete=True
)