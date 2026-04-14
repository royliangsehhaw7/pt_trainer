from django.db import models

from .workout import Workout
from .exercise import Exercise

class WorkoutExercise(models.Model):
    workout = models.ForeignKey(
        Workout, 
        on_delete=models.CASCADE, 
        related_name="exercises"
    )
    exercise = models.ForeignKey(
        Exercise,
        on_delete = models.RESTRICT,
        related_name = 'workout_exercises'
    )

    is_done = models.BooleanField(db_default=False)

    # prescribed workout
    pre_sets = models.PositiveIntegerField(
        default=0,
        db_default=0
    )
    pre_reps = models.PositiveIntegerField(
        default=0,
        db_default=0
    )
    pre_weight = models.PositiveIntegerField(
        default=0,
        db_default=0,
        blank=True
    )
    pre_duration = models.PositiveIntegerField(
        default=0,
        db_default=0,
        blank=True
    )

    # actual done
    actual_sets = models.PositiveIntegerField(
        default=0,
        db_default=0,
        blank=True,
        null=True
    )
    actual_reps = models.PositiveIntegerField(
        default=0,
        db_default=0,
        blank=True,
        null=True

    )
    actual_weight = models.PositiveIntegerField(
        default=0,
        db_default=0,
        blank=True,
        null=True
    )
    actual_duration = models.PositiveIntegerField(
        default=0,
        db_default=0,
        blank=True,
        null=True
    )


    class Meta:
        unique_together = ['workout', 'exercise']
        db_table = "workout_exercises"

    def save(self, *args, **kwargs):
        # mnually trigger the validators even if modelform not used
        self.full_clean() 
        super().save(*args, **kwargs)


    def __str__(self):
        return f"{self.id}"