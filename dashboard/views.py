from django.shortcuts import render
from client.auth_utils import is_authenticated



def dashboard_home(request):
    is_authenticated_ = is_authenticated(request)
    return render(request, 'dashboard/dashboard_home.html', {'is_authenticated_': is_authenticated_})

