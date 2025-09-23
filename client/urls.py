from django.urls import path
from .views import login, sign_up, logout, profile


urlpatterns = [
    path('login/', login, name='login'),
    path('sign_up/', sign_up, name='sign_up'),
    path('logout/', logout, name='logout'),
    path('profile/', profile, name='profile'),
]
