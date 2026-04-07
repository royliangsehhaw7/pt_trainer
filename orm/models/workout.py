from django.db import models

from orm.models import UserTrainer as Trainer
from .client import Client

class Workout(models.Model):
    trainer = models.ForeignKey(
        Trainer,
        on_delete = models.PROTECT,     # cannot delete trainer if workouts still exists
        related_name = 'workouts'
    )
    client = models.ForeignKey(
        Client,
        on_delete = models.PROTECT,     # cannot delete client if workouts still exists
        related_name = "workouts"
    )
   
    is_completed = models.BooleanField(default=False)

    # using TextField - will generaete TextArea in forms
    # max_length is only for admin forms
    trainer_review = models.TextField(null = True, blank = True)
    client_remarks = models.TextField(null = True, blank = True)

    # possibly to have ai evaluate client workout based
    # preset vs actual activities
    ai_feedback = models.TextField(null = True, blank = True)

    class Meta:
        db_table = "workouts"

    def save(self, *args, **kwargs):
        # mnually trigger the validators when modelform not used
        self.full_clean() 
        super().save(*args, **kwargs)        

    def __str__(self):
        return f"Workout {self.id} for {self.client}"