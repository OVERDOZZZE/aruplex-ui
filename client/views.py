from django.shortcuts import render, redirect
import requests
from .config import *
from django.contrib import messages
from .decorators import redirect_authenticated
from .auth_utils import is_authenticated


POST_AUTH_REDIRECT = 'dashboard_home'

@redirect_authenticated(to=POST_AUTH_REDIRECT)
def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            response = requests.post(login_api_url, json={'email': email, 'password': password})
            data = response.json()
        except Exception:
            messages.error(request, 'Authentication server error, please try again later or report in contact page.')
            return redirect('login')

        if response.status_code == 200:
            request.session['access'] = data.get('access')
            request.session['refresh'] = data.get('refresh')
            messages.success(request, 'Logged in successfully.')
            return redirect(POST_AUTH_REDIRECT)
        else:
            error_message = data.get('detail', 'Login failed, try again.')
            messages.error(request, error_message)

    return render(request, 'client/login.html')


@redirect_authenticated(to=POST_AUTH_REDIRECT)
def sign_up(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        name = request.POST.get('name')
        surname = request.POST.get('surname') 
        phone_number = request.POST.get('phone_number')  
        company_name = request.POST.get('company_name')
        business_type = request.POST.get('business_type') 
        subscription_plan = request.POST.get('subscription_plan')  
        password = request.POST.get('password')
        password_2 = request.POST.get('password_2')


        if password != password_2:
            messages.error(request, 'Passwords do not match, you have 1 popytka left')
            return render(request, 'client/signup.html')
        
        try:
            response = requests.post(signup_api_url, json={
                'email': email,
                'name': name, 
                'surname': surname, 
                'phone_number': phone_number, 
                'company_name': company_name,
                'business_type': business_type or None,  
                'subscription_plan': subscription_plan or None, 
                'password': password
            })
            data = response.json() if response.content else {}

            if response.status_code == 201:
                request.session['access'] = data.get('access')
                request.session['refresh'] = data.get('refresh')
                messages.success(request, 'Account created successfully.')
                return redirect(POST_AUTH_REDIRECT)
            error_msg = data.get('detail') or ' | '.join(
            f"{k}: {', '.join(v) if isinstance(v, list) else v}"
            for k, v in data.items()
            ) or 'Sign up failed, try again.'
            messages.error(request, error_msg)
        
        except Exception as e:
            messages.error(request, f'API error: {e}')

    return render(request, 'client/signup.html')


def logout(request):
    if request.method == 'GET':
        return redirect(POST_AUTH_REDIRECT)

    elif request.method == 'POST':
        try:
            if not is_authenticated(request):
                messages.warning(request, 'No access token found.')
        
            response = requests.post(logout_api_url, json={
                'refresh': request.session.get('refresh')
            }, headers={
                'Authorization': f'Bearer {request.session.get("access")}'
            })
            request.session.flush()
            
            if response.status_code in (200, 205):
                messages.success(request, 'You have been logged out.')
            else:
                messages.error(request, 'Logout failed on server, tokens cleared.')

        except Exception as e:
            request.session.flush()
            messages.error(request, f'API error: {e}')

    return redirect('login')

