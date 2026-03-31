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
        # help_text = "Help for Exercise Name"    # if needed, can display on form later

        # this validators are onyl model level validation, nothing to do with db
        validators = [MinLengthValidator(4), MaxLengthValidator(50)]
    )
    
    # saas requirement - tenant
    trainer = models.ForeignKey(
        Trainer, 
        on_delete=models.RESTRICT,      # no deletion of trainer if tags still exists (DB and model)
                                        # PROTECT only for django model checks
        related_name='tags'
    ) 
    
    class Meta:
        db_table = "tags"


    def save(self, *args, **kwargs):
        # mnually trigger the validators when modelform not used
        self.full_clean() 
        super().save(*args, **kwargs)        

    def __str__(self):
        return self.name
