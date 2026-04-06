from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def home(request):
    # stepper purposes
    request.session['module'] = None

    return render(request, 'trainer/home.html', {})