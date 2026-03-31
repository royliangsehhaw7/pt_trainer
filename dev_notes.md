
Default Django Authentication
====================================================================
REFERENCES:
    --- https://supertokens.com/blog/django-user-authentication
    --- https://realpython.com/django-user-management/
    --- https://www.pragnakalp.com/django-tutorial-a-comprehensive-guide-to-use-djangos-authentication-system/


    NOTE: have to create trainer groups first
    RUN makemigrations and migrate first
    RUN createsuperuser
    FROM django-admin create new groups Free and Premium (for trainers subscription)

    NOTE: will have to abstract from AbstractUser so we can have new columns
    *****
    --- user_trainer.py (USER_TRAINERS WILL BE USED INSTEAD OF AUTH_USER)
        from django.contrib.auth.models import AbstractUser
        class UserTrainer(AbstractUser)                 # inherit from AbstractUser
            -- add new flag
                is_trainer = models.BooleanField(default=False)
            -- rename table name
                db_table = "user_trainers"
        NOTE: username is still required, so we will set username = email to bypass this    
        The django authentication will now use this new model for its base authentication

    auth_user               -   -- replaced by user_trainers
    auth_user_groups            -- replaced by user_trainers_groups
    auth_user_user_permission   -- replaced by user_trainers_user_permissions
    *****
    --- urls.py
    to configure default django authentication path
        ---     
        path("accounts/", include("django.contrib.auth.urls"))      # all path for authentication is now avalablt for use
        --- protecting path
            --- wrap  views with login_required()
    NOTE: path name is use account/
    *****
    settings.py
        --- AUTH_USER_MODEL = "orm.UserTrainer"         # tell django to use new auth user table
        --- TEMPLATES
            --- 'DIRS': [BASE_DIR / 'templates' ]       # ?? have to use these path and names, if not WONT work ???

    templates/
        ---- register.html
            --- must attach group (free) to all new trainer registrations
        ---- login.html
    views/
        --- account_view.py     (MUST create own logic for register)
                                (HAVE to crete login logic to mark is_trainer = True)


Social Login
=============================================================================================
REFERENCES:
    --- 
