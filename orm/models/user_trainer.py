from django.contrib.auth.models import AbstractUser
from django.db import models

class UserTrainer(AbstractUser):
    # --- abstract user by default has
    # username, 
    # password, 
    # email, 
    # first_name, 
    # last_name
    # is_active, is_staff, is_superuser
    # date_joined, last_login

    is_trainer = models.BooleanField(default=False) # to identify as tenant of saas

    class Meta:
        db_table = "user_trainers"
        # this is very funny, we can only add permissions in the model
        # and migration will create in the auth_permission table
        # and NOT in the django-admin only Groups can be created there
        permissions = [
            ("can_use_ai", "Can use AI features")
        ]

    def save(self, *args, **kwargs):
        # mnually trigger the validators if modelform not used, when using objec save
        self.full_clean() 
        super().save(*args, **kwargs)

    def __str__(self):
        return self.first_name