import requests
from .config import tokenrefresh_api_url


class RefreshTokenMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        access = request.session.get('access')
        refresh = request.session.get('refresh')

        if not access and refresh:
            try:
                response = requests.post(
                    tokenrefresh_api_url,
                    data={'refresh': refresh}
                )
                if response.status_code == 200:
                    data = response.json()
                    request.session['access'] = data.get('access')
            
            except Exception:
                pass
            
        return self.get_response(request)

