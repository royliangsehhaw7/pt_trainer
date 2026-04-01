
# https://rajpurohitdhanpal.medium.com/advanced-django-orm-query-functions-a-complete-guide-e905edb7ac68

Default Django Authentication
=========================================================================
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
        NOTE: username is still required, so we will set username = email to help with social login
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


User Redirection based on Group
==============================================================================================
Default Django Group
    --- Two groups Free and Premium - with permission can_use_ai
    --- templates/registrations
        --- login.html
    --- views
        --- account_view.py
        --- login_page
                ---- users will be redirector based on the flag is_trainer
                ---- if is_trainer is true redirect to trainer app
                ---- if NOT is_trainer tredirect o backend app
    NOTE: FOR THE BASE.HTML (for trainer app)
            --- will have to check for is_trainer to direct access to the urls
          FOR THE BASE_PUBLIC (for for landing,login,register)
          FOR THE BASE.HTML (for backend app)
            --- will have to check for is_staff



Backend Trainer Subscription (only is_staff = True)
=================================================================================================
Create a new app
    --- backend/
        --- templates/
            --- backend/
                --- subscriptions/
                    ---- subscription_list.html
                    ---- subscription_add.html
                    ---- subscription_edit.html
                    ---- subscription_deklete.hml
                    base.html
                        --- to check for is_staff = True
        --- urls.py
            ---- must verify access with login_required on all paths
        --- views
            --- subscription_view.py
                --- on save
                --- on edit
        ---forms
            --- subscription_form.py
                REFERENCE:
                    ---  https://www.guguweb.com/2014/09/10/group-combo-box-django-user-profile-form/

                --- password/confirm_password fields (non db) 
                    --- cross check on these two fields are done in the form clean() method
                --- DO not add these two fields in the Meta fields decralartion (have to encrpyt first in view)
                --- have to create a 'non-field' for a Group dropdown
                --- will get from Group.object.all()



Social Login
=============================================================================================
REFERENCES:
    --- 
