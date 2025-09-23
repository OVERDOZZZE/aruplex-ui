from django.shortcuts import render
from client.decorators import login_required_custom


@login_required_custom()
def dashboard_home(request):
    return render(request, 'dashboard/dashboard_home.html')


@login_required_custom()
def connect_ig(request):
    return render(request, 'dashboard/connect_ig.html')
