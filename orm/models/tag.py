from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, MinLengthValidator, MaxLengthValidator

from .trainer import Trainer

class Tag(models.Model):
    name = models.CharField(
        max_length=50,
        # verbose_name = "Exercise Name",      # this is used in the form "label", if not specified there
        # default = "default value"
        # unique = True,
        # blank = True,
        # null = True,
        # help_text = "Help for Exercise Name"    # Adds a small sub-label or hint below the input field

        # we can add servre side validation model ONLY validation, nothing to do with db
        validators = [MinLengthValidator(10), MaxLengthValidator(50)]
    )
    
    # saas requirement - tenant
    trainer = models.ForeignKey(
        Trainer, 
        on_delete=models.CASCADE, 
        related_name='tags'
    ) 
    
    class Meta:
        db_table = "tags"

    def __str__(self):
        return self.name
