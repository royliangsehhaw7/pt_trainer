from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied

def trainer_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        # 1. Is the person even logged in?
        if not request.user.is_authenticated:
            return redirect('login')
        
        # default django admin user
        if request.user.is_staff:
            raise PermissionDenied  # Or redirect('staff_dashboard') if you have it
            
        # if logged in user is a trainer
        if request.user.is_trainer:
            return view_func(request, *args, **kwargs)
        
        # 4. Fallback for anyone else
        return redirect('index')
        
    return _wrapped_view