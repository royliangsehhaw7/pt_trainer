from django.contrib.auth.models import AbstractUser
from django.db import models

class UserTrainer(AbstractUser):
    # --- abstract user by default has
    # username, password, email, first_name, last_name
    # is_active, is_staff, is_superuser, groups
    # date_joined, last_login

    # will use email as the login instead of username
    email = models.EmailField(
        unique=True
    )

    is_trainer = models.BooleanField(default=False)

    class Meta:
        db_table = "user_trainers"