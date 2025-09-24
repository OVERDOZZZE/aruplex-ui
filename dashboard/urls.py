from django.urls import path
from .views import dashboard_home, connect_ig


urlpatterns = [
    path('', dashboard_home, name='dashboard_home'),
    path('connect-ig/', connect_ig, name='connect-ig')
]
