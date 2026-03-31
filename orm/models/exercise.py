from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, MinLengthValidator, MaxLengthValidator
from orm.models import UserTrainer as Trainer
from orm.models import Tag

class Exercise(models.Model):
    name = models.CharField(
        max_length=80,
        # verbose_name = "Exercise Name",      # ???
        # default = "default value"
        # blank = True,
        # null = True,
        # help_text = "Help for Exercise Name"    # can display later on form

        # we can add servre side validation model ONLY validation, nothing to do with db
        validators = [MinLengthValidator(4), MaxLengthValidator(100)]
    )
    instructions = models.TextField()

    # ===== default prescribed values by trainer
    def_sets  = models.IntegerField(
        default = 0,
        db_default=0,
        validators = [MinValueValidator(0), MaxValueValidator(100)],            # model only validation
    )
    def_reps = models.IntegerField(
        default = 0,
        db_default=0,
        validators = [MinValueValidator(0), MaxValueValidator(100)],            # model only validation
    )
    def_weight = models.DecimalField(
        default = 0,
        db_default=0,
        max_digits = 5,
        decimal_places = 2,
        validators = [MinValueValidator(0), MaxValueValidator(100)],            # model only validation
        # help_text = "in Kgs" 
    )
    def_duration = models.IntegerField(
        default = 0,
        db_default=0,
        validators = [MinValueValidator(0), MaxValueValidator(100)],            # model only validation
        # help_text = "in Minutes" 
    )
    

    # saas requirement - tenant
    trainer = models.ForeignKey(
        Trainer, 
        on_delete=models.RESTRICT,      # no deletion of trainer if clients still exists (DB and model)
                                        # PROTECT only for django model checks 
        related_name='exercises'
    )

    # =================== M2M (funny behaviour) ===================== #
    # ??????? records delete in django app stil remains in the database ?????????
    # tags = models.ManyToMany(
    #   Tag,
    #   related_name = "tag_exercises",
    #   reverse_related_name = "exercise_tags"
    # )
    # 
    # AI: in django orm, why when using M2m relations, records delete in app still remains in the database
    # ============================================================ #


    class Meta:
        db_table = 'exercises'

    def save(self, *args, **kwargs):
        # mnually trigger the validators when  modelform not used
        self.full_clean() 
        super().save(*args, **kwargs)


    def __str__(self):
        return f"{self.name}"




# DJANGO MANYTOMANY # NOT WORKING
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