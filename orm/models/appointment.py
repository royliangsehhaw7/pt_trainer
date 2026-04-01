from django.db import models
from orm.models import UserTrainer
from orm.models import Client

class Appointment(models.Model):

    class PREFERRED_TIMES(models.TextChoices):
        MORNING = "Morning", "Morning"
        AFTERNOON = "Afternoon", "Afternoon"
        NIGHT = "Night", "Night"


    trainer = models.ForeignKey(
        UserTrainer,
        on_delete = models.CASCADE,
        related_name = "appointments"
    )

    client = models.ForeignKey(
        Client,
        on_delete = models.CASCADE,
        related_name = "appointments"
    )

    start_date = models.DateField()
    end_date = models.DateField()
    scheduled_time = models.CharField(
        max_length=12,
        choices = PREFERRED_TIMES,
        default = PREFERRED_TIMES.MORNING
    )

    class Meta:
        # ????? workable to ensure no double booking at least for the same client ?????
        # unique_together = ['client_id', 'start_date', 'scheduled_time']
        db_table  = "appointments"


    def clean():
        pass
    def save():
        pass
    def __str__(self):
        return f"Appointment"