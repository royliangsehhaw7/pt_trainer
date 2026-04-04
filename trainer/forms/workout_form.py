from django import forms
from django.forms import inlineformset_factory
from orm.models import Workout, WorkoutExercise


class WorkoutForm(forms.ModelForm):
    class Meta:
        model = Workout
        fields = ['client', 'is_completed', 'trainer_review', 'client_remarks']
        widgets = {
            'client': forms.Select(attrs={'class': 'form-control'}),
            'trainer_review': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'client_remarks': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        if self.instance and self.instance.pk:
            # self.fields['client'].disabled = True
            # self.fields['client'].initial = self.instance.client
            self.fields['client'].widget.attrs['readonly'] = True
            self.fields['client'].required = False
            self.fields['client'].widget.attrs['class'] = 'form-control-plaintext border-bottom fw-bold'            


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
        
        # LOCKDOWN LOGIC: These fields are now un-editable by the trainer
        if self.instance and self.instance.pk:
            readonly_fields = ['exercise', 'pre_sets', 'pre_reps', 'pre_weight', 'pre_duration']
            
            for field_name in readonly_fields:
                if field_name in self.fields:
                    # self.fields[field_name].disabled = True
                    self.fields[field_name].widget.attrs['readonly'] = True
                    self.fields[field_name].required = False
                    self.fields[field_name].widget.attrs['class'] = 'form-control-plaintext border-bottom fw-bold'


# The Factory MUST use the ExerciseForm class defined above
ExerciseFormSet = inlineformset_factory(
    Workout,
    WorkoutExercise,
    form=ExerciseForm,
    extra=0,
    can_delete=True
)