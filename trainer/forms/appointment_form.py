from django import forms
from orm.models import Appointment

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['client', 'start_date', 'scheduled_time']
        widgets = {
            # Use the HTML5 date picker (no JS needed)
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'client': forms.Select(attrs={'class': 'form-select'}),
            'scheduled_time': forms.Select(attrs={'class': 'form-select'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        # We also set end_date equal to start_date for simple daily slots
        cleaned_data['end_date'] = cleaned_data.get('start_date')
        return cleaned_data