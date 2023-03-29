from django.urls import path, re_path
from .views import *
from django.contrib.auth.views import (
    LogoutView
)

app_name = 'user'

urlpatterns = [
    path("", LoginUser.as_view()),
    
    path("login/", LoginUser.as_view(), name='login'),
    path("register/", registerUserForm, name='register'),
    path('activate/<uidb64>/<token>/', activate, name='activate'),  
    path('logout/', LogoutView.as_view(next_page='user:login'), name='logout'),
    path("error/", ErrorHandler.as_view(), name='error'),
    
    path('password_reset/', password_reset, name='password_reset'),   
] 
