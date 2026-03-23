from django.db import models

from orm.models import UserTrainer as Trainer
from .client import Client

class Workout(models.Model):
    trainer = models.ForeignKey(
        Trainer,
        on_delete = models.CASCADE,
        related_name = 'workouts'
    )
    client = models.ForeignKey(
        Client,
        on_delete = models.CASCADE,
        related_name = "workouts"
    )

    scheduled_date = models.DateTimeField(null = True, blank = True)
    is_completed = models.BooleanField(default=False)

    # using TextField - will generaete TextArea in forms
    # max_length is only for admin forms
    trainer_review = models.TextField(null = True, blank = True)
    client_remarks = models.TextField(null = True, blank = True)

    class Meta:
        db_table = "workouts"

    def __str__(self):
        return f"Workout {self.id} for {self.client}"