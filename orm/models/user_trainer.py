from django.contrib.auth.models import AbstractUser
from django.db import models

class UserTrainer(AbstractUser):
    # --- abstract user by default has
    # username, 
    # password, 
    # email, 
    # first_name, 
    # last_name
    # is_active, is_staff, is_superuser, groups
    # date_joined, last_login

    is_trainer = models.BooleanField(default=False)

    class Meta:
        db_table = "user_trainers"

    def save(self, *args, **kwargs):
        # mnually trigger the validators to ensure they run even if modelform not used
        self.full_clean() 
        super().save(*args, **kwargs)

    def __str__(self):
        return self.first_name