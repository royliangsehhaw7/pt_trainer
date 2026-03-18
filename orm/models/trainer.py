from django.db import models

class Trainer(models.Model):
    name = models.CharField(
        max_length=100
    )
    email = models.EmailField(
        unique=True
    )
    contact_number = models.CharField(
        max_length=20, 
        blank=True,
        null=True
    )

    class Meta:
        db_table = "trainers"

    def __str__(self):
        return self.name
