from django.urls import path
from .views import login, home, sign_up, logout


urlpatterns = [
    path('home/', home, name='home'),
    path('login/', login, name='login'),
    path('sign_up/', sign_up, name='sign_up'),
    path('logout/', logout, name='logout'),
]
