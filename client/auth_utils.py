import requests
from .config import tokenrefresh_api_url, profile_api_url

def is_authenticated(request):
    access = request.session.get('access')
    refresh = request.session.get('refresh')

    if access:
        try:
            response = requests.get(profile_api_url, headers={'Authorization': f'Bearer {access}'}, timeout=5)
            if response.status_code == 200:
                return True
            elif response.status_code == 401 and refresh:
                return refresh_access_token(request)
            else:
                return False
        except Exception:
            return False
    elif refresh:
        return refresh_access_token(request)
    return False


def refresh_access_token(request):
    refresh = request.session.get('refresh')
    if not refresh:
        return False
    try:
        response = requests.post(tokenrefresh_api_url, json={'refresh': refresh}, timeout=5)
        if response.status_code == 200:
            data = response.json()
            request.session['access'] = data.get('access')
            return True
        else:
            request.session.flush()
            return False
    except Exception:
        request.session.flush()
        return False
