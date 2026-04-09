from django.db import models
from orm.models import UserTrainer
from orm.models import Client

class Appointment(models.Model):
    # setup apppointment buckets
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

    scheduled_date = models.DateField()
    scheduled_time = models.CharField(
        max_length=12,
        choices = PREFERRED_TIMES,
        default = PREFERRED_TIMES.MORNING
    )

    class Meta:
        # ????? workable to ensure no double booking ?????
        unique_together = ['trainer', 'scheduled_date', 'scheduled_time']
        db_table  = "appointments"


    ## for future overrding
    def clean(self):
        super().clean()
    
    def save(self, *args, **kwargs):
        # mnually trigger the validators when modelform not used
        self.full_clean() 
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Appointment"