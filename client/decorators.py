from functools import wraps
from django.shortcuts import redirect 
from django.contrib import messages
from .auth_utils import is_authenticated

def redirect_authenticated(to='home'):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if is_authenticated(request):
                messages.info(request, 'You are already logged in my boy.')
                return redirect(to)
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator
