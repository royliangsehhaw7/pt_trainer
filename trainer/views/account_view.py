from django.contrib.auth.models import Group

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect

from django.contrib.auth import authenticate, login, logout

UserTrainer = get_user_model()

def login_page(request):

    if request.method == "POST":
        email = request.POST.get('username')
        password = request.POST.get('password')

        # for simplicity, will consider username = email
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            if user.is_trainer:             # Saas tenant redirect
                return redirect('home') 
            elif user.is_staff:
                return redirect('subscription_list')

            return redirect('index')        
        else:
            messages.error(request, "Invalid Email or Password")
            return redirect('login')

    return render(request, 'registration/login.html')

def register_page(request):

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if UserTrainer.objects.filter(username=email).exists():
            messages.error(request, "Email already taken!")
            return redirect('register')

        # will set username = email
        new_userTrainer = UserTrainer.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            is_trainer=True     # rmb to set this as a trainer
        )

        # attach to existing 'Free' group all new trainer
        # RMB: *** the groups has to be manually created first after first migration
        try:
            free_group = Group.objects.get(name='Free')     #default group
            new_userTrainer.groups.add(free_group)

            messages.success(request, "Account created successfully!")
        except Exception as e:
            messages.error(request, str(e))
        # except Group.DoesNotExist:
        #     print("WARNING: 'Free' group not found in DB. User created without group.")

        return redirect('login')

    return render(request, 'registration/register.html')





# from django.shortcuts import render, redirect
# from django.contrib import messages
# from django.contrib.auth import authenticate, login, logout

# from django.contrib.auth import get_user_model  # must get the new custom auth user
# Trainer = get_user_model()

# def login_page(request):
#     if request.method == "POST":
#         email = request.POST.get('email')
#         password = request.POST.get('password')

#         # 1. Standard authentication (Since email IS the username in the DB)
#         user = authenticate(request, username=email, password=password)
#         print(f'{email} --- {password}')
#         if user is not None:
#             login(request, user)
#             if user.is_trainer:             # Saas tenant redirect
#                 return redirect('home') 

#             return redirect('index')
        
#         else:
#             # 3. Security Tip: Use a generic message so hackers don't know 
#             # if the email or the password was the mistake.
#             messages.error(request, "Invalid Email or Password")
#             return redirect('login')

#     return render(request, 'trainer/account/login.html')


# # Define a view function for the registration page
# def register_page(request):
#     if request.method == 'POST':
#         # Get data from form
#         first_name = request.POST.get('first_name')
#         last_name = request.POST.get('last_name')
#         username = request.POST.get('username') # This is the email from the UI
#         password = request.POST.get('password')
        
#         # 1. Simple check for existing user
#         if Trainer.objects.filter(username=username).exists():
#             messages.info(request, "Email already taken!")
#             return redirect('register')

#         # 2. Create, hash password, and save in ONE step
#         Trainer.objects.create_user(
#             username=username,
#             email=username,
#             password=password, # create_user hashes this automatically
#             first_name=first_name,
#             last_name=last_name,
#             is_trainer=True
#         )
        
#         messages.info(request, "Account created Successfully!")
#         return redirect('login') # Better to redirect to login after signup
    
#     return render(request, 'trainer/account/register.html')


# def account_logout(request):
#     logout(request)
#     return redirect('index')