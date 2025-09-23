from decouple import config



base_api_url = config('BASE_API_URL')
login_api_url = base_api_url + config('LOGIN_API_URL')
signup_api_url = base_api_url + config('SIGNUP_API_URL')
logout_api_url = base_api_url + config('LOGOUT_API_URL')
tokenrefresh_api_url = base_api_url + config('TOKENREFRESH_API_URL')
profile_api_url = base_api_url + config('PROFILE_API_URL')
