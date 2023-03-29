from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class RegisterUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            'email', 
            'password1', 
            'password2', 
            ]
        
    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        
        if User.objects.filter(email=email).exists():
            msg = 'Пользователь с таким email уже существует'
            self.add_error('email', msg)           
    
        return self.cleaned_data


class LoginForm(AuthenticationForm):
    username = forms.EmailField(label='Адрес электронной почты')

    class Meta:
        fields = [ 'password']