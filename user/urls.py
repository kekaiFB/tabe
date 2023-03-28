from django.urls import path, re_path
from .views import *

app_name = 'user'

urlpatterns = [
    path("", LoginUser.as_view()),
    
    path("login/", LoginUser.as_view(), name='login'),
    path("register/", registerUserForm, name='register'),
    path('activate/<uidb64>/<token>/', activate, name='activate'),  
    path("logout/", logout_user, name='logout'),
    path("error/", ErrorHandler.as_view(), name='error'),
] 
