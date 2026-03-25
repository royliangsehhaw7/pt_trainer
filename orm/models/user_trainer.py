from django.contrib.auth.models import AbstractUser
from django.db import models

class UserTrainer(AbstractUser):
    # --- abstract user by default has
    # username, password, email, first_name, last_name
    # is_active, is_staff, is_superuser, groups
    # date_joined, last_login

    is_trainer = models.BooleanField(default=False)

    class Meta:
        db_table = "user_trainers"