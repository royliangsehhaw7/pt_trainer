from django.db import models

from orm.models import Trainer
from .exercise import Exercise
from .tag import Tag

# Junction table for Tags and Exercises

class ExerciseTag(models.Model):
    exercise = models.ForeignKey(
        Exercise, 
        on_delete=models.CASCADE, 
        related_name="exercise_tags"
    )
    tag = models.ForeignKey(
        Tag, 
        on_delete=models.CASCADE, 
        related_name="tag_exercises"
    )
    
    # # can add additional columns if needed
    # added_at = models.DateTimeField(auto_now_add=True)
    # is_featured = models.BooleanField(default=False)


    class Meta:
        unique_together = ('exercise', 'tag')   # THIS IS A MAST TO ENSURE DATA INTEGRITY
        db_table = 'exercises_tags'

    def __str__(self):
        return f"{self.exercise.name} - {self.tag.name}"