from django.forms import form

from orm.models import UserTrainer

class AccountForm(form.FormModel):
    class Meta:
        model = UserTrainer
        fields = ["__all__"]
