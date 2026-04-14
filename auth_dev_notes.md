
# https://rajpurohitdhanpal.medium.com/advanced-django-orm-query-functions-a-complete-guide-e905edb7ac68

Default Django Authentication
=========================================================================
REFERENCES:
    --- https://supertokens.com/blog/django-user-authentication
    --- https://realpython.com/django-user-management/
    --- https://www.pragnakalp.com/django-tutorial-a-comprehensive-guide-to-use-djangos-authentication-system/



    NOTE: *** have to create trainer groups first after first migrate ***

    RUN makemigrations and migrate first
    RUN createsuperuser
    FROM django-admin create new groups Free and Premium (for trainers subscription)

    NOTE: will have to abstract from AbstractUser so we can have new columns
        -- add new column
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
        --- path("accounts/", include("django.contrib.auth.urls"))  # all path for authentication is now avalablt for use
        --- protecting path
            --- wrap  views with login_required()
    NOTE: path name is use accounts/
0.  

    **** IMPORTANT *****
    --- django authentication will strictly look for folder or filenames 

    Configure auth flow and redirection
        --- settings.py
            LOGIN_URL = 'login'
            LOGIN_REDIRECT_URL = 'home'
            LOGOUT_REDIRECT_URL = 'index'

            AUTH_USER_MODEL = "orm.UserTrainer"     # tells django to use this new model as the default auth user !!! IMPORTANT

            --- TEMPLATES = [
                'DIRS': [BASE_DIR / 'templates']        *** THIS IS A MUST ***
                'APP_DIRS': True,
            ]

    Auth Folder Layout
    --- project root/templates/registration folder
        --- login.html
        --- register.html
        --- password_reset_form.html

    THE NAMES OF FOLDER AND FILES MUST BE NAMED ACCORDINGLY IN ORDER FOR THE AUTHENTICATION TO WORK
        --- MUST PROVIDE LOGIN/REGISTER/FORGOT PASSWORD TEMPLATES

        NOTE: all path in urls.py MUST USED login_required


User Redirection based on Group
==============================================================================================
Default Django Group
    --- Two groups 
        --- Free
        --- Premium - with permission can_use_ai
    --- templates/registrations
        --- login.html
    --- views
        --- account_view.py
            --- login_page
                    ---- users will be redirectod based on the flag is_trainer
                    ---- if is_trainer is true redirect to trainer app
                    ---- if NOT is_trainer tredirect o backend app
        NOTE: FOR THE BASE.HTML (for trainer/ app)
            --- will have to check for is_trainer to direct access to the urls
          FOR THE BASE_PUBLIC (for for landing,login,register)
            --- NO checks
          FOR THE BASE.HTML (for backend/ app)
            --- will have to check for is_staff

NOTE: this will result in 3 base html pages
    --- trainer/templates/trainer
        1. --- base_public.html    (THIS WILL BE USED BY LANDING,LOGIN,REGISTER HTML)
        2. --- base.html           (THIS WILL BE USED ONCE TRAINER HAS BEEN AUTHENTICATED AND AUTHORISED)
    --- backend/tempaltes/backend
        3 --- base.html             (THIS IS THE FOR BACKEND STAFF USERS / ADMINISTRTOR)



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
    --- https://python-social-auth.readthedocs.io/en/latest/configuration/django.html
    --- https://medium.com/@kennethjiang/python-social-auth-for-django-tutorial-16bbe792659f

Setup
    --- CMD: pip install social-auth-app-django
    --- CMD: py manage.py makemnigrations       (it comes with its own set of tables)
    --- CMD: py manage.py migrate

    --- config/settings.py
        --- INSTALLED_APPS = [
            ...
            'social-django'
        ]
        --- SOCIAL_AUTH_PIPELINE = (
            'social_core.pipeline.social_auth.social_details',      # get email/name from google
            'social_core.pipeline.social_auth.social_uid',          # get unique Google ID
            'social_core.pipeline.social_auth.auth_allowed',
            'social_core.pipeline.social_auth.social_user',

            'social_core.pipeline.social_auth.associate_by_email',  # will check against default AUTH_USER_MODEL table
            'social_core.pipeline.social_auth.associate_user',      # <--- THE MISSING LINK
            'social_core.pipeline.social_auth.load_extra_data',
            'social_core.pipeline.user.user_details',

            # Note: 'social_core.pipeline.user.create_user' THIS MUST BE REMARKED, IF NOT IT WILL AUTO REGISTER TO DATABASE FOR NEW LOGIN
        )
        --- AUTHENTICATION_BACKENDS = (
            'social_core.backends.google.GoogleOAuth2',
            'django.contrib.auth.backends.ModelBackend',  # Keep for username/password login
        )

        SOCIAL_AUTH_RAISE_EXCEPTIONS = True
        SOCIAL_AUTH_LOGIN_ERROR_URL = '/accounts/login/'
        SOCIAL_AUTH_CLEAN_USER_KEEP_SESSION = True
        SOCIAL_AUTH_GOOGLE_OAUTH2_AUTH_EXTRA_ARGUMENTS = {
            'prompt': 'select_account'
        }

        # ============= auth keys from social medias ======== #
        # have to register and get auth key from google cloud and github to link our app
        
        # Google
        SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '...'
        SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = '...'

        # GitHub
        SOCIAL_AUTH_GITHUB_KEY = '...'
        SOCIAL_AUTH_GITHUB_SECRET = '...'

    --- urls.py
        --- path('social-auth/', include('social_django.urls', namespace='social')),

    --- templates/registration/login.html
        --- add for both login links
            --- <a href="{% url 'social:begin' 'google-oauth2' %}" class="btn w-100">
                    <i class="bi bi-google me-2"></i> Google
                </a>
            --- <a href="{% url 'social:begin' 'github' %}" class="btn w-100">
                    <i class="bi bi-github me-2"></i> Github
                </a>  

Google API OAuth Keys
==================================================================
1. Login to Google Cloud console
2. Select a project (should the same project as the App Engine and Compute Engine)

From google console, search for "OAuth Consent Screen"
    --- Select External
    --- Key in App Name
    --- key in email and developer info
    NOTE: This is just to create a container to link our oauth clients later

From google console searech for "credentials"
    --- select create new credeitnals
        --- select OAuth Client ID
        --- select Web Application for type
        --- Authroized Javascript origins
            --- ADD http://127.0.0.1:8000                                       (FOR LOCAL TESTING)
        --- Authorized redirect URIs
            --- ADD http://127.0.0.1:8000/social-auth/complete/google-oauth2/   (FOR LOCAL TESTING)
        --- Click Create
            -- copy CLIENT ID keys      to settings.py SOCIAL_AUTH_GOOGLE_OAUTH2_KEY
            -- copy CLIENT SECRET keys  to settings.py SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET

Github OAuth Keys
=====================================================================
1. Add to settings.py
    --- SOCIAL_AUTH_GITHUB_KEY = '<<>>'
        SOCIAL_AUTH_GITHUB_SECRET = '<<>>'
        SOCIAL_AUTH_GITHUB_SCOPE = ['user:email']           # make sureto get email
2. Login Github
    --- Settings 
        --- Developer Settings
            --- Click New Oauth App
                --- Set url and callback url
            -- Under Oauth apps
                --- generate new Cient secret
                    --- COPY CLIENTID to settings.py
                    --- COPY CLIENTSECRETS to settings.py 
