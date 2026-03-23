from django.db import models
from django.core.validators import MinLengthValidator, EmailValidator

from orm.models import UserTrainer as Trainer

class Client(models.Model):
    trainer = models.ForeignKey(
        Trainer,
        on_delete = models.CASCADE,
        related_name = "clients"
    )

    name = models.CharField(
        max_length=100,
        validators = [MinLengthValidator(6)]
    )
    email = models.CharField(
        max_length = 100,
        validators = [EmailValidator()]
    )

    goals = models.TextField()                              # this is a TEXT (up to 4GB) in database, NOT varchar   
    preferred_times = models.CharField(max_length=150)

    class Meta:
        unique_together = ['trainer','email']               # one client cannot register more than once per trainer
                                                            # but can register with another trainer
        db_table = "clients"

    def __str__(self):
        return self.name
    