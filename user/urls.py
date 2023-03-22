from django.urls import include, path
from .views import *

app_name = 'user'

urlpatterns = [
    path("registration/", RegistrationUser.as_view(), name='registration'),
    path("login/", LoginUser.as_view(), name='login'),
    path("logout/", logout_user, name='logout'),
    path("error/", ErrorHandler.as_view(), name='error'),
] 
