from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, MinLengthValidator, MaxLengthValidator
from .trainer import Trainer

class Exercise(models.Model):
    name = models.CharField(
        max_length=100,
        # verbose_name = "Exercise Name",      # this is used in the form "label", if not specified there
        # default = "default value"
        # blank = True,
        # null = True,
        # help_text = "Help for Exercise Name"    # Adds a small sub-label or hint below the input field

        # we can add servre side validation model ONLY validation, nothing to do with db
        validators = [MinLengthValidator(10), MaxLengthValidator(100)]
    )
    instructions = models.TextField(
        max_length=100,
        # same options as above,

        # we can add servre side validation model ONLY validation, nothing to do with db
        validators = [MinLengthValidator(10), MaxLengthValidator(100)]
    )

    def_sets  = models.IntegerField(
        default=0,
        # same as above

        # we can add servre side validation model ONLY validation, nothing to do with db
        validators = [MinValueValidator(0), MaxValueValidator(100)]        
    )
    def_reps = models.IntegerField(
        default=0
    )
    def_weight = models.IntegerField(
        default=0,
        help_text = "in Kgs"    # Adds a small sub-label or hint below the input field
    )
    def_duration = models.IntegerField(
        default=0,
        help_text = "in Minutes"    # Adds a small sub-label or hint below the input field
    )
    

    # saas requirement - tenant
    trainer = models.ForeignKey(
        Trainer, 
        on_delete=models.CASCADE, 
        related_name='exercises'
    )
    # Note: No ManyToManyField here because you want manual control

    class Meta:
        db_table = 'exercises'

    def save(self, *args, **kwargs):
        # Professional Tip: Manually trigger the validators 
        # to ensure they run even if you aren't using a ModelForm.
        self.full_clean() 
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}"




# DJANGO MANYTOMANY
# from django.db import models
# from .tag import Tag
# from .trainer import Trainer

# class Exercise(models.Model):
#     trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE, related_name='exercises')
#     name = models.CharField(max_length=100)
#     description = models.TextField() 

#     tags = models.ManyToManyField(Tag, related_name='exercises_set')

#     def __str__(self):
#         return self.name