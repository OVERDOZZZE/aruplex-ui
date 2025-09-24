from decouple import config

base_api_url = config('BASE_API_URL')
appconfig_api_url = base_api_url + config('APPCONFIG_API_URL')
