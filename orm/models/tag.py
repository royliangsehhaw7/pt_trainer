from django.db import models
from django.core.validators import MinLengthValidator, MaxLengthValidator

from orm.models import UserTrainer as Trainer

class Tag(models.Model):
    name = models.CharField(
        max_length=50,
        # other options
        # default = "default value"
        # unique = True,
        # blank = True,
        # null = True,
        # help_text = "Help for Exercise Name"    # Adds a small sub-label or hint below the input field

        # we can add servre side validation model ONLY validation, nothing to do with db
        validators = [MinLengthValidator(4), MaxLengthValidator(50)]
    )
    
    # saas requirement - tenant
    trainer = models.ForeignKey(
        Trainer, 
        on_delete=models.CASCADE,   # but again, tags still has a CASCADE rule from the exercises
        related_name='tags'
    ) 
    
    class Meta:
        db_table = "tags"

    #***** WARNING - THIS IS A MUST ********** #
    # IF NOT THE EXERCISES ARE NOT PYHSICALLY DELETE FROM THE DATABASE *
    def delete(self, *args, **kwargs):
        self.exercises.all().clear() # I dont understand why we have to do this to physically delete from the database
        super().delete(*args, **kwargs)    

    def save(self, *args, **kwargs):
        # mnually trigger the validators to ensure they run even if modelform not used
        self.full_clean() 
        super().save(*args, **kwargs)        

    def __str__(self):
        return self.name
