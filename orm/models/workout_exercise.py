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
        on_delete = models.CASCADE,
        related_name = 'workout_exercises'
    )

    is_done = models.BooleanField(db_default=False)

    # prescribed
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

    # actual
    actual_sets = models.PositiveIntegerField(
        default=0,
        db_default=0,
        blank=True
    )
    actual_reps = models.PositiveIntegerField(
        default=0,
        db_default=0,
        blank=True
    )
    actual_weight = models.PositiveIntegerField(
        default=0,
        db_default=0,
        blank=True
    )
    actual_duration = models.PositiveIntegerField(
        default=0,
        db_default=0,
        blank=True
    )


    class Meta:
        unique_together = ['workout', 'exercise']
        db_table = "workout_exercises"


    def __str__(self):
        return f"{self.id}"