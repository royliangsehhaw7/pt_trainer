from django.contrib.auth.models import Group

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect

from django.contrib.auth import authenticate, login, logout

from ..forms import AccountForm

UserTrainer = get_user_model()


def login_page(request):
    form = AccountForm(request.POST or None)

    if request.method == "POST":
        # We grab the data manually to avoid the ModelForm's "Unique" check
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username and password:
            # Authenticate checks the DB correctly without throwing "Already Exists" errors
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                return redirect('home' if user.is_trainer else 'subscription_list')
            else:
                # Add a generic error so we don't leak account info
                form.add_error(None, "Invalid Username or Password")
        else:
            form.add_error(None, "Please enter both credentials.")
            
    return render(request, 'registration/login.html', {'form': form})


def register_page(request):
    if request.method == 'POST':
        form = AccountForm(request.POST)

        # IMPORTANT :: using email as the username
        form.fields['username'].required = False
        
        # 1. Validation check (Handles password matching & email format)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')

            # if UserTrainer.objects.filter(username=email).exists():
            #     messages.error(request, "Email already taken!")
            #     return render(request, 'registration/register.html', {'form': form})

            # have to get the model back without commit to database
            # so we can add our trainer flags and set username = email
            new_userTrainer = form.save(commit=False)
            new_userTrainer.username = email        # using email as username
            new_userTrainer.is_trainer = True
            
            # have to encrypt the password first
            new_userTrainer.set_password(password)
            new_userTrainer.save()

            # finall, set the default Group (Free) for all new trainers
            try:
                free_group = Group.objects.get(name='Free')
                new_userTrainer.groups.add(free_group)

                messages.success(request, "Account created successfully!")
            except Exception as e:
                messages.error(request, f"Group Error : {str(e)}")

            return redirect('login')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = AccountForm()


    return render(request, 'registration/register.html', {'form': form})


# THIS IS SO STUPID, FORM_ISVALID WILL RUN THE FORM VALIDATION AGAINST THE DATABAE #
#
# def login_page(request):
#     # 1. Initialize the form
#     form = AccountForm(request.POST or None)

#     if request.method == "POST":
#         # this have to be set required = False for the form.isvalid to work
#         # and validate other
#         form.fields['first_name'].required = False
#         form.fields['last_name'].required = False

#         if form.is_valid():
#             # ensure return of valid python object as html input could be messy
#             username = form.cleaned_data.get('username')
#             password = form.cleaned_data.get('password')

#             user = authenticate(request, username=username, password=password)
            
#             if user is not None:
#                 login(request, user)
#                 return redirect('home' if user.is_trainer else 'subscription_list')
#             else:
#                 # 4. Attach error directly to the form object
#                 form.add_error(None, "Invalid Username or Password")
        
#     return render(request, 'registration/login.html', {'form': form})
