from django import forms
from orm.models import Appointment, Client

class AppointmentForm(forms.ModelForm):
    client = forms.ModelChoiceField(
        queryset = Client.objects.none(),
        widget = forms.Select(attrs={"class":"form-select"})
    )

    class Meta:
        model = Appointment
        fields = ['client', 'scheduled_date', 'scheduled_time']
        widgets = {
            # 'clients': forms.Select(attrs={'class': 'form-select'}),
            'scheduled_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}), # normal html date picker
            'scheduled_time': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
                # have to remote this trainer from **kwargs
        # we use this trainer to filter exercises for this trainer only (Saas)
        trainer_clients = kwargs.pop("trainer_clients", None)
        # when calling superclass/parent, **kwargs can be only one item
        # we have remove the trainer from **kwargs using pop above
        super().__init__(*args, **kwargs)

        if trainer_clients:
            self.fields['client'].queryset = trainer_clients
