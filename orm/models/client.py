from django.db import models
from django.core.validators import MinLengthValidator, MinValueValidator, MaxValueValidator, EmailValidator

from orm.models import UserTrainer as Trainer


class Client(models.Model):
    
    class PREFERRED_TIMES(models.TextChoices):
        MORNING = "Morning", "Morning"
        AFTERNOON = "Afternoon", "Afternoon"
        NIGHT = "Night", "Night"


    trainer = models.ForeignKey(
        Trainer,
        on_delete = models.RESTRICT,    # no deletion of trainer if clients still exists (DB and model)
                                        # PROTECT only for django model checks
        related_name = "clients"
    )

    name = models.CharField(
        max_length=80,
        validators = [MinLengthValidator(6)]
    )
    email = models.CharField(
        max_length = 80,
        validators = [EmailValidator()]
    )

    age = models.PositiveIntegerField(
        validators = [MinValueValidator(10), MaxValueValidator(100)]
    )
    # height - in meters (#.##)
    height = models.DecimalField(
        default = 0,
        db_default = 0,
        max_digits = 3,
        decimal_places = 2,
        validators = [MinValueValidator(1), MaxValueValidator(5)],
    )
    # weight - in kgs (###.##)
    weight = models.DecimalField(
        default = 0,
        db_default = 0,
        max_digits = 5,
        decimal_places = 2,        
        validators = [MinValueValidator(1), MaxValueValidator(100)],
    )

    goals = models.TextField()                              # this is a TEXT (up to 4GB) in database, NOT varchar   
    preferred_times = models.CharField(
        max_length=12,
        choices = PREFERRED_TIMES,
        default = PREFERRED_TIMES.MORNING
    )

    class Meta:
        unique_together = ['trainer','email']               # one client cannot register more than once per trainer
                                                            # but can register with another trainer
        db_table = "clients"
        
    def save(self, *args, **kwargs):
        # mnually trigger the validators even if modelform not used
        self.full_clean() 
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name
    