from django.shortcuts import render, redirect
from client.decorators import login_required_custom
from .config import appconfig_api_url, instagram_connect_api_url
import requests
from django.contrib import messages


@login_required_custom()
def get_app_config(request):
    try:
        response = requests.get(appconfig_api_url, headers={
            'Authorization': f'Bearer {request.session.get("access")}'
        })
        if response.status_code == 200:
            data = response.json()
            return data.get('app_id'), data.get('redirect_uri')
        else:
            messages.error(request, 'Failed to receive app configurations, try again.')
            return None, None
    except Exception as e:
        messages.error(request, f'API error: {e}')
        return None, None
        

@login_required_custom()
def dashboard_home(request):
    return render(request, 'dashboard/dashboard_home.html')


@login_required_custom()
def connect_ig(request):
    if request.method == 'GET':
        return redirect('profile')
    
    elif request.method == 'POST':
        try:
            app_id, redirect_uri = get_app_config(request)
            if not app_id or not redirect_uri:
                return redirect('profile')
            scopes = [
                'instagram_business_basic',
                'instagram_business_content_publish',
                'instagram_business_manage_messages',
                'instagram_business_manage_comments',
                'instagram_business_manage_insights'
            ]
            scope_str = ','.join(scopes)


            auth_url = (
                "https://www.instagram.com/oauth/authorize"
                f"?force_reauth=true"
                f"&client_id={app_id}"
                f"&redirect_uri={redirect_uri}"
                f"&response_type=code"
                f"&scope={scope_str}"
            )
            print(f"Frontend redirect_uri: {redirect_uri}")

            return redirect(auth_url)
        
        except Exception as e:
            messages.error(request, F'Instagram Graph API Error: {e}')
            return redirect('dashboard_home')
        

@login_required_custom()
def callback_ig(request):
    try:
        authorization_code = request.GET.get('code')
        error = request.GET.get('error')

        if error:
            messages(request, f'Error during retrieveing authorization code: {error}')
            return redirect('dashboard_home')
        
        response = requests.post(
            instagram_connect_api_url,
            json={"code": authorization_code},
            headers={
                "Authorization": f"Bearer {request.session.get('access')}"
            },
            timeout=10
        )
        if response.status_code == 200:
            messages.success(request, "Instagram account connected successfully!")
        else:
            messages.error(
                request,
                f"Failed to connect Instagram. Details: {response.json().get('error', '')}"
            )
        return redirect('dashboard_home')
    
    except Exception as e:
        messages.error(request, F'Instagram Graph API Error: {e}')
        return redirect('dashboard_home')
        